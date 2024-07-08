import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:soganglink/login.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:http/http.dart' as http;

import '../storage.dart';

class StudyroomStatus extends StatefulWidget {
  const StudyroomStatus({Key? key}) : super(key: key);

  @override
  _StudyroomStatus createState() => _StudyroomStatus();
}

class _StudyroomStatus extends State<StudyroomStatus> {
  final List<Map<String, dynamic>> readingRooms = [];

  final Map<dynamic, int> roomsnumber = {
    "111 일반열람실": 2,
    "112 일반열람실": 3,
    "113 일반열람실": 4,
    "133 일반열람실": 5,
    "K관 열람실": 6,
    "X관 대학원열람실": 8,
    "PA관 열람실": 11,
    "J관 일반열람실": 15,
    "J관 노트북전용실": 16,
  };

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
                if (roomsnumber.containsKey(json["name"])) {
                  readingRooms.add({
                    "name": json["name"],
                    "totalSeats": json["total_seats"],
                    "availableSeats": json["available_seats"]
                  });
                }
              }
              setState(() {});
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
        title: const Text('열람실 좌석 정보'),
        actions: [
          IconButton(
            icon: const Icon(Icons.info_outline),
            onPressed: () {
              _launchDetailsURL('http://libseat.sogang.ac.kr/seat/domian5.asp');
            },
          ),
        ],
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(8.0),
        itemCount: readingRooms.length,
        itemBuilder: (context, index) {
          final room = readingRooms[index];
          final availableSeats = room["availableSeats"];
          final totalSeats = room["totalSeats"];
          final percentage = availableSeats / totalSeats;

          return Card(
              margin: const EdgeInsets.symmetric(vertical: 8.0),
              child: InkWell(
                onTap: () {
                  _launchDetailsURL(
                      'http://libseat.sogang.ac.kr/seat/roomview5.asp?room_no=${roomsnumber[room["name"]]}');
                },
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        room["name"],
                        style: const TextStyle(
                          fontSize: 18.0,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 8.0),
                      Text("남은 좌석: $availableSeats / $totalSeats"),
                      const SizedBox(height: 8.0),
                      LinearProgressIndicator(
                        value: percentage,
                        backgroundColor: Colors.grey.shade300,
                        valueColor: AlwaysStoppedAnimation<Color>(
                          percentage > 0.5
                              ? Colors.green
                              : (percentage > 0.2 ? Colors.orange : Colors.red),
                        ),
                      ),
                      const SizedBox(height: 8.0),
                      Text("${(percentage * 100).toStringAsFixed(1)}% 남음"),
                    ],
                  ),
                ),
              ));
        },
      ),
    );
  }

  void _launchDetailsURL(String link) async {
    Uri url = Uri.parse(link);
    if (await canLaunchUrl(url)) {
      await launchUrl(url);
    } else {
      throw 'Could not launch $url';
    }
  }
}
