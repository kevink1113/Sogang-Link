import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:soganglink/homepage.dart';

import 'package:soganglink/timetable.dart';

class Home extends StatefulWidget {
  const Home({Key? key}) : super(key: key);
  @override
  _Home createState() => _Home();
}

class _Home extends State<Home> {
  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();
  Widget bodyPage = const HomePage();
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    // TODO: implement build

    return Scaffold(
        key: scaffoldKey,
        backgroundColor: Colors.grey,
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
        body: bodyPage,
        bottomNavigationBar: BottomAppBar(
          height: 50,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              Flexible(
                child: Column(
                  children: [
                    Icon(Icons.dehaze),
                    Text('기능'),
                  ],
                ),
                flex: 1,
              ),
              Flexible(
                child: InkWell(
                  onTap: () {
                    setState(() {
                      bodyPage = const TimeTable();
                    });
                  },
                  child: Column(
                    children: [
                      Icon(Icons.date_range),
                      Text('시간표'),
                    ],
                  ),
                ),
                flex: 1,
              ),
              Flexible(
                child: InkWell(
                  onTap: () {
                    setState(() {
                      bodyPage = const HomePage();
                    });
                  },
                  child: Column(
                    children: [
                      Icon(Icons.home),
                      Text('홈'),
                    ],
                  ),
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
