import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:http/http.dart' as http;
import 'package:soganglink/data/courses/takes.dart';
import 'package:soganglink/data/login/User.dart';
import 'package:soganglink/home.dart';
import 'storage.dart'; // Import the secure storage class
import 'package:fluttertoast/fluttertoast.dart';
import 'package:lottie/lottie.dart';

final String url = "http://127.0.0.1:8000";

late User user;
late Takes takes;
late Set semester_list;

class Login extends StatefulWidget {
  @override
  _LoginState createState() => _LoginState();
}

class _LoginState extends State<Login> {
  final idController = TextEditingController();
  final passwordController = TextEditingController();
  bool isLoading = false;
  bool isVerified = false;
  int semester = 2024010;

  // print saved token
  void printToken() async {
    var token = await SecureStorage.getToken();
    print(token);
  }

  @override
  initState() {
    // TODO: implement initState
    super.initState();

    SecureStorage.getToken().then((token) => {
          if (token != null) {tokenlogin(token)}
        });
  }

  Future<void> login() async {
    setState(() {
      isLoading = true;
    });

    var request = Uri.parse("$url/login");
    try {
      final response = await http.post(request, body: {
        "username": idController.text,
        "password": passwordController.text
      });

      if (response.statusCode == 200) {
        var data =
            jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
        String token = data['token'];
        user = User.fromJson(data);
        await SecureStorage.setToken(token); // Store token securely
        takes = (await get_timetable(token))!;
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

  Future<void> tokenlogin(String token) async {
    setState(() {
      isLoading = true;
    });
    var request = Uri.parse("$url/users/info");
    try {
      final response =
          await http.get(request, headers: {"Authorization": "Token $token"});

      if (response.statusCode == 200) {
        var data =
            jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
        user = User.fromJson(data);
        takes = (await get_timetable(token))!;
        // setState(() {
        //   isVerified = true;
        // });
        // Future.delayed(Duration(seconds: 0), () {
        Navigator.pushReplacement(
            context, MaterialPageRoute(builder: (_) => Home()));
        // });
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

  Future<Takes?> get_timetable(String token) async {
    try {
      var request = Uri.parse("$url/lecture/takes");
      // var token = await storage.read(key: 'token');
      // convert token to base64
      // printToken();

      final response =
          await http.get(request, headers: {"Authorization": "Token $token"});

      var tmp = jsonDecode(utf8.decode(response.bodyBytes));
      Takes takes = Takes.fromJsonlist(tmp);
      if (response.statusCode == 200) {
        // Assuming 'Home' is your home widget after login success
        return takes;
      } else {
        Fluttertoast.showToast(
            msg: "로그인 실패",
            toastLength: Toast.LENGTH_SHORT,
            gravity: ToastGravity.CENTER,
            timeInSecForIosWeb: 1,
            backgroundColor: Colors.red,
            textColor: Colors.white,
            fontSize: 16.0);
        return null;
      }
    } catch (e) {
      print(e);
      Fluttertoast.showToast(
          msg: "네트워크 오류",
          toastLength: Toast.LENGTH_SHORT,
          gravity: ToastGravity.CENTER,
          timeInSecForIosWeb: 1,
          backgroundColor: Colors.red,
          textColor: Colors.white,
          fontSize: 16.0);
      return null;
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
    return Scaffold(
      backgroundColor: Colors.white,
      body: isLoading
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Lottie.asset('assets/lotties/loading_doc.json',
                      width: 400, height: 200), // Loading animation
                  const Text(
                    '학사 정보를 불러오는 중입니다...',
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                  const Text(
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
                          width: 400, height: 200), // Success animation
                      const Text(
                        '로딩 완료!',
                        style: TextStyle(
                            fontSize: 20, fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                )
              : Center(
                  child: SingleChildScrollView(
                    child: ConstrainedBox(
                      constraints: BoxConstraints(
                        minHeight: MediaQuery.of(context).size.height,
                      ),
                      child: IntrinsicHeight(
                        child: Padding(
                          padding: EdgeInsets.symmetric(horizontal: 15),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              // const Padding(
                              //   padding: EdgeInsets.only(top: 60),
                              //   child: Icon(Icons.login, size: 100),
                              // ),
                              Padding(
                                padding:
                                    const EdgeInsets.only(top: 60, bottom: 0),
                                child: Lottie.asset(
                                    'assets/lotties/school_stuffs.json',
                                    width: 400,
                                    height: 200), // Loading animation
                              ),
                              Container(
                                padding: const EdgeInsets.only(
                                    left: 15.0,
                                    right: 15.0,
                                    top: 50,
                                    bottom: 0),
                                width: MediaQuery.of(context).size.width > 1200
                                    ? 400
                                    : MediaQuery.of(context).size.width,
                                child: TextField(
                                  controller: idController,
                                  decoration: const InputDecoration(
                                    labelText: '학번',
                                    // hintText: '학번',
                                    prefixIcon: Icon(Icons.school),
                                    // border: OutlineInputBorder(),

                                    filled: true,
                                    // fill color is light grey
                                    fillColor:
                                        Color.fromARGB(255, 232, 232, 232),
                                  ),
                                ),
                              ),
                              Container(
                                width: MediaQuery.of(context).size.width > 1200
                                    ? 400
                                    : MediaQuery.of(context).size.width,
                                padding: const EdgeInsets.only(
                                    left: 15.0,
                                    right: 15.0,
                                    top: 15,
                                    bottom: 50),
                                child: TextField(
                                  controller: passwordController,
                                  obscureText: true,
                                  decoration: const InputDecoration(
                                    labelText: 'SAINT 비밀번호',
                                    // hintText: 'SAINT 비밀번호',
                                    prefixIcon: Icon(Icons.lock_outline),
                                    // border: OutlineInputBorder(),
                                    filled: true,
                                    fillColor:
                                        Color.fromARGB(255, 232, 232, 232),
                                  ),
                                  onSubmitted: (value) => login(),
                                ),
                              ),
                              SizedBox(height: 10),
                              const Text(
                                'SAINT 계정을 이용하여 로그인합니다.\n암호는 서버에 저장되지 않으며\n학사정보 연동에만 사용됩니다.',
                                style: TextStyle(
                                    color: Colors.grey,
                                    fontSize: 15,
                                    fontWeight: FontWeight.bold),
                                textAlign: TextAlign.center,
                              ),
                              Spacer(), // Use Spacer to push the button towards the bottom
                              Padding(
                                padding: const EdgeInsets.only(
                                  top: 20,
                                  bottom: 20,
                                  left: 10,
                                  right: 10,
                                ), // Reduced bottom padding
                                child: Container(
                                  height: 60,
                                  width:
                                      MediaQuery.of(context).size.width > 1200
                                          ? 400
                                          : MediaQuery.of(context).size.width,
                                  decoration: BoxDecoration(
                                      color: Color(0xFF9e2a2f),
                                      borderRadius: BorderRadius.circular(15)),
                                  child: TextButton(
                                    onPressed: () {
                                      login();
                                    },
                                    child: const Text(
                                      'SAINT 계정으로 로그인',
                                      style: TextStyle(
                                        color: Colors.white,
                                        fontSize: 18,
                                        fontWeight: FontWeight.w600,
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
    );
  }
}
