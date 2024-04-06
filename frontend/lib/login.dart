import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:soganglink/home.dart';
import 'storage.dart'; // Import the secure storage class
import 'package:fluttertoast/fluttertoast.dart';
import 'package:lottie/lottie.dart';

class Login extends StatefulWidget {
  @override
  _LoginState createState() => _LoginState();
}

class _LoginState extends State<Login> {
  final idController = TextEditingController();
  final passwordController = TextEditingController();
  final String url = "http://127.0.0.1:8000/login";
  bool isLoading = false;
  bool isVerified = false;

  // print saved token
  void printToken() async {
    var token = await SecureStorage.getToken();
    print(token);
  }

  Future<void> login() async {
    setState(() {
      isLoading = true;
    });

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
        setState(() {
          isVerified = true;
        });
        Future.delayed(Duration(seconds: 2), () {
          Navigator.pushReplacement(
              context, MaterialPageRoute(builder: (_) => Home()));
        });
      } else {
        showToast("로그인 실패");
      }
    } catch (e) {
      showToast("네트워크 오류");
    } finally {
      setState(() {
        isLoading = false;
      });
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
      body: isLoading
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Lottie.asset('assets/lotties/loading_doc.json',
                      width: 400, height: 200), // Loading animation
                  Text(
                    '학사 정보를 불러오는 중입니다...',
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                  Text(
                    '잠시만 기다려주세요.',
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                ],
              ),
            )
          : isVerified
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Lottie.asset('assets/lotties/check.json',
                          width: 400, height: 200), // Loading animation
                      Text(
                        '로딩 완료!',
                        style: TextStyle(
                            fontSize: 20, fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                )
              : AnimatedSwitcher(
                  duration: Duration(milliseconds: 500),
                  child: Column(
                    key: ValueKey<bool>(isLoading),
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
                            color: Colors.blue,
                            borderRadius: BorderRadius.circular(20)),
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
                ),
    );
  }
}
