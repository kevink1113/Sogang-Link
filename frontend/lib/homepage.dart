import 'dart:convert';
import 'dart:math';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:soganglink/data/courses/takes.dart';
import 'package:soganglink/data/login/User.dart';
import 'package:soganglink/data/menu/menu.dart';
import 'package:soganglink/data/notice/notice.dart';
import 'package:soganglink/login.dart';
import 'package:soganglink/storage.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:wakelock/wakelock.dart';
import 'package:screen_brightness/screen_brightness.dart';
import 'package:http/http.dart' as http;

NoticeList? notice = null;
NoticeList? academic_notice = null;
NoticeList? scholarship_notice = null;
MenuList? menulist = null;
DateTime today = DateTime.now();

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePage createState() => _HomePage();
}

class _HomePage extends State<HomePage> with SingleTickerProviderStateMixin {
  List<DataRow> courses = [];
  int semester = 2024010;
  List<DataRow> bwmenus = []; //우정원 학식
  List<DataRow> emmenus = []; //엠마오 학식
  TabController? _tabController;

  @override
  void initState() {
    super.initState();

    today = DateTime.now();
    today = DateTime(today.year, today.month, today.day);
    print("today : $today");
    _tabController = TabController(length: 3, vsync: this);

    if (takes != null) {
      for (Take lecture in takes.cousrses_takes) {
        if (lecture.course.semester != semester) continue;

        String time = "";

        if (lecture.course.start_time != null &&
            lecture.course.end_time != null) {
          DateTime start = DateTime(today.year, today.month, today.day, 9)
              .add(Duration(minutes: lecture.course.start_time!));
          DateTime end = DateTime(today.year, today.month, today.day, 9)
              .add(Duration(minutes: lecture.course.end_time!));
          time = "${start.hour}:${start.minute} ~ ${end.hour}:${end.minute}";
        } else {
          time = "?";
        }

        for (var char in lecture.course.day!.runes) {
          if (String.fromCharCode(char) == today.weekday.toString()) {
            courses.add(DataRow(cells: [
              DataCell(Text(
                lecture.course.name,
                style: TextStyle(
                  color: Colors.black,
                  fontSize: 13,
                ),
              )),
              DataCell(Text(
                lecture.course.classroom!,
                style: TextStyle(color: Colors.black, fontSize: 13),
              )),
              DataCell(Text(
                lecture.course.advisor!,
                style: TextStyle(color: Colors.black, fontSize: 13),
              )),
              DataCell(Text(
                time,
                style: TextStyle(color: Colors.black, fontSize: 13),
              )),
            ]));
            break;
          }
        }
      }
    }

    try {
      SecureStorage.getToken().then((token) {
        try {
          http.get(Uri.parse("$url/notice?board=일반공지"),
              headers: {"Authorization": "Token $token"}).then((response) {
            if (response.statusCode == 200) {
              setState(() {
                notice = NoticeList.fromJsonlist(
                    jsonDecode(utf8.decode(response.bodyBytes)));
              });
            } else {
              print("로그인 실패");
            }
          });
          http.get(Uri.parse("$url/notice?board=학사공지"),
              headers: {"Authorization": "Token $token"}).then((response) {
            if (response.statusCode == 200) {
              setState(() {
                academic_notice = NoticeList.fromJsonlist(
                    jsonDecode(utf8.decode(response.bodyBytes)));
              });
            } else {
              print("로그인 실패");
            }
          });
          http.get(Uri.parse("$url/notice?board=장학공지"),
              headers: {"Authorization": "Token $token"}).then((response) {
            if (response.statusCode == 200) {
              setState(() {
                scholarship_notice = NoticeList.fromJsonlist(
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

    try {
      SecureStorage.getToken().then((token) {
        try {
          http.get(Uri.parse("$url/maps/menus"),
              headers: {"Authorization": "Token $token"}).then((response) {
            if (response.statusCode == 200) {
              setState(() {
                menulist = MenuList.fromJsonlist(
                    jsonDecode(utf8.decode(response.bodyBytes)));
                if (menulist != null) {
                  if (menulist!.BW.items_by_date[today] != null) {
                    for (var key
                        in menulist!.BW.items_by_date[today]!.keys.toList()) {
                      print(key);
                      print(menulist!.BW.items_by_date[today]![key][0]);
                      bwmenus.add(DataRow(cells: [
                        DataCell(Text(
                          key,
                          style: TextStyle(color: Colors.black, fontSize: 13),
                        )),
                        DataCell(Text(
                          menulist!.BW.items_by_date[today]![key][0],
                          style: TextStyle(color: Colors.black, fontSize: 13),
                          overflow: TextOverflow.visible,
                          softWrap: true,
                        )),
                      ]));
                    }
                    if (menulist!.Em.items_by_date[today] != null) {
                      for (var key
                          in menulist!.Em.items_by_date[today]!.keys.toList()) {
                        print(key);
                        print(menulist!.Em.items_by_date[today]![key][0]);
                        emmenus.add(DataRow(cells: [
                          DataCell(Text(
                            key,
                            style: TextStyle(color: Colors.black, fontSize: 13),
                          )),
                          DataCell(Text(
                            menulist!.Em.items_by_date[today]![key][0],
                            style: TextStyle(color: Colors.black, fontSize: 13),
                            overflow: TextOverflow.visible,
                            softWrap: true,
                          )),
                        ]));
                      }
                    }
                  }
                }
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
                height: 180,
                margin: EdgeInsets.fromLTRB(15, 0, 15, 0),
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
            margin: EdgeInsets.fromLTRB(25, 15, 0, 0),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Image.asset(
                  'assets/images/5401392.png', // 아이콘 경로
                  height: 20, // 아이콘 높이
                  width: 20, // 아이콘 너비
                ),
                SizedBox(width: 8), // 아이콘과 텍스트 사이의 간격
                Text(
                  "오늘의 강의",
                  style: TextStyle(
                    color: Colors.black,
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                    // letterSpacing: 2.0,
                  ),
                ),
              ],
            ),
          ),
          Container(
              alignment: Alignment(-0.95, -1.0),
              decoration: BoxDecoration(
                color: Colors.white, // Container의 배경색
                borderRadius: BorderRadius.circular(20), // 둥근 모서리 반경 설정
              ),
              margin: EdgeInsets.fromLTRB(15, 10, 15, 20),
              child: Padding(
                padding: EdgeInsets.fromLTRB(10, 10, 10, 10),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: <Widget>[
                    ConstrainedBox(
                      constraints:
                          const BoxConstraints(minWidth: double.infinity),
                      child: (courses.length != 0)
                          ? DataTable(
                              horizontalMargin: 6.0,
                              columnSpacing: 9.0,
                              columns: [
                                DataColumn(
                                    label: Text(
                                  "과목명",
                                  style: TextStyle(
                                      fontSize: 13,
                                      fontWeight: FontWeight.w600),
                                )),
                                DataColumn(
                                    label: Text(
                                  "강의실",
                                  style: TextStyle(
                                      fontSize: 13,
                                      fontWeight: FontWeight.w600),
                                )),
                                DataColumn(
                                    label: Text(
                                  "교수명",
                                  style: TextStyle(
                                      fontSize: 13,
                                      fontWeight: FontWeight.w600),
                                )),
                                DataColumn(
                                    label: Text(
                                  "시간",
                                  style: TextStyle(
                                      fontSize: 13,
                                      fontWeight: FontWeight.w600),
                                )),
                              ],
                              rows: courses)
                          : Center(child: Text('오늘은 공강입니다')),
                    ),
                  ],
                ),
              )),
          Container(
              margin: EdgeInsets.fromLTRB(15, 10, 15, 20),
              child: (menulist != null)
                  ? SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        children: [
                          Column(children: [
                            Container(
                              padding: EdgeInsets.all(15),
                              decoration: BoxDecoration(
                                color: Colors.white, // Container의 배경색
                                borderRadius: BorderRadius.circular(20),
                                // 둥근 모서리 반경 설정
                              ),
                              child: Image.asset(
                                'assets/images/restaurant_1.png', // 아이콘 경로
                                height: 25, // 아이콘 높이
                                width: 25, // 아이콘 너비
                              ),
                            ),
                            SizedBox(height: 8),
                            Text("음식점 추천", style: TextStyle(fontSize: 11)),
                          ]),
                          SizedBox(width: 30),
                          Column(children: [
                            Container(
                              padding: EdgeInsets.all(15),
                              decoration: BoxDecoration(
                                color: Colors.white, // Container의 배경색
                                borderRadius: BorderRadius.circular(20),
                                // 둥근 모서리 반경 설정
                              ),
                              child: Image.asset(
                                'assets/images/building.png', // 아이콘 경로
                                height: 25, // 아이콘 높이
                                width: 25, // 아이콘 너비
                              ),
                            ),
                            SizedBox(height: 8),
                            Text("빈 강의실", style: TextStyle(fontSize: 11)),
                          ]),
                          SizedBox(width: 30),
                          Column(children: [
                            Container(
                              padding: EdgeInsets.all(15),
                              decoration: BoxDecoration(
                                color: Colors.white, // Container의 배경색
                                borderRadius: BorderRadius.circular(20),
                                // 둥근 모서리 반경 설정
                              ),
                              child: Image.asset(
                                'assets/images/book.png', // 아이콘 경로
                                height: 25, // 아이콘 높이
                                width: 25, // 아이콘 너비
                              ),
                            ),
                            SizedBox(height: 8),
                            Text("열람실 현황", style: TextStyle(fontSize: 11)),
                          ]),
                          SizedBox(width: 30),
                          Column(children: [
                            Container(
                              padding: EdgeInsets.all(15),
                              decoration: BoxDecoration(
                                color: Colors.white, // Container의 배경색
                                borderRadius: BorderRadius.circular(20),
                                // 둥근 모서리 반경 설정
                              ),
                              child: Image.asset(
                                'assets/images/score.png', // 아이콘 경로
                                height: 25, // 아이콘 높이
                                width: 25, // 아이콘 너비
                              ),
                            ),
                            SizedBox(height: 8),
                            Text("성적 계산기", style: TextStyle(fontSize: 11)),
                          ]),
                          SizedBox(width: 30),
                          Column(children: [
                            Container(
                              padding: EdgeInsets.all(15),
                              decoration: BoxDecoration(
                                color: Colors.white, // Container의 배경색
                                borderRadius: BorderRadius.circular(20),
                                // 둥근 모서리 반경 설정
                              ),
                              child: Image.asset(
                                'assets/images/sogang_icon.png', // 아이콘 경로
                                height: 25, // 아이콘 높이
                                width: 25, // 아이콘 너비
                              ),
                            ),
                            SizedBox(height: 8),
                            Text("SAINT", style: TextStyle(fontSize: 11)),
                          ]),
                        ],
                      ),
                    )
                  : Center(child: Text('로딩중'))),
          Container(
            margin: EdgeInsets.fromLTRB(25, 15, 0, 0),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Image.asset(
                  'assets/images/restaurant.png', // 아이콘 경로
                  height: 20, // 아이콘 높이
                  width: 20, // 아이콘 너비
                ),
                SizedBox(width: 8), // 아이콘과 텍스트 사이의 간격
                Text(
                  "학식",
                  style: TextStyle(
                    color: Colors.black,
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                    // letterSpacing: 2.0,
                  ),
                ),
              ],
            ),
          ),
          Container(
              margin: EdgeInsets.fromLTRB(15, 10, 15, 20),
              child: (menulist != null)
                  ? SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        children: [
                          Container(
                            width: 400,
                            decoration: BoxDecoration(
                              color: Colors.white, // Container의 배경색
                              borderRadius:
                                  BorderRadius.circular(20), // 둥근 모서리 반경 설정
                            ),
                            child: Column(
                              children: [
                                Padding(
                                  padding: EdgeInsets.fromLTRB(10, 0, 10, 0),
                                  child: Align(
                                      alignment: Alignment.centerLeft,
                                      child: Text(
                                        menulist!.BW.facility_name,
                                        style: TextStyle(
                                          fontSize: 12,
                                          fontWeight: FontWeight.w600,
                                        ),
                                      )),
                                ),
                                (bwmenus.length != 0)
                                    ? ConstrainedBox(
                                        constraints: const BoxConstraints(
                                            minWidth: double.infinity),
                                        child: DataTable(
                                            horizontalMargin: 12.0,
                                            columnSpacing: 30.0,
                                            dataRowMaxHeight: double.infinity,
                                            headingRowHeight: 0,
                                            dividerThickness: 0,
                                            columns: [
                                              DataColumn(label: Text("")),
                                              DataColumn(label: Text("")),
                                            ],
                                            rows: bwmenus),
                                      )
                                    : Center(child: Text('오늘은 학식이 없습니다.'))
                              ],
                            ),
                          ),
                          SizedBox(
                            width: 50,
                            child: Container(),
                          ),
                          Container(
                            width: 400,
                            decoration: BoxDecoration(
                              color: Colors.white, // Container의 배경색
                              borderRadius:
                                  BorderRadius.circular(20), // 둥근 모서리 반경 설정
                            ),
                            child: Column(
                              children: [
                                Padding(
                                  padding: EdgeInsets.fromLTRB(10, 0, 10, 0),
                                  child: Align(
                                      alignment: Alignment.centerLeft,
                                      child: Text(
                                        menulist!.Em.facility_name,
                                        style: TextStyle(
                                          fontSize: 12,
                                          fontWeight: FontWeight.w600,
                                        ),
                                      )),
                                ),
                                (emmenus.length != 0)
                                    ? ConstrainedBox(
                                        constraints: const BoxConstraints(
                                            minWidth: double.infinity),
                                        child: DataTable(
                                            horizontalMargin: 12.0,
                                            columnSpacing: 28.0,
                                            dataRowMaxHeight: double.infinity,
                                            headingRowHeight: 0,
                                            columns: [
                                              DataColumn(label: Text("")),
                                              DataColumn(label: Text("")),
                                            ],
                                            rows: emmenus),
                                      )
                                    : Center(child: Text('오늘은 학식이 없습니다.'))
                              ],
                            ),
                          )
                        ],
                      ),
                    )
                  : Center(child: Text('로딩중'))),
          Container(
            margin: EdgeInsets.fromLTRB(25, 15, 0, 0),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Image.asset(
                  'assets/images/megaphone.png', // 아이콘 경로
                  height: 20, // 아이콘 높이
                  width: 20, // 아이콘 너비
                ),
                SizedBox(width: 8), // 아이콘과 텍스트 사이의 간격
                Text(
                  "공지사항",
                  style: TextStyle(
                    color: Colors.black,
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                    // letterSpacing: 2.0,
                  ),
                ),
              ],
            ),
          ),
          TabBar(
            controller: _tabController,
            tabs: [
              Tab(text: '일반공지'),
              Tab(text: '학사공지'),
              Tab(text: '장학공지'),
            ],
          ),
          SizedBox(
            height: 800,
            child: TabBarView(
              controller: _tabController,
              children: [
                Container(
                  alignment: Alignment.topLeft,
                  decoration: BoxDecoration(
                    color: Colors.white, // Container의 배경색
                    borderRadius: BorderRadius.circular(20), // 둥근 모서리 반경 설정
                  ),
                  padding: EdgeInsets.fromLTRB(15, 10, 15, 10),
                  margin: EdgeInsets.fromLTRB(15, 20, 15, 30),
                  child: (notice != null)
                      ? Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            ListView.builder(
                              shrinkWrap: true,
                              physics: NeverScrollableScrollPhysics(),
                              itemCount: min(notice!.noticelist.length, 20),
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
                                            .shade200), // Add a divider between items
                                  ],
                                );
                              }),
                            )
                          ],
                        )
                      : Center(child: Text('로딩중')),
                ),
                Container(
                  alignment: Alignment.topLeft,
                  decoration: BoxDecoration(
                    color: Colors.white, // Container의 배경색
                    borderRadius: BorderRadius.circular(20), // 둥근 모서리 반경 설정
                  ),
                  padding: EdgeInsets.fromLTRB(15, 10, 15, 10),
                  margin: EdgeInsets.fromLTRB(20, 20, 20, 30),
                  child: (academic_notice != null)
                      ? Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            ListView.builder(
                              shrinkWrap: true,
                              physics: NeverScrollableScrollPhysics(),
                              itemCount:
                                  min(academic_notice!.noticelist.length, 20),
                              itemBuilder: ((context, index) {
                                return Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    RichText(
                                      textAlign: TextAlign.left,
                                      text: TextSpan(
                                        text: academic_notice!
                                            .noticelist[index].title,
                                        style: TextStyle(
                                          fontSize: 14,
                                          color: Colors.black,
                                          overflow: TextOverflow.ellipsis,
                                        ),
                                        recognizer: TapGestureRecognizer()
                                          ..onTap = () {
                                            launchUrl(Uri.parse(academic_notice!
                                                .noticelist[index].url));
                                          },
                                      ),
                                      maxLines: 1,
                                    ),
                                    Divider(
                                        color: Colors.grey
                                            .shade200), // Add a divider between items
                                  ],
                                );
                              }),
                            )
                          ],
                        )
                      : Center(child: Text('로딩중')),
                ),
                Container(
                  alignment: Alignment.topLeft,
                  decoration: BoxDecoration(
                    color: Colors.white, // Container의 배경색
                    borderRadius: BorderRadius.circular(20), // 둥근 모서리 반경 설정
                  ),
                  padding: EdgeInsets.fromLTRB(15, 10, 15, 10),
                  margin: EdgeInsets.fromLTRB(20, 20, 20, 30),
                  child: (scholarship_notice != null)
                      ? Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            ListView.builder(
                              shrinkWrap: true,
                              physics: NeverScrollableScrollPhysics(),
                              itemCount: min(
                                  scholarship_notice!.noticelist.length, 20),
                              itemBuilder: ((context, index) {
                                return Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    RichText(
                                      textAlign: TextAlign.left,
                                      text: TextSpan(
                                        text: scholarship_notice!
                                            .noticelist[index].title,
                                        style: TextStyle(
                                          fontSize: 14,
                                          color: Colors.black,
                                          overflow: TextOverflow.ellipsis,
                                        ),
                                        recognizer: TapGestureRecognizer()
                                          ..onTap = () {
                                            launchUrl(Uri.parse(
                                                scholarship_notice!
                                                    .noticelist[index].url));
                                          },
                                      ),
                                      maxLines: 1,
                                    ),
                                    Divider(
                                        color: Colors.grey
                                            .shade200), // Add a divider between items
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
          )
        ],
      ),
    );
  }
}
