import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:soganglink/tools/restaurant/result_with.dart';
import 'data_fetch.dart';
import 'package:path_provider/path_provider.dart';
import 'package:cache_manager/cache_manager.dart';
import 'package:http/http.dart' as http;

import '../../login.dart';
import '../../storage.dart';

class SearchTag extends StatefulWidget {
  const SearchTag({Key? key}) : super(key: key);

  @override
  SearchPageState createState() => SearchPageState();
}

class SearchPageState extends State<SearchTag> {
  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();

  // 사용자가 선택한 태그에 따라 전체 결과 중에서 필터링된 결과를 보여주는 페이지
  void clickBottons() {
    setState(() {
      List<int> tmpprice = [];
      for (int i in Iterable.generate(prices.length)) {
        if (isSelectedPrices[i]) tmpprice.addAll(price[i]);
      }
      tmpprice = tmpprice.toSet().toList();

      List<int> tmpplace = [];
      for (int i in Iterable.generate(places.length)) {
        if (isSelectedPlaces[i]) tmpplace.addAll(place[places[i]]);
      }
      tmpplace = tmpplace.toSet().toList();

      List<int> tmpcate = [];
      for (int i in Iterable.generate(categorys.length)) {
        if (isSelectedCate[i]) tmpcate.addAll(category[categorys[i]]);
      }
      tmpcate = tmpcate.toSet().toList();

      targetIndex = [];
      targetIndex.addAll(tmpprice);
      if (tmpplace.isNotEmpty && targetIndex.isNotEmpty) {
        targetIndex.removeWhere((item) => !tmpplace.contains(item));
      } else {
        targetIndex.addAll(tmpplace);
      }
      if (tmpcate.isNotEmpty && targetIndex.isNotEmpty) {
        targetIndex.removeWhere((item) => !tmpcate.contains(item));
      } else {
        targetIndex.addAll(tmpcate);
      }
      targetIndex.toSet().toList();
    });
  }

  List<bool> isSelectedPrices = []; //가격대 선택여부 리스트
  List<String> selectedPrices = []; //가격대 태그 리스트
  List<bool> isSelectedCate = []; //카테고리 선택여부 리스트
  List<String> selectedCates = []; //선택된 카테고리 리스트
  List<bool> isSelectedPlaces = []; //위치 선택여부 리스트
  List<String> selectedPlaces = []; //선택된 위치 리스트
  List<int> targetIndex = [];
  List<String> price_tags = ["1만원 이하", "1만원대", "2만원대", "3만원 이상"];

  bool loaded = false;


  @override
  void initState() {
    super.initState();
    loaded = false;
    try {
      SecureStorage.getToken().then((token) {
        try {
          http.get(Uri.parse("$url/maps/restaurants"),
              headers: {"Authorization": "Token $token"}).then((
              response) async {
            if (response.statusCode == 200) {
              listfood = jsonDecode(utf8.decode(response.bodyBytes));
              makelist(listfood);
              setState(() {
                isSelectedPrices =
                    List.generate(prices.length, (index) => false); // isSelectedPrices 초기화
                isSelectedCate =
                    List.generate(categorys.length, (index) => false); // isSelectedCate 초기화
                isSelectedPlaces =
                    List.generate(places.length, (index) => false); // isSelectedCate 초기화
                targetIndex = [];
                loaded = true;
              });
            } else {
              print("음식점 불러오기 실패");
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        key: scaffoldKey,
        appBar: AppBar(
          title: Text('음식점 검색기'),
        ),
        body: (loaded) ? ListView(
          children: [
            Container(
              margin: const EdgeInsets.symmetric(vertical: 12, horizontal: 0),
              child: SingleChildScrollView(
                child: Container(
                  padding: const EdgeInsets.fromLTRB(0, 0, 0, 20),
                  child: Column(
                    children: [
                      // 태그 선택하는 박스
                      Container(
                        margin: const EdgeInsets.symmetric(horizontal: 20),
                        decoration: BoxDecoration(
                          color: Colors.grey[200],
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: ClipRRect(
                          borderRadius: BorderRadius.circular(10),
                          child: Column(
                            children: [
                              // 메뉴 선택 줄
                              Container(
                                decoration: const BoxDecoration(
                                  border: Border(
                                    bottom: BorderSide(
                                      color: Colors.grey,
                                      width: 0.5,
                                      style: BorderStyle.solid,
                                    ),
                                  ),
                                ),
                                child: IntrinsicHeight(
                                  child: Row(
                                    crossAxisAlignment:
                                    CrossAxisAlignment.stretch,
                                    children: [
                                      Container(
                                        width: 80,
                                        decoration: BoxDecoration(
                                          color: Colors.grey[300],
                                        ),
                                        padding: const EdgeInsets.symmetric(
                                            vertical: 5),
                                        alignment: Alignment.center,
                                        child: const Text(
                                          '메뉴',
                                          style: TextStyle(
                                            fontSize: 16,
                                            fontFamily: "NanumSquare_ac",
                                            fontWeight: FontWeight.w400,
                                          ),
                                        ),
                                      ),
                                      Expanded(
                                        child: Container(
                                          padding: const EdgeInsets.symmetric(
                                            horizontal: 10,
                                            vertical: 10,
                                          ),
                                          child: Align(
                                            alignment: Alignment.centerLeft,
                                            child: Wrap(
                                              spacing: 15,
                                              runSpacing: 10,
                                              children: [
                                                for (int i = 0;
                                                i < categorys.length;
                                                i++)
                                                  Container(
                                                    padding: const EdgeInsets
                                                        .symmetric(
                                                        horizontal: 10),
                                                    decoration: BoxDecoration(
                                                      color: isSelectedCate[i]
                                                          ? Colors.amber[300]
                                                          : Colors.grey[200],
                                                      border: Border.all(
                                                        color: isSelectedCate[i]
                                                            ? const Color
                                                            .fromARGB(
                                                            255, 255, 213, 79)
                                                            : const Color
                                                            .fromARGB(255,
                                                            238, 238, 238),
                                                        width: 3,
                                                      ),
                                                      borderRadius:
                                                      BorderRadius.circular(
                                                          50),
                                                    ),
                                                    child: InkWell(
                                                      onTap: () {
                                                        isSelectedCate[i] =
                                                        !isSelectedCate[i];
                                                        clickBottons();
                                                      },
                                                      child: Text(
                                                        categorys[i],
                                                        style: const TextStyle(
                                                          fontSize: 16,
                                                          fontFamily:
                                                          "NanumSquare_ac",
                                                          fontWeight:
                                                          FontWeight.w400,
                                                        ),
                                                      ),
                                                    ),
                                                  ),
                                              ],
                                            ),
                                          ),
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                              // 장소 선택 줄
                              Container(
                                decoration: const BoxDecoration(
                                  border: Border(
                                    bottom: BorderSide(
                                      color: Colors.grey,
                                      width: 0.5,
                                      style: BorderStyle.solid,
                                    ),
                                  ),
                                ),
                                child: IntrinsicHeight(
                                  child: Row(
                                    crossAxisAlignment:
                                    CrossAxisAlignment.stretch,
                                    children: [
                                      Container(
                                        width: 80,
                                        decoration: BoxDecoration(
                                          color: Colors.grey[300],
                                        ),
                                        padding: const EdgeInsets.symmetric(
                                            vertical: 5),
                                        alignment: Alignment.center,
                                        child: const Text(
                                          '장소',
                                          style: TextStyle(
                                            fontSize: 16,
                                            fontFamily: "NanumSquare_ac",
                                            fontWeight: FontWeight.w400,
                                          ),
                                        ),
                                      ),
                                      Expanded(
                                        child: Container(
                                          padding: const EdgeInsets.symmetric(
                                            horizontal: 10,
                                            vertical: 10,
                                          ),
                                          child: Align(
                                            alignment: Alignment.centerLeft,
                                            child: Wrap(
                                              spacing: 15,
                                              runSpacing: 10,
                                              children: [
                                                for (int i = 0;
                                                i < places.length;
                                                i++)
                                                  Container(
                                                    padding: const EdgeInsets
                                                        .symmetric(
                                                        horizontal: 10),
                                                    decoration: BoxDecoration(
                                                      color: isSelectedPlaces[i]
                                                          ? Colors.amber[300]
                                                          : Colors.grey[200],
                                                      border: Border.all(
                                                        color: isSelectedPlaces[i]
                                                            ? const Color
                                                            .fromARGB(
                                                            255, 255, 213, 79)
                                                            : const Color
                                                            .fromARGB(255,
                                                            238, 238, 238),
                                                        width: 3,
                                                      ),
                                                      borderRadius:
                                                      BorderRadius.circular(
                                                          50),
                                                    ),
                                                    child: InkWell(
                                                      onTap: () {
                                                        isSelectedPlaces[i] =
                                                        !isSelectedPlaces[i];
                                                        clickBottons();
                                                      },
                                                      child: Text(
                                                        places[i],
                                                        style: const TextStyle(
                                                          fontSize: 16,
                                                          fontFamily:
                                                          "NanumSquare_ac",
                                                          fontWeight:
                                                          FontWeight.w400,
                                                        ),
                                                      ),
                                                    ),
                                                  ),
                                              ],
                                            ),
                                          ),
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                              // 가격대 선택 줄
                              IntrinsicHeight(
                                child: Row(
                                  crossAxisAlignment: CrossAxisAlignment
                                      .stretch,
                                  children: [
                                    Container(
                                      width: 80,
                                      decoration: BoxDecoration(
                                        color: Colors.grey[300],
                                      ),
                                      padding:
                                      const EdgeInsets.symmetric(vertical: 5),
                                      alignment: Alignment.center,
                                      child: const Text(
                                        '가격대',
                                        style: TextStyle(
                                          fontSize: 16,
                                          fontFamily: "NanumSquare_ac",
                                          fontWeight: FontWeight.w400,
                                        ),
                                      ),
                                    ),
                                    Expanded(
                                      child: Container(
                                        padding: const EdgeInsets.symmetric(
                                          horizontal: 10,
                                          vertical: 10,
                                        ),
                                        child: Align(
                                          alignment: Alignment.centerLeft,
                                          child: Wrap(
                                            spacing: 15,
                                            runSpacing: 10,
                                            children: [
                                              for (int i = 0;
                                              i < prices.length;
                                              i++)
                                                Container(
                                                  padding:
                                                  const EdgeInsets.symmetric(
                                                      horizontal: 10),
                                                  decoration: BoxDecoration(
                                                    color: isSelectedPrices[i]
                                                        ? Colors.amber[300]
                                                        : Colors.grey[200],
                                                    border: Border.all(
                                                      color: isSelectedPrices[i]
                                                          ? const Color
                                                          .fromARGB(
                                                          255, 255, 213, 79)
                                                          : const Color
                                                          .fromARGB(
                                                          255, 238, 238, 238),
                                                      width: 3,
                                                    ),
                                                    borderRadius:
                                                    BorderRadius.circular(50),
                                                  ),
                                                  child: InkWell(
                                                    onTap: () {
                                                      isSelectedPrices[i] =
                                                      !isSelectedPrices[i];
                                                      clickBottons();
                                                    },
                                                    child: Text(
                                                      price_tags[i],
                                                      style: const TextStyle(
                                                        fontSize: 16,
                                                        fontFamily:
                                                        "NanumSquare_ac",
                                                        fontWeight:
                                                        FontWeight.w400,
                                                      ),
                                                    ),
                                                  ),
                                                ),
                                            ],
                                          ),
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                      const SizedBox(
                        height: 10,
                      ),
                      const Divider(
                        thickness: 1.5,
                        indent: 20,
                        endIndent: 20,
                      ),
                      ListView.separated(
                        shrinkWrap: true,
                        physics: NeverScrollableScrollPhysics(),
                        itemCount: targetIndex.length + 1,
                        itemBuilder: (context, index) {
                          if (index == targetIndex.length) {
                            return Container();
                          } else {
                            return ListTile(
                              title: Text(listfood[targetIndex[index]]["name"]),
                              subtitle:
                              Text(listfood[targetIndex[index]]["OneLiner"]),
                              contentPadding:
                              const EdgeInsets.symmetric(horizontal: 30),
                              onTap: () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                      builder: (context) =>
                                          resultlist_with(
                                              targetIndex[index], null)),
                                );
                              },
                            );
                          }
                        },
                        separatorBuilder: (context, index) {
                          return const Divider(
                            thickness: 1.5,
                            indent: 20,
                            endIndent: 20,
                          );
                        },
                      )
                    ],
                  ),
                ),
              ),
            ),

          ],
        )
            : Center(child: Text('로딩중'))
    );
  }
}
