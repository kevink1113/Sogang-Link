import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:async';
import 'dart:math';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);
  @override
  _HomePage createState() => _HomePage();
}

class _HomePage extends State<HomePage> {
  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    var screenwidth = MediaQuery.of(context).size.width;
    // TODO: implement build

    return Scaffold(
        key: scaffoldKey,
        backgroundColor: Colors.white,
        //
        appBar: AppBar(
          title: const Center(
            child: Text(
              'Sogang Link',
              textAlign: TextAlign.center,
              style: TextStyle(
                color: Colors.white, // Set text color to white
              ),
            ),
          ),
          backgroundColor: Colors.redAccent,
        ),
        body: SingleChildScrollView(
          child: Column(
            children: [
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
        ),
        bottomNavigationBar: const BottomAppBar(
          height: 68,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              Flexible(
                flex: 1,
                child: Column(
                  children: [
                    Icon(Icons.dehaze),
                    Text('기능'),
                  ],
                ),
              ),
              Flexible(
                flex: 1,
                child: Column(
                  children: [
                    Icon(Icons.date_range),
                    Text('시간표'),
                  ],
                ),
              ),
              Flexible(
                flex: 1,
                child: Column(
                  children: [
                    Icon(Icons.home),
                    Text('홈'),
                  ],
                ),
              ),
              Flexible(
                flex: 1,
                child: Column(
                  children: [
                    Icon(Icons.mode_comment),
                    Text('게시판'),
                  ],
                ),
              ),
              Flexible(
                flex: 1,
                child: Column(
                  children: [
                    Icon(Icons.settings),
                    Text('설정'),
                  ],
                ),
              ),
            ],
          ),
        ));
  }
}
