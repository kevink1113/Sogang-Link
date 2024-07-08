import 'courses.dart';

class Take {
  final Course course;
  final String? middle_grade;
  final String? final_grade;
  final bool real;

  Take(
      {required this.course,
      required this.middle_grade,
      required this.final_grade,
      required this.real});

  factory Take.fromJson(Map<String, dynamic> json) {
    return Take(
      course: Course.fromJson(json["course"]),
      middle_grade: json["middle_grade"],
      final_grade: json["final_grade"],
      real: json["real"],
    );
  }
}

class Takes {
  final List<Take> cousrses_takes;
  final Set<int> semesters;

  Takes({required this.cousrses_takes, required this.semesters});

  factory Takes.fromJsonlist(List<dynamic> list) {
    var courseList = <Take>[];
    Set<int> sem = {};
    for (final Map<String, dynamic> json in list) {
      var take = Take(
          course: Course.fromJson(json["course"]),
          middle_grade: json["middle_grade"],
          final_grade: json["final_grade"],
          real: json["real"]);
      sem.add(take.course.semester);
      courseList.add(take);
    }

    return Takes(cousrses_takes: courseList, semesters: sem);
  }
}
