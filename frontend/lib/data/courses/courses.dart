class Course {
  final int id;
  final String course_id;
  final String semester;
  final String name;
  final String day;
  final int start_time; // 9시 기준 몇분후 시작
  final int end_time; // 9시 기준 몇분후 끝
  final String classroom;
  final String advisor;
  final String major;

  Course(
      {required this.id,
      required this.course_id,
      required this.semester,
      required this.name,
      required this.day,
      required this.start_time,
      required this.end_time,
      required this.classroom,
      required this.advisor,
      required this.major});

  factory Course.fromJson(Map<String, dynamic> json) {
    var starttime = json["start_time"].split(':');
    var endtime = json["end_time"].split(':');
    return Course(
        id: json["id"],
        course_id: json["course_id"],
        semester: json["semester"].toString(),
        name: json["name"],
        day: json["day"].toString(),
        start_time:
            ((int.parse(starttime[0]) - 9) * 60 + int.parse(starttime[1])),
        end_time: ((int.parse(endtime[0]) - 9) * 60 + int.parse(endtime[1])),
        classroom: json["classroom"],
        advisor: json["advisor"],
        major: json["major"]);
  }
}
