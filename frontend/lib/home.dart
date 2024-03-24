import 'package:flutter/material.dart';

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
          backgroundColor: const Color(0xff9e2a2f),
        ),
        body: const SingleChildScrollView(
          child: Column(
            children: [
              Text('asdfa'),
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
    throw UnimplementedError();
  }
}
