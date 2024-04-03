import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:async';
import 'dart:math';


class TimeTable extends StatefulWidget{
  const TimeTable({Key? key}) : super(key:key);
  @override
  _TimeTable createState() => _TimeTable();
}


class _TimeTable extends State<TimeTable> {
  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();
  List week = ['월', '화', '수', '목', '금'];
  var kColumnLength = 22;
  double kFirstColumnHeight = 40;
  double kBoxSize = 90;


  @override
  void initState() {
    // TODO: implement initState
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return SingleChildScrollView(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          SizedBox(
            height: (kColumnLength / 2 * kBoxSize) + kFirstColumnHeight,
            child: Row(
              children: [
                buildTimeColumn(),
                ...buildDayColumn(0),
                ...buildDayColumn(1),
                ...buildDayColumn(2),
                ...buildDayColumn(3),
                ...buildDayColumn(4),
              ],
            ),
          ),
        ],
      )
    );
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

  List<Widget> buildDayColumn(int index) {
    String currentDay = week[index];
    List<Widget> lecturesForTheDay = [];
/*
    for (var lecture in selectedLectures) {
      for (int i = 0; i < lecture.day.length; i++) {
        double top = kFirstColumnHeight + (lecture.start[i] / 60.0) * kBoxSize;
        double height = ((lecture.end[i] - lecture.start[i]) / 60.0) * kBoxSize;

        if (lecture.day[i] == currentDay) {
          lecturesForTheDay.add(
            Positioned(
              top: top,
              left: 0,
              child: Stack(children: [
                GestureDetector(
                  onTap: () {
                    setState(() {
                      selectedLectures.remove(lecture);
                      setTimetableLength();
                    });
                  },
                  child: Container(
                    width: MediaQuery.of(context).size.width / 5,
                    height: height,
                    decoration: const BoxDecoration(
                      color: Colors.blue,
                      borderRadius: BorderRadius.all(Radius.circular(2)),
                    ),
                    child: Text(
                      "${lecture.lname}\n${lecture.classroom[i]}",
                      style: const TextStyle(color: Colors.white, fontSize: 12),
                    ),
                  ),
                ),
              ]),
            ),
          );
        }
      }
    }*/

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
                  )
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