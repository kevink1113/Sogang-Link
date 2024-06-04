import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import '../login.dart';
import '../storage.dart';

class PostCreate extends StatefulWidget {
  @override
  _PostCreateState createState() => _PostCreateState();
}

class _PostCreateState extends State<PostCreate> {
  final _formKey = GlobalKey<FormState>();
  String _title = '';
  String _content = '';

  void _submitPost() async {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();

      var request = Uri.parse("$url/posts/");
      try {
        SecureStorage.getToken().then((token) {
          try {
            http.post(request, headers: {
              "Authorization": "Token $token"
            }, body: {
              "title": _title,
              "content": _content,
              "author": user.username
            }).then((response) {
              if (response.statusCode == 201) {
                Navigator.pop(context);
              } else {
                print("게시판 글쓰기 실패");
                print(utf8.decode(response.bodyBytes));
              }
            });
          } catch (e) {
            print("네트워크 오류");
          }
        });
      } catch (e) {
        print(e);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('새 글 쓰기'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              Align(alignment: Alignment.centerLeft, child: Text("제목")),
              TextFormField(
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value!.isEmpty) {
                    return '제목을 입력하세요';
                  }
                  return null;
                },
                onSaved: (value) {
                  _title = value!;
                },
              ),
              SizedBox(height: 20),
              Align(alignment: Alignment.centerLeft, child: Text("내용")),
              TextFormField(
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                ),
                maxLines: 10,
                validator: (value) {
                  if (value!.isEmpty) {
                    return '내용을 입력하세요';
                  }
                  return null;
                },
                onSaved: (value) {
                  _content = value!;
                },
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: _submitPost,
                child: Text('작성하기'),
                style: ElevatedButton.styleFrom(
                  padding: EdgeInsets.symmetric(horizontal: 40, vertical: 20),
                  textStyle: TextStyle(fontSize: 16),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
