import 'dart:convert';
import 'dart:math';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:soganglink/data/courses/takes.dart';
import 'package:soganglink/data/login/User.dart';
import 'package:soganglink/data/notice/notice.dart';
import 'package:soganglink/login.dart';
import 'package:soganglink/storage.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:wakelock/wakelock.dart';
import 'package:screen_brightness/screen_brightness.dart';
import 'package:http/http.dart' as http;

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);
  @override
  _HomePage createState() => _HomePage();
}

class _HomePage extends State<HomePage> {
  List<DataRow> courses = [];
  int semester = 2024010;
  NoticeList? notice = null;

  @override
  void initState() {
    super.initState();

    if (takes != null) {
      for (Take lecture in takes.cousrses_takes) {
        if (lecture.course.semester != semester) continue;

        String time = "";

        if (lecture.course.start_time != null &&
            lecture.course.end_time != null) {
          DateTime start = DateTime(2022, 12, 1, 9)
              .add(Duration(minutes: lecture.course.start_time!));
          DateTime end = DateTime(2022, 12, 1, 9)
              .add(Duration(minutes: lecture.course.end_time!));
          time = "${start.hour}:${start.minute} ~ ${end.hour}:${end.minute}";
        } else {
          time = "?";
        }
        courses.add(DataRow(cells: [
          DataCell(Text(
            lecture.course.name,
            style: TextStyle(color: Colors.black, fontSize: 15),
          )),
          DataCell(Text(
            lecture.course.classroom!,
            style: TextStyle(color: Colors.black, fontSize: 15),
          )),
          DataCell(Text(
            lecture.course.advisor!,
            style: TextStyle(color: Colors.black, fontSize: 15),
          )),
          DataCell(Text(
            time,
            style: TextStyle(color: Colors.black, fontSize: 15),
          )),
        ]));
      }
    }

    var request = Uri.parse("$url/notice");
    try {
      SecureStorage.getToken().then((token) {
        try {
          http.get(request, headers: {"Authorization": "Token $token"}).then(
              (response) {
            if (response.statusCode == 200) {
              setState(() {
                notice = NoticeList.fromJsonlist(
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
      child: Column(
        children: [
          GestureDetector(
            onTap: () {
              HapticFeedback.mediumImpact();
              showModalBottomSheet<void>(
                showDragHandle: true,
                backgroundColor: Colors.white,
                context: context,
                builder: (BuildContext context) {
                  return Container(
                    height: 500,
                    child: Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        mainAxisSize: MainAxisSize.min,
                        children: <Widget>[
                          Flexible(
                              flex: 1,
                              child: ClipRRect(
                                  borderRadius: BorderRadius.circular(30.0),
                                  child: Image.asset(
                                    "assets/images/sample.jpg",
                                    height: 100,
                                    width: 100,
                                    fit: BoxFit.contain,
                                  ))),
                          SizedBox(height: 40), // Space between lines of text
                          QrImageView(
                            data: user.username,
                            version: QrVersions.auto,
                            size: 200.0,
                          ),
                          SizedBox(height: 20), // Space between lines of text
                          Text("이름: ${user.name}"),
                          Text("소속: ${user.major}"),
                          Text("학번: ${user.username}"),
                        ],
                      ),
                    ),
                  );
                },
              );
            },
            child: Container(
                //모바일 학생증
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  color: Colors.white, // Container의 배경색
                  borderRadius: BorderRadius.circular(20), // 둥근 모서리 반경 설정
                ),
                height: 200,
                margin: EdgeInsets.fromLTRB(20, 30, 20, 10),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    Flexible(
                        flex: 1,
                        child: ClipRRect(
                            borderRadius: BorderRadius.circular(30.0),
                            child: Image.asset(
                              "assets/images/sample.jpg",
                              height: 100,
                              width: 100,
                              fit: BoxFit.contain,
                            ))),
                    Flexible(
                        flex: 2,
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text(
                              "모바일 학생증",
                              style: TextStyle(
                                color: Colors.black,
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                                letterSpacing: 2.0,
                              ),
                            ),
                            Text("이름: ${user.name}"),
                            Text("소속: ${user.major}"),
                            Text("학번: ${user.username}"),
                          ],
                        ))
                  ],
                )),
          ),
          Container(
              alignment: Alignment(-0.95, -1.0),
              decoration: BoxDecoration(
                color: Colors.white, // Container의 배경색
                borderRadius: BorderRadius.circular(20), // 둥근 모서리 반경 설정
              ),
              margin: EdgeInsets.fromLTRB(20, 20, 20, 30),
              child: Padding(
                padding: EdgeInsets.fromLTRB(10, 10, 10, 10),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: <Widget>[
                    Text(
                      "이수교과목",
                      style: TextStyle(
                        color: Colors.black,
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        letterSpacing: 2.0,
                      ),
                    ),
                    ConstrainedBox(
                      constraints:
                          const BoxConstraints(minWidth: double.infinity),
                      child: DataTable(
                          horizontalMargin: 12.0,
                          columnSpacing: 28.0,
                          columns: [
                            DataColumn(label: Text("과목명")),
                            DataColumn(label: Text("강의실")),
                            DataColumn(label: Text("교수명")),
                            DataColumn(label: Text("시간")),
                          ],
                          rows: courses),
                    ),
                  ],
                ),
              )),
          Container(
            alignment: Alignment.topLeft,
            decoration: BoxDecoration(
              color: Colors.white, // Container의 배경색
              borderRadius: BorderRadius.circular(20), // 둥근 모서리 반경 설정
            ),
            padding: EdgeInsets.fromLTRB(20, 10, 20, 10),
            margin: EdgeInsets.fromLTRB(20, 20, 20, 30),
            child: (notice != null)
                ? Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Padding(
                        padding: const EdgeInsets.only(bottom: 10.0),
                        child: Text(
                          "공지사항",
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
                        itemCount: min(notice!.noticelist.length, 10),
                        itemBuilder: ((context, index) {
                          return Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              RichText(
                                textAlign: TextAlign.left,
                                text: TextSpan(
                                  text: notice!.noticelist[index].title,
                                  style: TextStyle(
                                    fontSize: 14,
                                    color: Colors.black,
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                  recognizer: TapGestureRecognizer()
                                    ..onTap = () {
                                      launchUrl(Uri.parse(
                                          notice!.noticelist[index].url));
                                    },
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
        ],
      ),
    );
  }
}
