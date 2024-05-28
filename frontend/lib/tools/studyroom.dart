import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:soganglink/login.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:http/http.dart' as http;

import '../storage.dart';

class StudyroomStatus extends StatefulWidget {
  StudyroomStatus({Key? key}) : super(key: key);

  @override
  _StudyroomStatus createState() => _StudyroomStatus();
}

class _StudyroomStatus extends State<StudyroomStatus> {

  final List<Map<String, dynamic>> readingRooms = [
  ];
  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    try {
      SecureStorage.getToken().then((token) {
        try {
          http.get(Uri.parse("$url/maps/facility"),
              headers: {"Authorization": "Token $token"}).then((response) {
            if (response.statusCode == 200) {
              var status = jsonDecode(utf8.decode(response.bodyBytes));
              for (final Map<String, dynamic> json in status) {
                if(json["name"].indexOf('열람실') != -1){
                  readingRooms.add({"name": json["name"], "totalSeats": json["total_seats"], "availableSeats": json["available_seats"]});
                }
              }
              setState(() {
              });
            } else {
              print("로그인 실패");
            }
          });
        } catch (e) {
          print("네트워크 오류");
        }
      });
    } catch (e) {
      print(e);
    }
  }



  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('열람실 좌석 정보'),
        actions: [
          IconButton(
            icon: Icon(Icons.info_outline),
            onPressed: _launchDetailsURL,
          ),
        ],
      ),
      body: ListView.builder(
        padding: EdgeInsets.all(8.0),
        itemCount: readingRooms.length,
        itemBuilder: (context, index) {
          final room = readingRooms[index];
          final availableSeats = room["availableSeats"];
          final totalSeats = room["totalSeats"];
          final percentage = availableSeats / totalSeats;

          return Card(
            margin: EdgeInsets.symmetric(vertical: 8.0),
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    room["name"],
                    style: TextStyle(
                      fontSize: 18.0,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: 8.0),
                  Text("남은 좌석: $availableSeats / $totalSeats"),
                  SizedBox(height: 8.0),
                  LinearProgressIndicator(
                    value: percentage,
                    backgroundColor: Colors.grey.shade300,
                    valueColor: AlwaysStoppedAnimation<Color>(
                      percentage > 0.5
                          ? Colors.green
                          : (percentage > 0.2 ? Colors.orange : Colors.red),
                    ),
                  ),
                  SizedBox(height: 8.0),
                  Text("${(percentage * 100).toStringAsFixed(1)}% 남음"),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  void _launchDetailsURL() async {
    Uri url = Uri.parse(
        'http://libseat.sogang.ac.kr/seat/domian5.asp'); // 여기에 실제 URL을 넣으세요.
    if (await canLaunchUrl(url)) {
      await launchUrl(url);
    } else {
      throw 'Could not launch $url';
    }
  }
}
