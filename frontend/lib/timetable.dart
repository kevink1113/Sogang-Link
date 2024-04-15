import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:async';
import 'dart:math';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'package:soganglink/data/courses/takes.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'login.dart';

import 'storage.dart'; // Import the secure storage class

class TimeTable extends StatefulWidget {
  const TimeTable({Key? key}) : super(key: key);
  @override
  _TimeTable createState() => _TimeTable();
}

class _TimeTable extends State<TimeTable> {
  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();
  List week = ['월', '화', '수', '목', '금'];
  var kColumnLength = 22;
  double kFirstColumnHeight = 40;
  double kBoxSize = 90;
  int semester = 2024010;
  Codec<String, String> stringToBase64 = utf8.fuse(base64);
  // final storage = FlutterSecureStorage();

  var url = 'http://127.0.0.1:8000/lecture/takes';

  // Future<Takes?> get_timetable() async {
  //   try {
  //     var request = Uri.parse("$url/$semester");
  //     // var token = await storage.read(key: 'token');
  //     var token = await SecureStorage.getToken();
  //     // convert token to base64
  //     // printToken();

  //     final response =
  //         await http.get(request, headers: {"Authorization": "Token $token"});

  //     var tmp = jsonDecode(utf8.decode(response.bodyBytes));
  //     Takes takes = Takes.fromJsonlist(tmp);
  //     if (response.statusCode == 200) {
  //       // Assuming 'Home' is your home widget after login success
  //       return takes;
  //     } else {
  //       Fluttertoast.showToast(
  //           msg: "로그인 실패",
  //           toastLength: Toast.LENGTH_SHORT,
  //           gravity: ToastGravity.CENTER,
  //           timeInSecForIosWeb: 1,
  //           backgroundColor: Colors.red,
  //           textColor: Colors.white,
  //           fontSize: 16.0);
  //       return null;
  //     }
  //   } catch (e) {
  //     print(e);
  //     Fluttertoast.showToast(
  //         msg: "네트워크 오류",
  //         toastLength: Toast.LENGTH_SHORT,
  //         gravity: ToastGravity.CENTER,
  //         timeInSecForIosWeb: 1,
  //         backgroundColor: Colors.red,
  //         textColor: Colors.white,
  //         fontSize: 16.0);
  //     return null;
  //   }
  // }

  @override
  initState() {
    // TODO: implement initState
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    List<List<Widget>> lecturesForTheDay = new List.generate(5, (index) => []);

    for (Take lecture in takes.cousrses_takes) {
      if (lecture.course.semester != semester) continue;
      if (lecture.course.start_time == null) continue;
      if (lecture.course.day == null) continue;
      double top =
          kFirstColumnHeight + (lecture.course.start_time! / 60.0) * kBoxSize;
      double height =
          ((lecture.course.end_time! - lecture.course.start_time!) / 60.0) *
              kBoxSize;

      for (int i = 0; i < lecture.course.day!.length; i++) {
        var v = int.parse(lecture.course.day![i]) - 1;
        if (v >= 0 && v < 5) {
          lecturesForTheDay[v].add(
            Positioned(
              top: top,
              left: 0,
              child: Stack(children: [
                Container(
                  width: MediaQuery.of(context).size.width / 5,
                  height: height,
                  decoration: const BoxDecoration(
                    color: Colors.blue,
                    borderRadius: BorderRadius.all(Radius.circular(2)),
                  ),
                  child: Text(
                    "${lecture.course.name}\n${lecture.course.classroom}",
                    style: const TextStyle(color: Colors.white, fontSize: 12),
                  ),
                ),
              ]),
            ),
          );
        }
      }
    }

    return SingleChildScrollView(
        child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        DropdownButton<String>(
          value: semester.toString(),
          icon: const Icon(Icons.arrow_downward),
          elevation: 16,
          style: const TextStyle(color: Colors.deepPurple),
          underline: Container(
            height: 2,
            color: Colors.deepPurpleAccent,
          ),
          onChanged: (String? value) {
            // This is called when the user selects an item.
            setState(() {
              semester = int.parse(value!);
            });
          },
          items: takes.semesters
              .toList()
              .map<DropdownMenuItem<String>>((int value) {
            return DropdownMenuItem<String>(
              value: value.toString(),
              child: Text(value.toString()),
            );
          }).toList(),
        ),
        SizedBox(
          height: (kColumnLength / 2 * kBoxSize) + kFirstColumnHeight,
          child: Row(
            children: [
              buildTimeColumn(),
              ...buildDayColumn(0, lecturesForTheDay[0]),
              ...buildDayColumn(1, lecturesForTheDay[1]),
              ...buildDayColumn(2, lecturesForTheDay[2]),
              ...buildDayColumn(3, lecturesForTheDay[3]),
              ...buildDayColumn(4, lecturesForTheDay[4]),
            ],
          ),
        ),
      ],
    ));
  }

  Expanded buildTimeColumn() {
    return Expanded(
      child: Column(
        children: [
          SizedBox(
            height: kFirstColumnHeight,
          ),
          ...List.generate(
            kColumnLength.toInt(),
            (index) {
              if (index % 2 == 0) {
                return const Divider(
                  color: Colors.black,
                  height: 0,
                );
              }
              return SizedBox(
                height: kBoxSize,
                child: Center(child: Text('${index ~/ 2 + 9}')),
              );
            },
          ),
        ],
      ),
    );
  }

  List<Widget> buildDayColumn(int index, List<Widget> lecturesForTheDay) {
    return [
      const VerticalDivider(
        color: Colors.black,
        width: 0,
      ),
      Expanded(
        flex: 4,
        child: Stack(
          children: [
            Column(
              children: [
                SizedBox(
                    height: kFirstColumnHeight,
                    child: Center(
                      child: Text(
                        '${week[index]}',
                      ),
                    )),
                ...List.generate(
                  kColumnLength.toInt(),
                  (index) {
                    if (index % 2 == 0) {
                      return const Divider(
                        color: Colors.black,
                        height: 0,
                      );
                    }
                    return SizedBox(
                      height: kBoxSize,
                      child: Container(),
                    );
                  },
                ),
              ],
            ),
            ...lecturesForTheDay, // 현재 요일에 해당하는 모든 강의를 Stack에 추가
          ],
        ),
      ),
    ];
  }
}
