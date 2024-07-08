import 'dart:convert';
import 'dart:math';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:soganglink/board/post.dart';
import 'package:soganglink/board/writepost.dart';
import 'package:soganglink/data/board/postlist.dart';
import 'package:soganglink/storage.dart';
import 'package:http/http.dart' as http;

import '../login.dart';

class Board extends StatefulWidget {
  const Board({Key? key}) : super(key: key);

  @override
  _Board createState() => _Board();
}

class _Board extends State<Board> {
  List<DataRow> courses = [];
  int semester = 2024010;
  late PostList post;
  bool loaded = false;

  void ReloadList() {
    var request = Uri.parse("$url/posts/");
    try {
      SecureStorage.getToken().then((token) {
        try {
          http.get(request, headers: {"Authorization": "Token $token"}).then(
              (response) {
            if (response.statusCode == 200) {
              setState(() {
                post = PostList.fromJsonlist(
                    jsonDecode(utf8.decode(response.bodyBytes)));
                loaded = true;
              });
            } else {
              print("게시판 가져오기 실패");
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
  void initState() {
    super.initState();

    ReloadList();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      alignment: Alignment.topLeft,
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
      ),
      padding: const EdgeInsets.fromLTRB(20, 10, 20, 10),
      margin: const EdgeInsets.fromLTRB(20, 20, 20, 30),
      child: (loaded)
          ? (Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Padding(
                  padding: const EdgeInsets.only(bottom: 10.0),
                  child: Row(
                    children: [
                      const Text(
                        "자유게시판",
                        textAlign: TextAlign.left,
                        style: TextStyle(
                          color: Colors.black,
                          fontSize: 30,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      IconButton(
                        icon: const Icon(Icons.refresh),
                        onPressed: () {
                          setState(() {
                            loaded = false;
                          });
                          ReloadList();
                        },
                      ),
                    ],
                  ),
                ),
                Expanded(
                  child: ListView.builder(
                    itemCount: min(post.postList.length, 20),
                    itemBuilder: ((context, index) {
                      return Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          ListTile(
                            contentPadding: EdgeInsets.zero,
                            title: RichText(
                              textAlign: TextAlign.left,
                              text: TextSpan(
                                text: post.postList[index].title,
                                style: const TextStyle(
                                  fontSize: 18,
                                  color: Colors.black,
                                  overflow: TextOverflow.ellipsis,
                                ),
                                recognizer: TapGestureRecognizer()
                                  ..onTap = () {
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (context) => PostDetail(
                                          id: post.postList[index].id,
                                          title: post.postList[index].title,
                                          author: post.postList[index].author,
                                          date: post.postList[index].date,
                                          content: post.postList[index].content,
                                        ),
                                      ),
                                    ).then((_) {
                                      // 수정 후 게시글들 다시 로드
                                      ReloadList();
                                    });
                                  },
                              ),
                              maxLines: 1,
                            ),
                            trailing: Column(
                              crossAxisAlignment: CrossAxisAlignment.end,
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Text(
                                  post.postList[index].author,
                                  style: const TextStyle(
                                    fontSize: 14,
                                    color: Colors.grey,
                                  ),
                                ),
                                Text(
                                  post.postList[index].date.toString(),
                                  style: const TextStyle(
                                    fontSize: 12,
                                    color: Colors.grey,
                                  ),
                                ),
                              ],
                            ),
                          ),
                          Divider(
                            color: Colors.grey.shade300,
                          ),
                        ],
                      );
                    }),
                  ),
                ),
                Align(
                  alignment: Alignment.bottomRight,
                  child: FloatingActionButton(
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (context) => const PostCreate()),
                      ).then((_) {
                        // 수정 후 게시글들 다시 로드
                        ReloadList();
                      });
                    },
                    child: const Icon(Icons.add),
                  ),
                )
              ],
            ))
          : const Center(child: Text('로딩중')),
    );
  }
}
