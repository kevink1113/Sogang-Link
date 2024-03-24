import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:async';
import 'dart:math';


class HomePage extends StatefulWidget{
  const HomePage({Key? key}) : super(key:key);
  @override
  _HomePage createState() => _HomePage();
}

class _HomePage extends State<HomePage>{
  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState(){
    super.initState();

  }
  @override
  Widget build(BuildContext context) {
    var screenwidth = MediaQuery.of(context).size.width;
    // TODO: implement build

    return Scaffold(
      key: scaffoldKey,
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Center(
            child: Text(
                'Sogang Link',
              textAlign: TextAlign.center,
            ),
        ),
        backgroundColor: Colors.purple,
      ),
      body: const SingleChildScrollView(
        child: Column(
          children: [
            Text('asdfa'),
          ],
        ),
      ),
      bottomNavigationBar: const BottomAppBar(
        height:50 ,
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
              child: Column(
                children: [
                  Icon(Icons.date_range),
                  Text('시간표'),
                ],
              ),
              flex: 1,
            ),
            Flexible(
              child: Column(
                children: [
                  Icon(Icons.home),
                  Text('홈'),
                ],
              ),
              flex: 1,
            ),
            Flexible(
              child: Column(
                children: [
                  Icon(Icons.mode_comment),
                  Text('게시판'),
                ],
              ),
              flex: 1,
            ),
            Flexible(
              child: Column(
                children: [
                  Icon(Icons.settings),
                  Text('설정'),
                ],
              ),
              flex: 1,
            ),
          ],
        ),
      )
    );
    throw UnimplementedError();
  }
}