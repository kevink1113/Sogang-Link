// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'dart:convert';

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

  final response = await http.get(request, headers: {
    "Authorization": "Token 5a86a49483e688b51fbcf244a382483f93d71127"
  });
  var t = jsonDecode(response.body);

  print(t);
}
