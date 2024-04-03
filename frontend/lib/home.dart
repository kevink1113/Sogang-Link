import 'package:flutter/material.dart';
import 'package:soganglink/homepage.dart';
import 'package:soganglink/timetable.dart';

class Home extends StatefulWidget {
  const Home({Key? key}) : super(key: key);

  @override
  _HomeState createState() => _HomeState();
}

class _HomeState extends State<Home> {
  int _selectedIndex = 2;
  final List<Widget> _pages = [
    const HomePage(),
    const TimeTable(),
    const HomePage(), // 게시판 페이지 예시로 임시로 HomePage 사용
    const HomePage(), // 설정 페이지 예시로 임시로 HomePage 사용
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey.shade200, // 밝은 회색으로 배경색 설정
      appBar: AppBar(
        title: const Text(
          'Sogang Link',
          style: TextStyle(color: Colors.white),
        ),
        backgroundColor: Colors.redAccent, // AppBar 색상 변경
        elevation: 0, // AppBar 그림자 제거
        centerTitle: true, // 제목 중앙 정렬
      ),
      body: IndexedStack(
        index: _selectedIndex,
        children: _pages,
      ),
      bottomNavigationBar: BottomNavigationBar(
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.dehaze),
            label: '기능',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.date_range),
            label: '시간표',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: '홈',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.mode_comment),
            label: '게시판',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.settings),
            label: '설정',
          ),
        ],
        currentIndex: _selectedIndex,
        selectedItemColor: Colors.red[300], // 선택된 아이템 색상 변경
        onTap: _onItemTapped,
        type: BottomNavigationBarType.fixed, // 4개 이상의 아이템에도 배경색 유지
        backgroundColor: Colors.white, // BottomNavigationBar 배경색 변경
        unselectedItemColor: Colors.grey, // 선택되지 않은 아이템 색상 변경
        elevation: 10.0, // BottomNavigationBar 그림자 추가
      ),
    );
  }
}
