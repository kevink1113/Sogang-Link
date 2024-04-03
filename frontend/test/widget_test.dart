// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:soganglink/home.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import '../lib/data/login/User.dart';
import 'package:fluttertoast/fluttertoast.dart';

Future<void> main() async {
  final String url = "http://127.0.0.1:8000/login/";
  var request = Uri.parse(url);

  final response =
      await http.post(request, body: {"username": "20191560", "password": ""});

  print(response);
}
