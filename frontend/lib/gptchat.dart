import 'dart:convert';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:soganglink/storage.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:flutter/services.dart';

class GptChat extends StatefulWidget {
  const GptChat({super.key});

  @override
  _GptChatState createState() => _GptChatState();
}

class _GptChatState extends State<GptChat> {
  final List<types.Message> _messages = [];
  final _user = const types.User(id: '82091008-a484-4a89-ae75-a22bf8d6f3ac');
  String _gptMessageId = randomString();
  String _currentGptMessageText = "";

  @override
  Widget build(BuildContext context) => Scaffold(
        body: Chat(
          l10n: const ChatL10nKo(
            inputPlaceholder: '여기에 입력하세요...',
          ),
          messages: _messages,
          onSendPressed: _handleSendPressed,
          user: _user,
          showUserNames: true,
          textMessageBuilder: _customTextMessageBuilder,
        ),
      );

  void _addMessage(types.Message message) {
    setState(() {
      _messages.insert(0, message);
    });
  }

  void _updateGptMessage(String newText) {
    setState(() {
      _currentGptMessageText = newText;
      final index = _messages.indexWhere((msg) => msg.id == _gptMessageId);
      if (index != -1) {
        _messages[index] = types.TextMessage(
          author: const types.User(id: 'GPT'),
          createdAt: DateTime.now().millisecondsSinceEpoch,
          id: _gptMessageId,
          text: _currentGptMessageText,
        );
      }
    });
  }

  Future<void> GPTstreamcall(String token, String question) async {
    try {
      _gptMessageId = randomString();
      _currentGptMessageText = "";
      _addMessage(types.TextMessage(
        author: const types.User(id: 'GPT'),
        createdAt: DateTime.now().millisecondsSinceEpoch,
        id: _gptMessageId,
        text: _currentGptMessageText,
      ));

      final client = http.Client();
      final request =
          http.Request('POST', Uri.parse("http://34.64.245.20:8000/chat"));

      Map<String, String> bodyMap = {'question': question};
      request.body = jsonEncode(bodyMap);
      request.headers['Authorization'] = 'Token $token';
      request.headers['Content-type'] = 'application/json';

      final response = await client.send(request);

      if (response.statusCode != 200) {
        print(
            'Failed to connect to the server. Status code: ${response.statusCode}');
        return;
      }

      response.stream.transform(utf8.decoder).transform(const LineSplitter()).listen(
          (data) {
        data.split('\n').forEach((line) {
          if (line.startsWith("data: ")) {
            final raw = line.substring(6).trim();
            if (raw.isNotEmpty && raw != '[DONE]' && raw != 'run_completed') {
              try {
                final decoded = json.decode(raw) as Map<String, dynamic>;
                final text = decoded['text'];
                if (text != null && text.isNotEmpty) {
                  _updateGptMessage(_currentGptMessageText + text);
                  HapticFeedback.lightImpact();
                }
              } catch (e) {
                print('Error decoding JSON: $e');
              }
            }
          }
        });
      }, onDone: () {
        print("\nStream closed");
      }, onError: (error) {
        print("\nStream error: $error");
      });
    } catch (e) {
      print("\ngpt error: $e");
    }
  }

  // Future<void> _handleSendPressed(types.PartialText message) async {
  //   final textMessage = types.TextMessage(
  //     author: _user,
  //     createdAt: DateTime.now().millisecondsSinceEpoch,
  //     id: randomString(),
  //     text: message.text,
  //   );

  //   _addMessage(textMessage);

  //   final token = '527faebec62c87affb7cf30e38d3e8beac327a41';
  //   GPTstreamcall(token, message.text);
  // }

  Future<void> _handleSendPressed(types.PartialText message) async {
    final textMessage = types.TextMessage(
      author: _user,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: randomString(),
      text: message.text,
    );

    _addMessage(textMessage);

    SecureStorage.getToken().then((token) => {
          if (token != null)
            {
              SecureStorage.getToken().then((token) => {
                    if (token != null) {GPTstreamcall(token, message.text)}
                  })
            }
        });
  }

  Widget _customTextMessageBuilder(
    types.TextMessage message, {
    required int messageWidth,
    required bool showName,
  }) {
    return Container(
      padding: const EdgeInsets.all(12.0),
      constraints: BoxConstraints(maxWidth: messageWidth.toDouble()),
      decoration: BoxDecoration(
        color: message.author.id == _user.id
            ? const Color(0xFF9e2a2f)
            : Colors.grey[200],
        borderRadius: BorderRadius.circular(8.0),
      ),
      child: MarkdownBody(
        data: message.text,
        onTapLink: (text, href, title) {
          if (href != null) {
            launch(href);
          }
        },
        imageBuilder: (uri, title, alt) {
          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 8.0),
            child: Image.network(uri.toString()),
          );
        },
        styleSheet: MarkdownStyleSheet(
          p: TextStyle(
            color: message.author.id == _user.id ? Colors.white : Colors.black,
          ),
          a: TextStyle(
            color: message.author.id == _user.id ? Colors.blue : Colors.blue,
          ),
        ),
      ),
    );
  }
}

String randomString() {
  final random = Random.secure();
  final values = List<int>.generate(16, (i) => random.nextInt(255));
  return base64UrlEncode(values);
}
