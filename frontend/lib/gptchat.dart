import 'dart:convert';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
import 'package:http/http.dart' as http;
import 'package:soganglink/storage.dart';

class GptChat extends StatefulWidget {
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
        // appBar: AppBar(
        //   title: Text('Flutter Chat Demo'),
        // ),
        body: Chat(
          l10n: const ChatL10nKo(
            inputPlaceholder: '여기에 입력하세요...',
          ),
          messages: _messages,
          onSendPressed: _handleSendPressed,
          user: _user,
          showUserNames: true,
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

      response.stream.transform(utf8.decoder).transform(LineSplitter()).listen(
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

  Future<void> _handleSendPressed(types.PartialText message) async {
    final textMessage = types.TextMessage(
      author: _user,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: randomString(),
      text: message.text,
    );

    _addMessage(textMessage);

    final token = '527faebec62c87affb7cf30e38d3e8beac327a41';
    GPTstreamcall(token, message.text);
  }
}

String randomString() {
  final random = Random.secure();
  final values = List<int>.generate(16, (i) => random.nextInt(255));
  return base64UrlEncode(values);
}
