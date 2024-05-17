class Posts {
  final int id;
  final String? title;
  final String? content;
  final String? author;
  final DateTime date;
  final int view_count;
  final int sum_votes;
  Posts({
    required this.id,
    required this.title,
    required this.content,
    required this.author,
    required this.date,
    required this.view_count,
    required this.sum_votes,
  });
}

class PostList {
  final List<Posts> postList;
  PostList({required this.postList});

  factory PostList.fromJsonlist(List<dynamic> list) {
    var post_list = <Posts>[];
    for (final Map<String, dynamic> json in list) {
      var post = Posts(
          id: json['id'],
          title: json['title'],
          content: json['content'],
          author: json['author'],
          date: DateTime.parse(json['created_at']),
          view_count: json['view_count'],
          sum_votes: json['sum_votes']);
      post_list.add(post);
    }

    return PostList(postList: post_list);
  }
}
