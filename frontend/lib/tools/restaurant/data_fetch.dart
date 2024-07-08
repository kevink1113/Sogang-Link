


//전체 데이터를 받는 리스트. JSON 객체 형태로 저장됨.
List<dynamic> listfood = [];

Map name = {};
Map category = {};
Map trav_time = {};
Map price = {};
Map place = {};
Map tag = {};
List<int> listmeta = [];
List<dynamic> tags = [];
List<dynamic> places = [];
List<dynamic> prices = [];
List<String> categorys = <String>[];
List<String> recentSearches = []; //최근검색어 리스트
List<int> liked = [];

/*
[
  name
  address
  category
  trav_time
  place
  avg_Price
  tags [

  ]
  times [
    
  ]

]
*/

int makelist(var parsedList) {
  int idx = 0;
  liked = [];
  for (var i in parsedList) {
    name[i["name"]] = idx;
    if (category.containsKey(i["category"])) {
      //Map에 바로 대입
      category[i["category"]].add(idx);
    } else {
      //List에 추가
      categorys.add(i["category"]);

      //Map 초기화
      category[i["category"]] = <int>[];

      //Map에 대입
      category[i["category"]].add(idx);
    }
    if (trav_time.containsKey(i["trav_time"])) {
      //Map에 바로 대입
      trav_time[i["trav_time"]].add(idx);
    } else {
      //Map 초기화
      trav_time[i["trav_time"]] = <int>[];

      //Map에 대입
      trav_time[i["trav_time"]].add(idx);
    }


    //평균 가격이 데이터 안에 존재할 때
    if (i["avg_Price"] != 0) {
      //평균 가격대 설정
      var pp = ((i["avg_Price"]) / 10000).toInt();
      if (pp > 3) pp = 3;
      if (price.containsKey(pp)) {
        price[pp].add(idx);
      } else {
        price[pp] = <int>[];
        price[pp].add(idx);
      }
    } else {
      for (int i = 0; i < 4; i++) {
        if (!price.containsKey(i)) {
          price[i] = <int>[];
        }
        price[i].add(idx);
      }
    }
    if (place.containsKey(i["place"])) {
      place[i["place"]].add(idx);
    } else {
      place[i["place"]] = <int>[];
      place[i["place"]].add(idx);
    }
    for (var j in i["tags"]) {
      if (tag.containsKey(j)) {
        tag[j].add(idx);
      } else {
        tag[j] = [];
        tag[j].add(idx);
      }
    }


    idx++;
  }

  //전체 데이터에서 place / tag / price에 대한 리스트를 추출.
  places = place.keys.toList();
  tags = tag.keys.toList();
  prices = price.keys.toList();
  //파싱 끝.

  return 0;
}
