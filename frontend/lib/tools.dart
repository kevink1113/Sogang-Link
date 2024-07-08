import 'package:flutter/material.dart';
import 'package:soganglink/tools/calcgrade.dart';
import 'package:soganglink/tools/restaurant/search_tag.dart';
import 'package:soganglink/tools/studyroom.dart';

class Tools extends StatefulWidget {
  const Tools({Key? key}) : super(key: key);
  @override
  _Tools createState() => _Tools();
}

class _Tools extends State<Tools> {
  @override
  void initState() {
    // TODO: implement initState
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    void initState() {
      // TODO: implement initState
      super.initState();
    }

    // TODO: implement build
    return Container(
        alignment: const Alignment(-0.95, -1.0),
        decoration: BoxDecoration(
          color: Colors.white, // Container의 배경색
          borderRadius: BorderRadius.circular(20), // 둥근 모서리 반경 설정
          // border: Border.all(
          //   color: Colors.blue, // 테두리 색상
          //   width: 2, // 테두리 두께
          // ),
        ),
        margin: const EdgeInsets.fromLTRB(20, 20, 20, 30),
        child: Padding(
          padding: const EdgeInsets.fromLTRB(10, 10, 10, 10),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              InkWell(
                child: const Center(
                    child: Text(
                  "성적계산기",
                  style: TextStyle(
                    color: Colors.black,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 2.0,
                  ),
                )),
                onTap: () {
                  Navigator.push(
                      context, MaterialPageRoute(builder: (_) => const CalcGrade()));
                },
              ),
              InkWell(
                child: const Center(
                    child: Text(
                      "열람실 현황",
                      style: TextStyle(
                        color: Colors.black,
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        letterSpacing: 2.0,
                      ),
                    )),
                onTap: () {
                  Navigator.push(
                      context, MaterialPageRoute(builder: (_) => const StudyroomStatus()));
                },
              ),
              InkWell(
                child: const Center(
                    child: Text(
                      "음식점 검색",
                      style: TextStyle(
                        color: Colors.black,
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        letterSpacing: 2.0,
                      ),
                    )),
                onTap: () {
                  Navigator.push(
                      context, MaterialPageRoute(builder: (_) => const SearchTag()));
                },
              )
            ],
          ),
        ));
  }
}
