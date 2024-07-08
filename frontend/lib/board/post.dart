import 'package:flutter/material.dart';
import 'package:soganglink/board/postedit.dart';
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
  int views = 0;
  int likes = 0;

  void LoadPostDetails() {
    try {
      SecureStorage.getToken().then((token) {
        try {
          http.get(Uri.parse("$url/posts/${widget.id}"),
              headers: {"Authorization": "Token $token"}).then((response) {
            if (response.statusCode == 200) {
              var postDetails = jsonDecode(utf8.decode(response.bodyBytes));
              setState(() {
                views = postDetails['view_count'];
                likes = postDetails['sum_votes'];
              });
            } else {
              print("게시글 상세 정보 가져오기 실패");
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
    if (_commentController.text.isNotEmpty) {
      var request = Uri.parse("$url/posts/${widget.id}/comments");

      try {
        SecureStorage.getToken().then((token) {
          try {
            http.post(request, headers: {
              "Authorization": "Token $token"
            }, body: {
              "post": '${widget.id}',
              "author": user.username,
              "content": _commentController.text
            }).then((response) {
              print(response);
              if (response.statusCode == 201) {
                LoadComments();
              } else {
                print("댓글쓰기 실패");
                print(utf8.decode(response.bodyBytes));
              }
            });
          } catch (e) {
            print("네트워크 오류 $e");
          }
        });
      } catch (e) {
        print(e);
        print("asdfasdf");
      }
      return;
    }
  }

  void _editPost() {
    // 현재 게시글 내용을 포함하여 수정 화면으로 이동
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => EditPostScreen(
          id: widget.id,
          title: widget.title,
          content: widget.content,
        ),
      ),
    ).then((_) {
      // 수정 후 게시글 세부 사항 및 댓글을 다시 로드
      LoadComments();
      LoadPostDetails();
    });
  }

  void _deletePost() {
    SecureStorage.getToken().then((token) {
      try {
        http.delete(Uri.parse("$url/posts/${widget.id}"),
            headers: {"Authorization": "Token $token"}).then((response) {
          if (response.statusCode == 204) {
            Navigator.pop(context); // 이전 화면으로 돌아가기
          } else {
            print("글 삭제 실패: ${utf8.decode(response.bodyBytes)}");
          }
        });
      } catch (e) {
        print("네트워크 오류 $e");
      }
    });
  }

  void _deleteComment(int commentId) {
    SecureStorage.getToken().then((token) {
      try {
        http.delete(Uri.parse("$url/posts/comments/$commentId"),
            headers: {"Authorization": "Token $token"}).then((response) {
          if (response.statusCode == 204) {
            LoadComments();
          } else {
            print("댓글 삭제 실패: ${utf8.decode(response.bodyBytes)}");
          }
        });
      } catch (e) {
        print("네트워크 오류 $e");
      }
    });
  }

  @override
  void initState() {
    super.initState();
    LoadComments();
    LoadPostDetails();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          title: const Text("게시글 상세"),
          actions: (user.username == widget.author)
              ? [
                  IconButton(
                    icon: const Icon(Icons.edit),
                    onPressed: _editPost,
                  ),
                  IconButton(
                    icon: const Icon(Icons.delete),
                    onPressed: _deletePost,
                  )
                ]
              : null),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              widget.title,
              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            Text(
              "글쓴이: ${widget.author}",
              style: const TextStyle(fontSize: 16, color: Colors.grey),
            ),
            Text(
              "날짜: ${widget.date.toString()}",
              style: const TextStyle(fontSize: 16, color: Colors.grey),
            ),
            const SizedBox(height: 10),
            Text(
              "조회수: $views",
              style: const TextStyle(fontSize: 16, color: Colors.grey),
            ),
            Text(
              "추천수: $likes",
              style: const TextStyle(fontSize: 16, color: Colors.grey),
            ),
            const SizedBox(height: 20),
            (widget.content != null)
                ? Text(
                    widget.content!,
                    style: const TextStyle(fontSize: 18),
                  )
                : const Text(
                    "내용이 없습니다.",
                    style: TextStyle(fontSize: 18),
                  ),
            const SizedBox(height: 20),
            const Text(
              "댓글",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const Divider(color: Colors.grey),
            TextField(
              controller: _commentController,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
              ),
              maxLines: 3,
            ),
            const SizedBox(height: 5),
            Align(
              alignment: Alignment.centerRight,
              child: ElevatedButton(
                onPressed: _submitComment,
                child: const Text("댓글 달기"),
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
                                    style: const TextStyle(
                                      color: Colors.white,
                                    ),
                                  ),
                                ),
                                const SizedBox(width: 10),
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        commentlist.commentlist[index].author,
                                        style: const TextStyle(
                                          fontSize: 14,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                      (commentlist.commentlist[index].content !=
                                              null)
                                          ? Row(
                                              children: [
                                                Text(
                                                  commentlist.commentlist[index]
                                                      .content!,
                                                  style: const TextStyle(
                                                    fontSize: 14,
                                                  ),
                                                ),
                                                if (user.username ==
                                                    commentlist
                                                        .commentlist[index]
                                                        .author)
                                                  Expanded(
                                                    child: Align(
                                                      alignment:
                                                          Alignment.centerRight,
                                                      child: IconButton(
                                                        icon:
                                                            const Icon(Icons.delete),
                                                        onPressed: () =>
                                                            _deleteComment(
                                                                commentlist
                                                                    .commentlist[
                                                                        index]
                                                                    .id),
                                                      ),
                                                    ),
                                                  )
                                              ],
                                            )
                                          : const Text(
                                              "내용 없음",
                                              style: TextStyle(
                                                fontSize: 14,
                                              ),
                                            ),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                          );
                        },
                      )
                    : const Text("댓글 로딩중")),
          ],
        ),
      ),
    );
  }
}
