import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:soganglink/home.dart';
import 'storage.dart'; // Import the secure storage class
import 'package:fluttertoast/fluttertoast.dart';

class Login extends StatefulWidget {
  @override
  _LoginState createState() => _LoginState();
}

class _LoginState extends State<Login> {
  final idController = TextEditingController();
  final passwordController = TextEditingController();
  final String url = "http://127.0.0.1:8000/login";

  // print saved token
  void printToken() async {
    var token = await SecureStorage.getToken();
    print(token);
  }

  Future<void> login() async {
    var request = Uri.parse(url);
    try {
      final response = await http.post(request, body: {
        "username": idController.text,
        "password": passwordController.text
      });

      if (response.statusCode == 200) {
        var data = jsonDecode(response.body);
        String token = data['token'];
        await SecureStorage.setToken(token); // Store token securely
        Navigator.pushReplacement(
            context, MaterialPageRoute(builder: (_) => Home()));
      } else {
        showToast("로그인 실패");
      }
    } catch (e) {
      showToast("네트워크 오류");
    }
  }

  void showToast(String msg) {
    Fluttertoast.showToast(
      msg: msg,
      toastLength: Toast.LENGTH_SHORT,
      gravity: ToastGravity.CENTER,
      timeInSecForIosWeb: 1,
      backgroundColor: Colors.red,
      textColor: Colors.white,
      fontSize: 16.0,
    );
  }

  @override
  Widget build(BuildContext context) {
    // print saved token
    // printToken();
    return Scaffold(
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.only(top: 60.0),
            child: Center(
              child: Container(
                width: 200,
                height: 150,
                child: Icon(Icons.login, size: 100),
              ),
            ),
          ),
          Padding(
            padding: EdgeInsets.symmetric(horizontal: 15),
            child: TextField(
              controller: idController,
              decoration: InputDecoration(
                labelText: '학번',
                hintText: '학번을 입력해주세요',
                prefixIcon: Icon(Icons.school),
                border: OutlineInputBorder(),
                filled: true,
                fillColor: Colors.white,
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.only(
                left: 15.0, right: 15.0, top: 15, bottom: 0),
            child: TextField(
              controller: passwordController,
              obscureText: true,
              decoration: InputDecoration(
                labelText: 'SAINT 비밀번호',
                hintText: '비밀번호를 입력해주세요',
                prefixIcon: Icon(Icons.lock_outline),
                border: OutlineInputBorder(),
                filled: true,
                fillColor: Colors.white,
              ),
              onSubmitted: (value) => login(),
            ),
          ),
          SizedBox(
            height: 200,
          ),
          Container(
            height: 50,
            width: 250,
            decoration: BoxDecoration(
                color: Colors.blue, borderRadius: BorderRadius.circular(20)),
            child: TextButton(
              onPressed: () {
                login();
              },
              child: Text(
                'Login',
                style: TextStyle(color: Colors.white, fontSize: 25),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
