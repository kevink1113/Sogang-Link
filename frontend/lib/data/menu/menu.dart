class Menu {
  final int facility;
  final String facility_name;
  final Map<DateTime, Map<String, dynamic>> items_by_date;
  Menu({
    required this.facility,
    required this.facility_name,
    required this.items_by_date
  });
}

class MenuList {
  final Menu Em;
  final Menu BW;
  MenuList({
    required this.Em,
    required this.BW
  });

  factory MenuList.fromJsonlist(List<dynamic> list) {
    Menu em = Menu(facility: 22, facility_name: "엠마오 학생식당", items_by_date:{}, );

    Menu bw = Menu(facility: 23, facility_name: "우정원 학생식당", items_by_date:{}, );
    for (final Map<String, dynamic> json in list) {
      if(json['facility'] == em.facility){
        em.items_by_date[DateTime.parse(json['date'])] = json['items_by_corner'];
      }else if (json['facility'] == bw.facility){
        bw.items_by_date[DateTime.parse(json['date'])] = json['items_by_corner'];
      }
    }

    return MenuList(Em: em, BW: bw);
  }
}
