import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:soganglink/data/courses/takes.dart';
import 'package:soganglink/data/login/User.dart';
import 'package:soganglink/login.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);
  @override
  _HomePage createState() => _HomePage();
}

class _HomePage extends State<HomePage> {
  List<Widget> courses = [];
  int semester = 2024010;
  @override
  void initState() {
    // TODO: implement initState
    super.initState();

    if (takes != null) {
      for (Take lecture in takes.cousrses_takes) {
        if (lecture.course.semester != semester) continue;
        courses.add(Text(lecture.course.name));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return SingleChildScrollView(
      child: Column(
        children: [
          InkWell(
            child: Container(
                //모바일 학생증
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  color: Colors.white, // Container의 배경색
                  borderRadius: BorderRadius.circular(20), // 둥근 모서리 반경 설정
                  // border: Border.all(
                  //   color: Colors.blue, // 테두리 색상
                  //   width: 2, // 테두리 두께
                  // ),
                ),
                height: 300,
                margin: EdgeInsets.fromLTRB(20, 30, 20, 10),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    Flexible(
                        flex: 1,
                        child: ClipRRect(
                            borderRadius: BorderRadius.circular(20.0),
                            child: Image.asset(
                              "assets/images/sample.jpg",
                              height: 200,
                              width: 200,
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
            onTap: () {
              showModalBottomSheet<void>(
                  context: context,
                  builder: (BuildContext context) {
                    return Container(
                      height: 500,
                      color: Colors.white,
                      child: Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          mainAxisSize: MainAxisSize.min,
                          children: <Widget>[
                            QrImageView(
                              data: user.username,
                              version: QrVersions.auto,
                              size: 300.0,
                            ),
                          ],
                        ),
                      ),
                    );
                  });
            },
          ),
          Container(
              alignment: Alignment(-0.95, -1.0),
              decoration: BoxDecoration(
                color: Colors.white, // Container의 배경색
                borderRadius: BorderRadius.circular(20), // 둥근 모서리 반경 설정
                // border: Border.all(
                //   color: Colors.blue, // 테두리 색상
                //   width: 2, // 테두리 두께
                // ),
              ),
              margin: EdgeInsets.fromLTRB(20, 20, 20, 30),
              child: Padding(
                padding: EdgeInsets.fromLTRB(0, 10, 0, 10),
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
                    Column(
                      children: courses,
                      crossAxisAlignment: CrossAxisAlignment.start,
                    )
                  ],
                ),
              )),
          Container(
            alignment: Alignment.center,
            decoration: BoxDecoration(
              color: Colors.white, // Container의 배경색
              borderRadius: BorderRadius.circular(20), // 둥근 모서리 반경 설정
              // border: Border.all(
              //   color: Colors.blue, // 테두리 색상
              //   width: 2, // 테두리 두께
              // ),
            ),
            height: 500,
            margin: EdgeInsets.fromLTRB(20, 30, 20, 30),
            child: Center(
              child: Text(
                '둥글고 테두리 색상',
                style: TextStyle(
                  fontSize: 18,
                  color: Colors.black,
                ),
              ),
            ),
          ),
          Container(
            alignment: Alignment.center,
            decoration: BoxDecoration(
              color: Colors.white, // Container의 배경색
              borderRadius: BorderRadius.circular(20), // 둥근 모서리 반경 설정
              // border: Border.all(
              //   color: Colors.blue, // 테두리 색상
              //   width: 2, // 테두리 두께
              // ),
            ),
            height: 500,
            margin: EdgeInsets.fromLTRB(20, 10, 20, 10),
            child: Center(
              child: Text(
                '둥글고 테두리 색상',
                style: TextStyle(
                  fontSize: 18,
                  color: Colors.black,
                ),
              ),
            ),
          )
        ],
      ),
    );
  }
}
