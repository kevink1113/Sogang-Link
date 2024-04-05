class Course {
  final int id;
  final String course_id;
  final int semester;
  final String name;
  final String? day;
  final int? start_time; // 9시 기준 몇분후 시작
  final int? end_time; // 9시 기준 몇분후 끝
  final String? classroom;
  final String? advisor;
  final String? major;

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
    var starttime = null;
    if (json["start_time"] != null) {
      var s = json["start_time"].split(':');
      starttime = ((int.parse(s[0]) - 9) * 60 + int.parse(s[1]));
    }

    var endtime = null;
    if (json["end_time"] != null) {
      var e = json["end_time"].split(':');
      endtime = ((int.parse(e[0]) - 9) * 60 + int.parse(e[1]));
    }

    return Course(
        id: json["id"],
        course_id: json["course_id"],
        semester: json["semester"],
        name: json["name"],
        day: json["day"].toString(),
        start_time: starttime,
        end_time: endtime,
        classroom: json["classroom"],
        advisor: json["advisor"],
        major: json["major"]);
  }
}
