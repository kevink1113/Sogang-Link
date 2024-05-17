import 'dart:convert';
import 'dart:math';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:soganglink/data/board/postlist.dart';
import 'package:soganglink/data/courses/takes.dart';
import 'package:soganglink/data/login/User.dart';
import 'package:soganglink/data/notice/notice.dart';
import 'package:soganglink/login.dart';
import 'package:soganglink/storage.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:wakelock/wakelock.dart';
import 'package:screen_brightness/screen_brightness.dart';
import 'package:http/http.dart' as http;

class Board extends StatefulWidget {
  const Board({Key? key}) : super(key: key);
  @override
  _Board createState() => _Board();
}

class _Board extends State<Board> {
  List<DataRow> courses = [];
  int semester = 2024010;
  PostList? post = null;

  @override
  void initState() {
    super.initState();

    var request = Uri.parse("$url/posts/");
    try {
      SecureStorage.getToken().then((token) {
        try {
          http.get(request, headers: {"Authorization": "Token $token"}).then(
              (response) {
            if (response.statusCode == 200) {
              setState(() {
                post = PostList.fromJsonlist(
                    jsonDecode(utf8.decode(response.bodyBytes)));
              });
            } else {
              print("로그인 실패");
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

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Container(
        alignment: Alignment.topLeft,
        decoration: BoxDecoration(
          color: Colors.white, // Container의 배경색
          borderRadius: BorderRadius.circular(20), // 둥근 모서리 반경 설정
        ),
        padding: EdgeInsets.fromLTRB(20, 10, 20, 10),
        margin: EdgeInsets.fromLTRB(20, 20, 20, 30),
        child: (post != null)
            ? Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Padding(
                    padding: const EdgeInsets.only(bottom: 10.0),
                    child: Text(
                      "자유게시판",
                      textAlign: TextAlign.left,
                      style: TextStyle(
                        color: Colors.black,
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  ListView.builder(
                    shrinkWrap: true,
                    physics: NeverScrollableScrollPhysics(),
                    itemCount: min(post!.postList.length, 20),
                    itemBuilder: ((context, index) {
                      return Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          RichText(
                            textAlign: TextAlign.left,
                            text: TextSpan(
                              text: post!.postList[index].title,
                              style: TextStyle(
                                fontSize: 14,
                                color: Colors.black,
                                overflow: TextOverflow.ellipsis,
                              ),
                              recognizer: TapGestureRecognizer()..onTap = () {},
                            ),
                            maxLines: 1,
                          ),
                          Divider(
                              color: Colors.grey
                                  .shade300), // Add a divider between items
                        ],
                      );
                    }),
                  )
                ],
              )
            : Center(child: Text('로딩중')),
      ),
    );
  }
}
