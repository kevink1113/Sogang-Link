class User {
  final String username;
  final String name;
  final int state;
  final int year;
  final int semeseter;
  final String major;
  final String advisor;
  final String nickname;

  User({
    required this.username,
    required this.name,
    required this.state,
    required this.year,
    required this.semeseter,
    required this.major,
    required this.advisor,
    required this.nickname,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
        username: json["username"],
        name: json["name"],
        state: json["state"],
        year: json["year"],
        semeseter: json["semester"],
        major: json["major"],
        advisor: json["advisor"],
        nickname: json["nickname"]);
  }
}
