import 'package:flutter/material.dart';
import 'package:soganglink/data/board/commentlist.dart';
import 'package:soganglink/storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import '../login.dart';

class PostDetail extends StatefulWidget {
  final int id;
  final String title;
  final String author;
  final DateTime date;
  final String? content;

  const PostDetail({
    Key? key,
    required this.id,
    required this.title,
    required this.author,
    required this.date,
    required this.content,
  }) : super(key: key);

  @override
  _PostDetailState createState() => _PostDetailState();
}

class _PostDetailState extends State<PostDetail> {
  final TextEditingController _commentController = TextEditingController();
  late CommentList commentlist;
  bool isloaded = false;

  void LoadComments() {
    isloaded = false;
    try {
      SecureStorage.getToken().then((token) {
        try {
          http.get(Uri.parse("$url/posts/${widget.id}/comments"),
              headers: {"Authorization": "Token $token"}).then((response) {
            if (response.statusCode == 200) {
              commentlist = CommentList.fromJsonlist(
                  jsonDecode(utf8.decode(response.bodyBytes)));
              setState(() {
                isloaded = true;
              });
            } else {
              print("댓글 가져오기 실패");
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

  void _submitComment() {
    if (!_commentController.text.isEmpty) {
      var request = Uri.parse("$url/posts/${widget.id}/comments");
      try {
        SecureStorage.getToken().then((token) {
          try {
            http.post(request, headers: {
              "Authorization": "Token $token"
            }, body: {
              "post": widget.id,
              "author": user.username, // 학번
              "content": _commentController.text
            }).then((response) {
              print(response);
              if (response.statusCode == 201) {
                LoadComments();
              } else {
                print("댓글쓰기 실패 실패");
                print(utf8.decode(response.bodyBytes));
              }
            });
          } catch (e) {
            print("네트워크 오류");
          }
        });
      } catch (e) {
        print(e);
        print("asdfasdf");
      }
      return;
    }
  }

  @override
  void initState() {
    super.initState();
    LoadComments();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("게시글 상세"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              widget.title,
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 10),
            Text(
              "글쓴이: ${widget.author}",
              style: TextStyle(fontSize: 16, color: Colors.grey),
            ),
            Text(
              "날짜: ${widget.date.toString()}",
              style: TextStyle(fontSize: 16, color: Colors.grey),
            ),
            SizedBox(height: 20),
            (widget.content != null)
                ? Text(
                    widget.content!,
                    style: TextStyle(fontSize: 18),
                  )
                : Text(
                    "내용이 없습니다.",
                    style: TextStyle(fontSize: 18),
                  ),
            SizedBox(height: 20),
            Text(
              "댓글",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            Divider(color: Colors.grey),
            TextField(
              controller: _commentController,
              decoration: InputDecoration(
                border: OutlineInputBorder(),
              ),
              maxLines: 3,
            ),
            SizedBox(height: 5),
            Align(
              alignment: Alignment.centerRight,
              child: ElevatedButton(
                onPressed: _submitComment,
                child: Text("댓글 달기"),
              ),
            ),
            Expanded(
                child: (isloaded)
                    ? ListView.builder(
                        itemCount: commentlist.commentlist.length,
                        itemBuilder: (context, index) {
                          return Padding(
                            padding: const EdgeInsets.symmetric(vertical: 8.0),
                            child: Row(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                CircleAvatar(
                                  radius: 15,
                                  backgroundColor: Colors.grey,
                                  child: Text(
                                    commentlist.commentlist[index].author[0],
                                    style: TextStyle(
                                      color: Colors.white,
                                    ),
                                  ),
                                ),
                                SizedBox(width: 10),
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        commentlist.commentlist[index].author,
                                        style: TextStyle(
                                          fontSize: 14,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                      (commentlist.commentlist[index].content !=
                                              null)
                                          ? Text(
                                              commentlist
                                                  .commentlist[index].content!,
                                              style: TextStyle(
                                                fontSize: 14,
                                              ),
                                            )
                                          : Text(
                                              "내용 없음",
                                              style: TextStyle(
                                                fontSize: 14,
                                              ),
                                            )
                                    ],
                                  ),
                                ),
                              ],
                            ),
                          );
                        },
                      )
                    : Text("댓글 로딩중")),
          ],
        ),
      ),
    );
  }
}
