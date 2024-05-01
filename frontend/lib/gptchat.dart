import 'dart:convert';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
import 'package:http/http.dart' as http;
import 'package:soganglink/storage.dart';

String randomString() {
  final random = Random.secure();
  final values = List<int>.generate(16, (i) => random.nextInt(255));
  return base64UrlEncode(values);
}

class GptChat extends StatefulWidget {
  const GptChat({Key? key}) : super(key: key);
  @override
  _GptChat createState() => _GptChat();
}

class _GptChat extends State<GptChat> {
  final List<types.Message> _messages = [];
  final _user = const types.User(id: '82091008-a484-4a89-ae75-a22bf8d6f3ac');

  @override
  Widget build(BuildContext context) => Scaffold(
        body: Chat(
          l10n: const ChatL10nKo(
            inputPlaceholder: 'Here',
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

  Future<void> GPTcall(String token, String question) async {
    var request = Uri.parse("http://127.0.0.1:8000/chat");
    try {
      final response = await http.post(request, headers: {
        "Authorization": "Token $token"
      }, body: {
        "question": question,
      });

      if (response.statusCode == 200) {
        var answer =
            jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
        _addMessage(types.TextMessage(
          author: const types.User(id: 'GPT'),
          createdAt: DateTime.now().millisecondsSinceEpoch,
          id: randomString(),
          text: answer["answer"],
        ));
      }
    } catch (e) {
      print("gpt error");
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

    SecureStorage.getToken().then((token) => {
          if (token != null)
            {
              SecureStorage.getToken().then((token) => {
                    if (token != null) {GPTcall(token, message.text)}
                  })
            }
        });
  }
}
