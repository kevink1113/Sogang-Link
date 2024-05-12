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
  final GlobalKey _containerkey = GlobalKey();
  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();
  List week = ['월', '화', '수', '목', '금'];
  var kColumnLength = 22;
  double kFirstColumnHeight = 40;
  double kBoxSize = 70;
  int semester = 2024010;
  Codec<String, String> stringToBase64 = utf8.fuse(base64);
  Color c = Colors.primaries[Random().nextInt(Colors.primaries.length)];
  List<Color> cs = [
    Colors.red,
    Colors.yellow,
    Colors.blue,
    Colors.purple,
    Colors.orange,
    Colors.red,
    Colors.red,
    Colors.red,
    Colors.red,
  ];

  @override
  initState() {
    // TODO: implement initState

    super.initState();
  }

  Size? _getSize() {
    if (_containerkey.currentContext != null) {
      final RenderBox renderBox =
          _containerkey.currentContext!.findRenderObject() as RenderBox;
      Size size = renderBox.size;
      return size;
    }
  }

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    List<List<Widget>> lecturesForTheDay = new List.generate(5, (index) => []);
    int count = 0;
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
                InkWell(
                  onTap: () => showModalBottomSheet<void>(
                      showDragHandle: true,
                      backgroundColor: Colors.white,
                      context: context,
                      builder: (BuildContext context) {
                        return Container(
                          height: 200,
                          // decoration: BoxDecoration(
                          //   color: Colors.transparent,
                          //   borderRadius: BorderRadius.only(
                          //     topLeft: Radius.circular(20.0),
                          //     topRight: Radius.circular(20.0),
                          //   ),
                          // ),
                          child: Center(
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              crossAxisAlignment: CrossAxisAlignment.start,
                              mainAxisSize: MainAxisSize.min,
                              children: <Widget>[
                                Text("과목: ${lecture.course.name}",
                                    style: TextStyle(
                                      fontSize: 16,
                                    )),
                                Text("교수명: ${lecture.course.advisor}",
                                    style: TextStyle(
                                      fontSize: 16,
                                    )),
                                Text("교실: ${lecture.course.classroom}",
                                    style: TextStyle(
                                      fontSize: 16,
                                    )),
                                (lecture.final_grade != null)
                                    ? Text("성적: ${lecture.final_grade}",
                                        style: TextStyle(
                                          fontSize: 16,
                                        ))
                                    : Text(" ")
                              ],
                            ),
                          ),
                        );
                      }),
                  child: Container(
                    width: MediaQuery.of(context).size.width / 5,
                    height: height,
                    decoration: BoxDecoration(
                      color: cs[count % (cs.length)],
                      borderRadius: BorderRadius.all(Radius.circular(5)),
                    ),
                    child: Text(
                      "${lecture.course.name}\n${lecture.course.classroom}",
                      style: const TextStyle(color: Colors.black, fontSize: 12),
                    ),
                  ),
                )
              ]),
            ),
          );
        }
      }
      count++;
    }

    return SingleChildScrollView(
        child: Column(
      key: _containerkey,
      mainAxisSize: MainAxisSize.min,
      children: [
        Wrap(
          spacing: 8.0, // Horizontal space between chips
          runSpacing: 4.0, // Vertical space between chip rows
          children: takes.semesters.toList().map<Widget>((int value) {
            return ChoiceChip(
              label: Text(
                value.toString(),
                style: TextStyle(
                  color:
                      semester == value ? Colors.white : Colors.grey.shade800,
                ),
              ),
              selected: semester == value,
              onSelected: (bool selected) {
                setState(() {
                  if (selected) {
                    semester = value;
                  }
                });
              },
              backgroundColor:
                  semester == value ? Color(0xFF9e2a2f) : Colors.grey.shade300,
              selectedColor: Color(0xFF9e2a2f),
              padding: EdgeInsets.symmetric(horizontal: 10.0, vertical: 10.0),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(20),
              ),
              elevation: 8,
              avatar:
                  null, // Explicitly remove any avatar, such as a check mark
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
