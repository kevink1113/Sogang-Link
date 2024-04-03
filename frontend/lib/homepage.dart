import 'package:flutter/material.dart';
import 'package:flutter/services.dart';



class HomePage extends StatefulWidget{
  const HomePage({Key? key}) : super(key:key);
  @override
  _HomePage createState() => _HomePage();
}


class _HomePage extends State<HomePage>{
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
        children: [
          Container( //모바일 학생증
              alignment: Alignment.center,
              decoration: BoxDecoration(
                color: Colors.white, // Container의 배경색
                borderRadius: BorderRadius.circular(20), // 둥근 모서리 반경 설정
                border: Border.all(
                  color: Colors.blue, // 테두리 색상
                  width: 2, // 테두리 두께
                ),
              ),
              height: 300,
              margin: EdgeInsets.fromLTRB(40, 30, 40, 10),
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
                          )
                      )
                  ),
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
                          Text("이름: "),
                          Text("소속: "),
                          Text("학번: "),
                        ],
                      )
                  )
                ],
              )
          ),
          Container(
              alignment: Alignment(-0.95,-1.0),
              decoration: BoxDecoration(
                color: Colors.white, // Container의 배경색
                borderRadius: BorderRadius.circular(20), // 둥근 모서리 반경 설정
                border: Border.all(
                  color: Colors.blue, // 테두리 색상
                  width: 2, // 테두리 두께
                ),
              ),
              margin: EdgeInsets.fromLTRB(40, 20, 40, 30),
              child: Padding(
                padding: EdgeInsets.fromLTRB(0, 10, 0, 10),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "공지",
                      style: TextStyle(
                        color: Colors.black,
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        letterSpacing: 2.0,
                      ),
                    ),
                    Text("A"),
                    Text("B"),
                    Text("C"),
                  ],
                ),
              )
          ),
          Container(
            alignment: Alignment.center,
            decoration: BoxDecoration(
              color: Colors.white, // Container의 배경색
              borderRadius: BorderRadius.circular(20), // 둥근 모서리 반경 설정
              border: Border.all(
                color: Colors.blue, // 테두리 색상
                width: 2, // 테두리 두께
              ),
            ),
            height: 500,
            margin: EdgeInsets.fromLTRB(40, 30, 40, 30),
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
              border: Border.all(
                color: Colors.blue, // 테두리 색상
                width: 2, // 테두리 두께
              ),
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
