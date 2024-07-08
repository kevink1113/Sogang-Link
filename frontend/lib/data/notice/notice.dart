class Notice {
  final int id;
  final String board;
  final String title;
  final String url;
  final String? writer;
  final DateTime date;

  Notice({
    required this.id,
    required this.board,
    required this.title,
    required this.url,
    required this.writer,
    required this.date,
  });
}

class NoticeList {
  final List<Notice> noticelist;
  NoticeList({required this.noticelist});

  factory NoticeList.fromJsonlist(List<dynamic> list) {
    var noticeList = <Notice>[];
    for (final Map<String, dynamic> json in list) {
      var notice = Notice(
          id: json['id'],
          board: json['board'],
          title: json['title'],
          url: json['url'],
          writer: json['writer'],
          date: DateTime.parse(json['date']));
      noticeList.add(notice);
    }

    return NoticeList(noticelist: noticeList);
  }
}
