import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

void main() async {
  print('Enter your question:');
  final question = stdin.readLineSync();

  if (question != null && question.isNotEmpty) {
    // Replace this with your actual token
    const token = '527faebec62c87affb7cf30e38d3e8beac327a41';
    await GPTstreamcall(token, question);
  } else {
    print('Question cannot be empty.');
  }
}

Future<void> GPTstreamcall(String token, String question) async {
  try {
    final client = http.Client();
    final request =
        http.Request('POST', Uri.parse("http://34.64.245.20:8000/chat"));

    Map<String, String> bodyMap = {'question': question};
    request.body = jsonEncode(bodyMap);
    request.headers['Authorization'] = 'Token $token';
    request.headers['Content-type'] = 'application/json';

    final response = await client.send(request);

    if (response.statusCode != 200) {
      print(
          'Failed to connect to the server. Status code: ${response.statusCode}');
      return;
    }

    print('Connected to the server. Streaming response:');
    // Stream data handling
    response.stream.transform(utf8.decoder).listen((data) {
      // Print raw data for debugging
      // print('Raw data: $data');
      data.split('\n').forEach((line) {
        if (line.startsWith("data: ")) {
          final raw = line.substring(6).trim();
          if (raw.isNotEmpty && raw != '[DONE]' && raw != 'run_completed') {
            try {
              final decoded = json.decode(raw) as Map<String, dynamic>;
              final text = decoded['text'];
              if (text != null && text.isNotEmpty) {
                stdout.write(
                    text); // Print each piece of the response as it arrives
              }
            } catch (e) {
              print('Error decoding JSON: $e');
            }
          }
        }
      });
    }, onDone: () {
      print("\nStream closed");
    }, onError: (error) {
      print("\nStream error: $error");
    });
  } catch (e) {
    print("\ngpt error: $e");
  }
}
