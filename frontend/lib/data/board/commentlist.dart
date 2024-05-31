class Comments {
  final int id;
  final String? content;
  final String author;
  final DateTime date;
  final int post;
  Comments({
    required this.id,
    required this.content,
    required this.author,
    required this.date,
    required this.post,
  });
}

class CommentList {
  final List<Comments> commentlist;
  CommentList({required this.commentlist});

  factory CommentList.fromJsonlist(List<dynamic> list) {
    var comment_list = <Comments>[];
    for (final Map<String, dynamic> json in list) {
      var comment = Comments(
          id: json['id'],
          content: json['content'],
          author: json['author'],
          date: DateTime.parse(json['created_at']),
          post: json['post']);
      comment_list.add(comment);
    }

    return CommentList(commentlist: comment_list);
  }
}
