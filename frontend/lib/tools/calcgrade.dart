import 'package:flutter/material.dart';

class CalcGrade extends StatefulWidget {
  CalcGrade({Key? key}) : super(key: key);
  @override
  _CalcGrade createState() => _CalcGrade();
}

class _CalcGrade extends State<CalcGrade> {
  @override
  Widget build(BuildContext context) {
    // printToken();
    return Scaffold(
      backgroundColor: Colors.grey.shade200, // 밝은 회색으로 배경색 설정
      appBar: AppBar(
        scrolledUnderElevation: 1.0,
        // leading: IconButton(
        //   icon: Icon(Icons.logout),
        //   onPressed: () {
        //     // Add logout functionality here
        //   },
        // ),
        actions: [
          IconButton(
            icon: const Icon(
              Icons.arrow_back,
              color: Colors.white,
            ),
            onPressed: () {
              Navigator.pop(context);
            },
          ),
        ],

        shadowColor: Colors.black, // AppBar 그림자 색상 변경
        title: Padding(
          padding: const EdgeInsets.only(left: 5.0),
          child: const Text(
            'Sogang Link',
            style: TextStyle(
              color: Colors.white,
              fontSize: 20,
              fontWeight: FontWeight.w600,
              // letterSpacing: 5.0,
            ),
          ),
        ),
        backgroundColor: Color(0xFF9e2a2f), // AppBar 색상 변경
        elevation: 0, // AppBar 그림자 제거
        centerTitle: false, // 제목 중앙 정렬
      ),
    );
  }
}
