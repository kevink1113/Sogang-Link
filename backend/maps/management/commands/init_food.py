# management/commands/populate_restaurants.py
from django.core.management.base import BaseCommand
from maps.models import Restaurant, Tag
import json

class Command(BaseCommand):
    help = 'Populate the database with restaurant data'

    def handle(self, *args, **kwargs):
        data = [
          {
            "name":"678 버거",
            "address":"서울특별시 마포구 서강로16길 69 2 층",
            "category":"양식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":8000,
            "tags":[
              "햄버거"
            ],
            "times":[
              "10:30",
              "00:50"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090810849293242428\/2022-09-16.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/V6GsDMeUhGrwzu5D6",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1588376257?c=15.00,0,0,0,dh",
            "OneLiner":"그래도 평타 이상의 햄버거"
          },
          {
            "name":"New York Apartment",
            "address":"서울특별시 마포구 합정동 385-9",
            "category":"양식",
            "trav_time":3,
            "place":"합정",
            "avg_Price":22900,
            "tags":[
              "햄버거",
              "수제"
            ],
            "times":[
              "11:00",
              "23:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090173964334149632\/2023-03-26.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/SFdbF7RjTFzExo767",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/19594124?c=15.00,0,0,0,dh",
            "OneLiner":"이것은 햄버거인가 빵을 곁들인 고기덩어리인가"
          },
          {
            "name":"TAO",
            "address":"서울특별시 서대문구 창천동 57-9",
            "category":"중식",
            "trav_time":2,
            "place":"신촌",
            "avg_Price":0,
            "tags":[
              "마라탕"
            ],
            "times":[
              "11:30",
              "20:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090171937927467018\/2023-03-18.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/RnHC5jnSiqi7qoJU8",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1153861853?c=15.00,0,0,0,dh",
            "OneLiner":"이 근처 제일 맛있는 마라탕집(주관적)"
          },
          {
            "name":"Tol",
            "address":"서울특별시 마포구 대흥로20안길 11",
            "category":"일식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":8900,
            "tags":[
              "가츠동",
              "나베"
            ],
            "times":[
              "10:00",
              "21:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1089791077390757918\/14581307_1777576772532082_8948001613008854768_n.png",
            "MapLink":"https:\/\/goo.gl\/maps\/LCTTyCGnNr66S2YdA",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1871670311?c=15.00,0,0,0,dh",
            "OneLiner":"가츠동이랑 나베도 맛있지만 개인적으로는 마제면도 맛있어요"
          },
          {
            "name":"deeper",
            "address":"서울특별시 마포구 동교동 188-2번지 2층",
            "category":"주점",
            "trav_time":2,
            "place":"서강",
            "avg_Price":17900,
            "tags":[
              "피자",
              "루프탑",
              "맥주"
            ],
            "times":[
              "15:00",
              "01:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1089812258961489930\/20230205_201509.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/g727zJdptauLg28W9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/836030725?c=15.00,0,0,0,dh",
            "OneLiner":"피자 종류 많은 루프탑 맥주집"
          },
          {
            "name":"世界の果てのラーメン",
            "address":"서울특별시 마포구 양화로7길 6-5",
            "category":"일식",
            "trav_time":3,
            "place":"합정",
            "avg_Price":8000,
            "tags":[
              "라멘",
              "본토의_맛"
            ],
            "times":[
              "11:00",
              "15:00",
              "17:00",
              "20:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1089913055682506794\/99A784445C8375AD01.png",
            "MapLink":"https:\/\/goo.gl\/maps\/65wdDiuKaJvj3VbEA",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1644407254?c=15.00,0,0,0,dh",
            "OneLiner":"별 볼 일 없지만 다른 라멘집에 갈수록 여기가 생각납니다."
          },
          {
            "name":"가츠벤또",
            "address":"서울특별시 마포구 노고산동 31-90",
            "category":"일식",
            "trav_time":1,
            "place":"서강",
            "avg_Price":16000,
            "tags":[
              "가츠동"
            ],
            "times":[
              "11:00",
              "15:00",
              "16:30",
              "21:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090603253097562142\/20221021_184757.jpg",
            "MapLink":"https:\/\/maps.app.goo.gl\/qYyxPVRNQP7noYGJ7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/21581714?c=15.00,0,0,0,dh",
            "OneLiner":"항상 처음 만난 선배가 밥사준다고 하면 여기 가더라."
          },
          {
            "name":"거구장(케이터틀)",
            "address":"서울특별시 마포구 신수동 63-14",
            "category":"한식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":23800,
            "tags":[
              "한정식"
            ],
            "times":[
              "11:00",
              "15:00",
              "17:00",
              "21:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090898497856880720\/2022-10-22.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/1WFnC3xu5d3hxPDE9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1213745867?c=15.00,0,0,0,dh",
            "OneLiner":"부모님 오셨을때 가기 좋은 한정식집"
          },
          {
            "name":"거북이의 주방",
            "address":"서울특별시 마포구 백범로1길 10",
            "category":"양식",
            "trav_time":1,
            "place":"서강",
            "avg_Price":9600,
            "tags":[
              "카레"
            ],
            "times":[
              "10:00",
              "15:00",
              "16:30",
              "21:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1089911744178167859\/14650_1636764710404_26551.png",
            "MapLink":"https:\/\/goo.gl\/maps\/2wen2mGq64WZrRN49",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/35915198?c=15.00,0,0,0,dh",
            "OneLiner":"카레 맛있음. 밥 추가 가능하지만 양이 생각보다 많아서 추가 안하게 됨."
          },
          {
            "name":"고기마니 밥마니",
            "address":"서울특별시 마포구 신수동 백범로 68",
            "category":"한식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":7400,
            "tags":[
              "고기",
              "무한리필"
            ],
            "times":[
        
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090601805974622340\/2019-03-03.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/Zx6dsMsmkBA75aRt8",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/37555555?c=15.00,0,0,0,dh",
            "OneLiner":"고기는 언제나 옳다."
          },
          {
            "name":"고주파",
            "address":"서울특별시 마포구 신수동 광성로6길 28",
            "category":"주점",
            "trav_time":0,
            "place":"서강",
            "avg_Price":7600,
            "tags":[
              "고기",
              "술"
            ],
            "times":[
              "17:00",
              "24:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090603132637171772\/20210205_142836_HDR.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/RoyH5LRjHBizkVa76",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/34937148?c=15.00,0,0,0,dh",
            "OneLiner":"\"High Frequency\"라고 부르는 사람은 전자과입니다."
          },
          {
            "name":"공복식당",
            "address":"서울특별시 서대문구 연세로12길 23",
            "category":"한식",
            "trav_time":2,
            "place":"신촌",
            "avg_Price":11400,
            "tags":[
              "돼지고기구이"
            ],
            "times":[
              "16:00",
              "22:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090166921565057085\/2020-12-25.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/SsBjLRoWqDjSbWtg8",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/38286911?c=15.00,0,0,0,dh",
            "OneLiner":"비싼 가격이지만 제값을 하는 최고의 돼지고기구이집! 소주 땡긴다~"
          },
          {
            "name":"광안리",
            "address":"서울특별시 마포구 대흥동  32-15번지",
            "category":"일식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":22200,
            "tags":[
              "사케동",
              "연어"
            ],
            "times":[
              "11:00",
              "14:40",
              "17:00",
              "22:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090172899329052712\/2022-10-23.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/voQrM3iAt2EY5PGWA",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1565755388?c=15.00,0,0,0,dh",
            "OneLiner":"육회비빔밥도 맛있고 사케동도 맛이씀"
          },
          {
            "name":"규니왕타코",
            "address":"서울특별시 서대문구 신촌역로 4 1층",
            "category":"간식",
            "trav_time":2,
            "place":"이대",
            "avg_Price":4000,
            "tags":[
              "타코야키"
            ],
            "times":[
              "15:00",
              "02:00"
            ],
            "image":"https:\/\/mblogthumb-phinf.pstatic.net\/MjAxNzAxMjJfOTIg\/MDAxNDg1MDg2MjcwMTkz.GhbuUid2L5V58UjQraLvRsSuVIuBikrtWKhDFZWJQ5kg.vKY2VcFjdDKSpXb0EzEgHylK09gB1A2XePALS0ps4Okg.JPEG.gypsyone\/image_2969689161485086135630.jpg?type=w800",
            "MapLink":"https:\/\/goo.gl\/maps\/GJvj5HUzPEgH6FsE7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1615765212?c=15.00,0,0,0,dh",
            "OneLiner":"이화여대 맛집게시판 기준 별점 5점. 방문 후 후기 부탁드립니다."
          },
          {
            "name":"그레이스국밥",
            "address":"서울특별시 마포구 마포대로12길 18",
            "category":"한식",
            "trav_time":2,
            "place":"공덕",
            "avg_Price":10000,
            "tags":[
              "국밥",
              "막걸리"
            ],
            "times":[
              "11:00",
              "15:00",
              "17:00",
              "22:00"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1046418973954158612\/1156788233435349082\/image0.jpg?ex=65163e7e&is=6514ecfe&hm=f7c3b44f1755797bc0bf8656397f39064679c3ef249c29f0d34bfc0a8c591dbe&",
           
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1910505525?c=18.38,0,0,0,dh",
            "OneLiner":"비싸지만 깔끔한 명품 국밥."
          },
          {
            "name":"까이식당",
            "address":"서울특별시 서대문구 이화여대2가길 24",
            "category":"기타",
            "trav_time":2,
            "place":"이대",
            "avg_Price":10000,
            "tags":[
              "치킨라이스"
            ],
            "times":[
              "11:00",
              "15:00",
              "17:00",
              "20:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090173133153124392\/2022-06-21.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/mW8nUWeGC2rPGAPfA",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/37792177?c=15.00,0,0,0,dh",
            "OneLiner":"수비드 닭고기가 들어간 독특한 동남아식 치킨라이스"
          },
          {
            "name":"꼬숑돈까스",
            "address":"서울특별시 서대문구 명물1길 2",
            "category":"일식",
            "trav_time":2,
            "place":"신촌",
            "avg_Price":5000,
            "tags":[
              "돈까스"
            ],
            "times":[
              "11:00",
              "16:00",
              "17:00",
              "20:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090898238032322560\/2023-01-07.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/CoHGStLykYhbbuVL9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1733373968?c=15.00,0,0,0,dh",
            "OneLiner":"일식 돈까스가 4000원??"
          },
          {
            "name":"나베공방",
            "address":"서울특별시 마포구 양화로6길 57-24 1층",
            "category":"주점",
            "trav_time":3,
            "place":"합정",
            "avg_Price":29000,
            "tags":[
              "나베",
              "술"
            ],
            "times":[
              "17:00",
              "00:20"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090175695294050304\/20220127_184808.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/1UVwvyzhnTYbCE2WA",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1023342470?c=15.00,0,0,0,dh",
            "OneLiner":"난 여기보다 더 맛있는 나베집을 본 적이 없어"
          },
          {
            "name":"남매밥상",
            "address":"서울특별시 마포구 대흥동 325 13번지 1층 102호",
            "category":"한식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":12600,
            "tags":[
              "백반"
            ],
            "times":[
              "10:30",
              "20:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1089917588282290296\/common.png",
            "MapLink":"https:\/\/goo.gl\/maps\/snYPSXZUtTunJ5Lq7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1072227360?c=15.00,0,0,0,dh",
            "OneLiner":"고등어구이 맛있겠따ㅏ"
          },
          {
            "name":"남원 추어탕",
            "address":"서울특별시 마포구 광성로 35",
            "category":"한식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":12000,
            "tags":[
              "추어탕"
            ],
            "times":[
              "10:00",
              "21:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090900449231646830\/2021-03-30.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/bbC4fsQPYe4gTzTy8",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/18335431?c=15.00,0,0,0,dh",
            "OneLiner":"든든하다. 플라시보인지는 모르겠지만 기운도 난다."
          },
          {
            "name":"낭만식탁",
            "address":"서울특별시 서대문구 이화여대5길 6",
            "category":"일식",
            "trav_time":2,
            "place":"이대",
            "avg_Price":13000,
            "tags":[
              "덮밥"
            ],
            "times":[
              "11:00",
              "15:00",
              "17:00",
              "20:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090172224713015436\/2019-12-17.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/gYaECCaCAdNv5xCdA",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/46808073?c=15.00,0,0,0,dh",
            "OneLiner":"밥약 하기 괜찮은 연어덮밥\/간장새우덮밥집!"
          },
          {
            "name":"낭만오지",
            "address":"서울특별시 마포구 고산길 17",
            "category":"주점",
            "trav_time":1,
            "place":"서강",
            "avg_Price":16700,
            "tags":[
              "치킨",
              "술"
            ],
            "times":[
              "16:30",
              "02:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090166423290126366\/2021-10-17.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/AVsDgMoMxio11rYD6",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/34006458?c=15.00,0,0,0,dh",
            "OneLiner":"\"낭만오지 좀 그만 가자\" 하는 사람은 화석입니다. 토마토치킨 맛있음."
          },
          {
            "name":"네이버후드",
            "address":"서울특별시 서대문구 연세로7안길 41",
            "category":"양식",
            "trav_time":2,
            "place":"신촌",
            "avg_Price":16200,
            "tags":[
              "피자",
              "맥주"
            ],
            "times":[
              "16:00",
              "01:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1089812310551449661\/2Q.png",
            "MapLink":"https:\/\/goo.gl\/maps\/CZvy7jtgxAoXqKQ9A",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1544835372?c=15.00,0,0,0,dh",
            "OneLiner":"맥주 종류 많은 피자집"
          },
          {
            "name":"녹기전에",
            "address":"서울특별시 마포구 염리동 148-22",
            "category":"간식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":20200,
            "tags":[
              "아이스크림",
              "기상천외"
            ],
            "times":[
              "12:00",
              "22:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1089914355795116142\/745A4171.png",
            "MapLink":"https:\/\/goo.gl\/maps\/nzFzmht5JQKVGPRW9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/815032618?c=15.00,0,0,0,dh",
            "OneLiner":"카이스트 화학과가 연구끝에 만들어낸 재료 본연의 맛을 살린 아이스크림"
          },
          {
            "name":"누들김밥",
            "address":"서울특별시 서대문구 이화여대8길 2 무궁화상가아파트 지하 103호 누들김밥",
            "category":"한식",
            "trav_time":2,
            "place":"이대",
            "avg_Price":6000,
            "tags":[
              "김밥"
            ],
            "times":[
              "08:00",
              "20:30"
            ],
            "image":"https:\/\/mp-seoul-image-production-s3.mangoplate.com\/486316_1540456806251064.jpg?fit=around|512:512&crop=512:512;*,*&output-format=jpg&output-quality=80",
            "MapLink":"https:\/\/goo.gl\/maps\/pNNcbfPrCD7ZuMD37",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/21857230?c=15.00,0,0,0,dh",
            "OneLiner":"이화여대 맛집게시판 기준 별점 5점. 방문 후 후기 부탁드립니다."
          },
          {
            "name":"더바스켓",
            "address":"서울특별시 마포구 대흥동 266-1",
            "category":"기타",
            "trav_time":0,
            "place":"서강",
            "avg_Price":25500,
            "tags":[
              "떡볶이",
              "치킨"
            ],
            "times":[
              "11:30",
              "23:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090602627726839808\/2022-02-07.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/Vb6JJzmQHN3j6n3N6",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1531822720?c=15.00,0,0,0,dh",
            "OneLiner":"치킨과 떡볶이가 있는 이상한 맛집."
          },
          {
            "name":"더파니니",
            "address":"서울특별시 서대문구 신촌동 이화여대길 50-10",
            "category":"양식",
            "trav_time":2,
            "place":"이대",
            "avg_Price":7500,
            "tags":[
              "파니니",
              "샐러드"
            ],
            "times":[
        
            ],
            "image":"https:\/\/mblogthumb-phinf.pstatic.net\/MjAxNzA1MjNfMTkw\/MDAxNDk1NTE5ODE3ODY5.7_uOnj-r2EDNRfwJeFbI6j55UHsz6zp4Rq6CRFGjSwAg.gPbePHjwOyobRCEj4F2uFE0UZGMqe16k0UHfSUSluTsg.JPEG.hanna21kim\/16%EC%9D%B4%EB%8C%80_%EB%8D%94_%ED%8C%8C%EB%8B%88%EB%8B%88.jpg?type=w800",
            "MapLink":"https:\/\/goo.gl\/maps\/ZszDoQtuZg4WQWau7",
            "NaverMap":"",
            "OneLiner":"이화여대 맛집게시판 기준 별점 5점. 방문 후 후기 부탁드립니다."
          },
          {
            "name":"덮당",
            "address":"서울특별시 마포구 신수동 81-100",
            "category":"일식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":8600,
            "tags":[
              "덮밥"
            ],
            "times":[
              "10:00",
              "20:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1159080512808300695\/4cb49aec2d2e11edacb70242ac110004.jpg?ex=651e9558&is=651d43d8&hm=9127bac57fa9dd2bd02a915233afab57d0d9a177272d691afc37533c0a20b0fb&",
            "MapLink":"https:\/\/goo.gl\/maps\/iXfcJK2u2tcLvPm28",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1086317653?c=15.00,0,0,0,dh",
            "OneLiner":"거리도 가까운데 맛도 있는 든든한 덮밥집. 자리는 좁아요."
          },
          {
            "name":"도쿄샌드위치",
            "address":"서울 마포구 광성로4길 21-12 1층",
            "category":"양식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":7000,
            "tags":[
              "샌드위치",
              "바나나쥬스",
              "카레"
            ],
            "times":[
              "8:00",
              "19:30"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1146588346139824308\/1160879706149748836\/image.png?ex=6536447a&is=6523cf7a&hm=a8e94263562e6d360c7f5575582901c06e732a06e0158d4bf80c558674ff4c7d&=&width=736&height=549",
            # # "MapLink":"",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/37542841?c=15.00,0,0,0,dh",
            "OneLiner":"남문의 샌드위치 맛집. 카레도 팝니다."
          },
          {
            "name":"돌솥밥 찌개마을",
            "address":"서울특별시 서대문구 이화여대7길 14 1층",
            "category":"한식",
            "trav_time":2,
            "place":"이대",
            "avg_Price":10000,
            "tags":[
              "찌개"
            ],
            "times":[
        
            ],
            "image":"https:\/\/img.siksinhot.com\/place\/1444756485785179.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/3zUeRufGBphkfpcTA",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1296685318?placePath=%2Fhome&c=15.00,0,0,0,dh",
            "OneLiner":"이화여대 맛집게시판 기준 별점 5점. 방문 후 후기 부탁드립니다."
          },
          {
            "name":"동해횟집 ",
            "address":"서울특별시 마포구 대흥동 31-170",
            "category":"일식",
            "trav_time":1,
            "place":"서강",
            "avg_Price":12200,
            "tags":[
              "횟집",
              "술"
            ],
            "times":[
              "12:00",
              "02:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090898834688847922\/image.png",
            "MapLink":"https:\/\/goo.gl\/maps\/wY63A4uKtoH23Wdm6",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1664804076?c=15.00,0,0,0,dh",
            "OneLiner":"선배들이 자주 갔다는 횟집"
          },
          {
            "name":"따띠삼겹",
            "address":"서울특별시 서대문구 이화여대7길 15 1층(대현동)",
            "category":"한식",
            "trav_time":2,
            "place":"이대",
            "avg_Price":9800,
            "tags":[
              "삼겹살",
              "포장"
            ],
            "times":[
              "11:30",
              "15:00",
              "16:00",
              "21:30"
            ],
            "image":"https:\/\/d3af5evjz6cdzs.cloudfront.net\/images\/uploads\/800x0\/download-18_a73919d07dc73aeb0d4d63e4a29dd1b81676875255.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/pg6DLCjeCcSej7di9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1462964953?c=15.00,0,0,0,dh",
            "OneLiner":"이화여대 맛집게시판 기준 별점 5점. 방문 후 후기 부탁드립니다."
          },
          {
            "name":"라장훠궈",
            "address":"서울특별시 서대문구 신촌동 연세로 35",
            "category":"중식",
            "trav_time":2,
            "place":"신촌",
            "avg_Price":13600,
            "tags":[
              "양꼬치",
              "훠궈"
            ],
            "times":[
              "11:00",
              "22:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090166617721282650\/2022-10-10.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/4Nwmm3Q1pKzet7Yv9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1672520602?c=15.00,0,0,0,dh",
            "OneLiner":"신촌에는 훠궈+양꼬치가 무한리필인 전설적인 식당이 있대... (소근소근)"
          },
          {
            "name":"마포리 1987",
            "address":"서울특별시 마포구 대흥동 403",
            "category":"양식",
            "trav_time":1,
            "place":"서강",
            "avg_Price":17800,
            "tags":[
              "파스타",
              "치킨"
            ],
            "times":[
              "11:30",
              "15:00",
              "17:00",
              "21:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090602482511655013\/2022-06-04.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/hY96QjEBiA6FuaqHA",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/37690949?c=15.00,0,0,0,dh",
            "OneLiner":"이곳에서 후배에게 밥을 사주는 당신은 멋쟁이."
          },
          {
            "name":"마포만두",
            "address":"서울특별시 마포구 백범로 95 다나빌딩",
            "category":"중식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":6200,
            "tags":[
              "만두",
              "라면",
              "분식"
            ],
            "times":[
              "00:00",
              "24:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090637524524859532\/20190529_221359.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/nqTZ6aGBykKBchMD9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/18770344?c=15.00,0,0,0,dh",
            "OneLiner":"\"이정도면 뭐 걸어서 13초네요.\""
          },
          {
            "name":"마포쌈밥식당",
            "address":"서울특별시 마포구 신수동 81-45",
            "category":"한식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":8500,
            "tags":[
              "쌈밥",
              "불고기"
            ],
            "times":[
              "11:00",
              "19:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090164714971091054\/2022-11-20.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/x83fs7kS45HRF9YK6",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1045474371?c=15.00,0,0,0,dh",
            "OneLiner":"\"춥고 배고파요...\" 한끼만 든든히 먹고 하루를 버텨야 할 때"
          },
          {
            "name":"망원동 즉석우동",
            "address":"서울특별시 마포구 망원제1동 385-26",
            "category":"한식",
            "trav_time":3,
            "place":"합정",
            "avg_Price":6600,
            "tags":[
              "돈까스",
              "우동"
            ],
            "times":[
              "11:00",
              "22:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090600381517668352\/2023-02-16.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/rTrps7wyrdPiYwJu6",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/31583220?c=15.00,0,0,0,dh",
            "OneLiner":"아! 달콤짭짜름한 옜날 돈까쓰의 추억이여!"
          },
          {
            "name":"메종드리즈팡",
            "address":"서울특별시 서대문구 이화여대길 81",
            "category":"간식",
            "trav_time":2,
            "place":"이대",
            "avg_Price":4700,
            "tags":[
              "빵"
            ],
            "times":[
        
            ],
            "image":"https:\/\/search.pstatic.net\/common\/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA2MTBfMTUz%2FMDAxNjg2MzI3MjMzNzAx.fOObLrdvnJr8rs0sVukZB1pmb64qb0bT5iLZW15NyuEg.8Ve1WVFj38M9hcBocvBr8n0kO4gnapVPT7GrNeZ2gNYg.JPEG.redcat731%2FIMG_1432.jpg",
            "MapLink":"https:\/\/map.naver.com\/v5\/entry\/place\/1827482319?placePath=%2Fhome&c=15,0,0,0,dh",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1827482319?c=15.00,0,0,0,dh",
            "OneLiner":"이화여대 맛집게시판 기준 별점 5점. 방문 후 후기 부탁드립니다."
          },
          {
            "name":"멘카야",
            "address":"서울특별시 마포구 마포대로10길 20",
            "category":"일식",
            "trav_time":2,
            "place":"공덕",
            "avg_Price":9000,
            "tags":[
              "라멘",
              "덮밥"
            ],
            "times":[
              "11:30",
              "15:00",
              "17:30",
              "21:00"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1046418973954158612\/1156785452892831864\/image0.jpg?ex=65163be8&is=6514ea68&hm=10c5d99b0249262e39f7efe5ad1c4461262fbead87ce19344fddafa98a5af915&",
            # # "MapLink":"",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/84178291?c=18.38,0,0,0,dh",
            "OneLiner":"공덕의 무난한 라멘집."
          },
          {
            "name":"모미지식당",
            "address":"서울특별시 서대문구 대현동 56-36",
            "category":"일식",
            "trav_time":2,
            "place":"이대",
            "avg_Price":10500,
            "tags":[
              "덮밥"
            ],
            "times":[
              "11:30",
              "15:30",
              "17:00",
              "19:30"
            ],
            "image":"https:\/\/d12zq4w4guyljn.cloudfront.net\/20220529111417_photo1_ba2b8a1f6698.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/rzLfq7JXzQ8KwAsJ8",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1915239189?c=15.00,0,0,0,dh",
            "OneLiner":"이화여대 맛집게시판 기준 별점 5점. 방문 후 후기 부탁드립니다."
          },
          {
            "name":"미가",
            "address":"서울특별시 마포구 염리동 숭문길 47",
            "category":"한식",
            "trav_time":1,
            "place":"서강",
            "avg_Price":40000,
            "tags":[
              "육회비빔밥"
            ],
            "times":[
        
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090173820641480734\/20221001_103712.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/QDmeVc67D7nvZF1XA",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1706452151?c=15.00,0,0,0,dh",
            "OneLiner":"언뜻 보면 평범한 한식집이지만, 이곳에서는 육회비빔밥을 판다!"
          },
          {
            "name":"미도인(신촌)",
            "address":"서울특별시 서대문구 창천동 31-86 번지 2층",
            "category":"일식",
            "trav_time":2,
            "place":"신촌",
            "avg_Price":12300,
            "tags":[
              "스테이크",
              "덮밥"
            ],
            "times":[
              "11:30",
              "15:00",
              "17:00",
              "21:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090601523433709568\/2022-10-24.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/xAZ1yRPF4Sf1r1i78",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1679026287?c=15.00,0,0,0,dh",
            "OneLiner":"스테이크 덮밥이 꽤 괜찮은 집 (신촌)"
          },
          {
            "name":"미도인(홍대)",
            "address":"서울특별시 마포구 잔다리로2길 19",
            "category":"일식",
            "trav_time":3,
            "place":"홍대",
            "avg_Price":15700,
            "tags":[
              "스테이크",
              "덮밥"
            ],
            "times":[
              "11:30",
              "15:00",
              "17:00",
              "21:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090601523433709568\/2022-10-24.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/PG7h4mGDCVFUg8Dv6",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1436718221?c=15.00,0,0,0,dh",
            "OneLiner":"스테이크 덮밥이 꽤 괜찮은 집 (홍대)"
          },
          {
            "name":"미쁘동",
            "address":"서울특별시 마포구 동교로38길 33-21",
            "category":"일식",
            "trav_time":3,
            "place":"홍대",
            "avg_Price":18700,
            "tags":[
              "사케동"
            ],
            "times":[
              "11:00",
              "21:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090175440733343875\/PXL_20230309_021203878.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/JMrPHYWFpwZ6qjKH9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1685805793?c=15.00,0,0,0,dh",
            "OneLiner":"연어 국수라는 말 들어봤어? 말 그대로 생연어로 국수를 만든다는 뜻이야!"
          },
          {
            "name":"밀플랜비",
            "address":"서울특별시 마포구 대흥동 40-3",
            "category":"기타",
            "trav_time":0,
            "place":"서강",
            "avg_Price":6200,
            "tags":[
              "부리또"
            ],
            "times":[
              "10:00",
              "21:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090173280721313822\/2022-05-04.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/PsbKfSA2FJ5Ypyvq9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1298514038?c=15.00,0,0,0,dh",
            "OneLiner":"양은 적은데 배부른 부리또. 의외로 괜찮음."
          },
          {
            "name":"바른치킨",
            "address":"서울특별시 마포구 광성로6길 16",
            "category":"양식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":23100,
            "tags":[
              "치킨",
              "떡볶이"
            ],
            "times":[
              "16:00",
              "23:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090167114054254623\/2022-06-02.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/gpHmmKxaGsSCeXUGA",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1192412630?c=15.00,0,0,0,dh",
            "OneLiner":"뒷풀이 장소로도 좋고 시켜먹기도 좋은 치킨집"
          },
          {
            "name":"바코드",
            "address":"서울특별시 서대문구 연세로9길 26 지하1층",
            "category":"주점",
            "trav_time":2,
            "place":"신촌",
            "avg_Price":18000,
            "tags":[
              "바",
              "술"
            ],
            "times":[
              "18:00",
              "02:00"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1046418973954158612\/1156788733526409237\/image0.jpg?ex=65163ef6&is=6514ed76&hm=9304109b70aec975b23f03e4b896e9c3cc9ea23d302d7d72038758ad6a1d2100&",
            # # "MapLink":"",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1687470326?c=15.00,0,0,0,dh",
            "OneLiner":"장소가 작아서 사람 수 제한있음."
          },
          {
            "name":"방콕익스프레스",
            "address":"서울특별시 서대문구 창천동 백송 빌딩",
            "category":"기타",
            "trav_time":2,
            "place":"신촌",
            "avg_Price":10500,
            "tags":[
              "태국",
              "팟타이",
              "뿌팟퐁커리"
            ],
            "times":[
              "11:30",
              "14:00",
              "14:30",
              "21:00"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1022464938800857098\/1116197210313465906\/997F7E505EB2F8E702.jpg",
            "MapLink":"https:\/\/maps.app.goo.gl\/Q93UcskJeDNzsLTv7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/36860497?c=15.00,0,0,0,dh",
            "OneLiner":"가성비 괜찮았던 태국음식점. 그래도 여전히 맛있다."
          },
          {
            "name":"베가니끄",
            "address":"서울특별시 서대문구 대현동 이화여대길 52-35",
            "category":"간식",
            "trav_time":2,
            "place":"이대",
            "avg_Price":5000,
            "tags":[
              "카페",
              "비건"
            ],
            "times":[
              "12:30",
              "21:30"
            ],
            "image":"https:\/\/mblogthumb-phinf.pstatic.net\/MjAyMjA3MzFfMjg5\/MDAxNjU5MjUzODgyMjcw.HJTaYsGgKvGrbuztDBiPJvOVUp659zyCTAJ2OsqfqNkg.tXaCHi094s-p36oiOW1dmW2ZsHGa5se4ABXPmML_VS0g.JPEG.ygyg612\/IMG_6272.jpg?type=w800",
            "MapLink":"https:\/\/goo.gl\/maps\/RvCtab1NYY76Xdjt8",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1226537306?c=15.00,0,0,0,dh",
            "OneLiner":"이화여대 맛집게시판 기준 별점 5점. 방문 후 후기 부탁드립니다."
          },
          {
            "name":"베이스캠프",
            "address":"서울특별시 마포구 서교동 395-111번지",
            "category":"한식",
            "trav_time":3,
            "place":"합정",
            "avg_Price":19300,
            "tags":[
              "돼지고기구이"
            ],
            "times":[
              "11:00",
              "01:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090601252506833047\/2021-11-26.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/D9kSeHYhcCh1xX6R9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/37542231?c=15.00,0,0,0,dh",
            "OneLiner":"목살, 삼겹살, 돼지껍데기를 무한리필해주는 최고의 회식장소 (4인추천)"
          },
          {
            "name":"봉구스 밥버거",
            "address":"서울특별시 마포구 신수동 23-1",
            "category":"기타",
            "trav_time":0,
            "place":"서강",
            "avg_Price":4500,
            "tags":[
              "밥버거"
            ],
            "times":[
              "10:00",
              "20:50"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090602157570535584\/2022-10-25.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/sdX9subpyt9c9rDv6",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1768866565?c=15.00,0,0,0,dh",
            "OneLiner":"배고픈 대학원생들의 눈물젖은 한 끼"
          },
          {
            "name":"불밥",
            "address":"서울특별시 서대문구 대현동 60-51",
            "category":"한식",
            "trav_time":2,
            "place":"이대",
            "avg_Price":9100,
            "tags":[
              "불오징어",
              "불닭"
            ],
            "times":[
              "11:00",
              "15:00",
              "16:00",
              "21:30"
            ],
            "image":"https:\/\/mblogthumb-phinf.pstatic.net\/MjAxODA1MjRfMjA2\/MDAxNTI3MDkxNTc1MTQ0.JuDIOR3z2JJfEaH1C-_ImceDU-sEmfMWdo5jX1OHzI0g.HRsOZ3phcRV_-2Mb4zVQRyuaRPwmkJSfIKjjIj9RRZkg.JPEG.ye0n_d\/DSC03539.JPG?type=w800",
            "MapLink":"https:\/\/goo.gl\/maps\/nVwXtUYYrNx2cjfG6",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/11594306?c=15.00,0,0,0,dh",
            "OneLiner":"이화여대 맛집게시판 기준 별점 5점. 방문 후 후기 부탁드립니다."
          },
          {
            "name":"블루포트",
            "address":"서울특별시 서대문구 이화여대길 52",
            "category":"간식",
            "trav_time":2,
            "place":"이대",
            "avg_Price":2700,
            "tags":[
              "카페"
            ],
            "times":[
        
            ],
            "image":"https:\/\/mblogthumb-phinf.pstatic.net\/MjAyMTAzMTFfOTUg\/MDAxNjE1NDQ2MzE0ODE5.V1A550-RbxjB-7ZpXGvEN_ddleAbPtdO5rzf7YEGEn8g.fJSBWNOPpn--dynSTFZMEOZMJVMgvTuut3YDxgDjPH8g.JPEG.dmgkgk2080\/KakaoTalk_20210311_135240223_08.jpg?type=w800",
            "MapLink":"https:\/\/m.place.naver.com\/restaurant\/1325090108\/home",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1325090108?c=15.00,0,0,0,dh",
            "OneLiner":"이화여대 맛집게시판 기준 별점 5점. 방문 후 후기 부탁드립니다."
          },
          {
            "name":"살사리까",
            "address":"서울특별시 마포구 양화로11길 22",
            "category":"양식",
            "trav_time":3,
            "place":"합정",
            "avg_Price":13300,
            "tags":[
              "가정식",
              "멕시코",
              "본토의_맛"
            ],
            "times":[
              "11:30",
              "15:00",
              "17:00",
              "22:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090175560925331506\/IMG_4490.JPG",
            "MapLink":"https:\/\/goo.gl\/maps\/8DebwgdMFPW17sUB6",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1045321111?c=15.00,0,0,0,dh",
            "OneLiner":"타코, 퀘사디아 등등 별의별 음식 다 있음"
          },
          {
            "name":"샤브로21 신촌",
            "address":"서울 서대문구 연세로7안길 46 1층",
            "category":"일식",
            "trav_time":2,
            "place":"신촌",
            "avg_Price":7800,
            "tags":[
              "샤브샤브",
              "가성비"
            ],
            "times":[
              "11:00",
              "22:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1146588346139824308\/1160880625163714590\/BBFEBAEABBFEBAEA_BBFEBAEAB7CE21.png?ex=65364555&is=6523d055&hm=ac6ae5f5b755bfed56abc16a9456c722791f2c8ffc1fe9dc209fd1fab09c4028&",
            # # "MapLink":"",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1627373220?c=13.00,0,0,0,dh",
            "OneLiner":"1인 샤브샤브. 가성비 최고!"
          },
          {
            "name":"샨샨",
            "address":"서울 마포구 숭문길 43 1층",
            "category":"중식",
            "trav_time":1,
            "place":"서강",
            "avg_Price":9000,
            "tags":[
              "짜장면",
              "고기짬뽕",
              "마파두부",
              "가지덮밥"
            ],
            "times":[
              "11:30",
              "15:00",
              "17:00",
              "21:00"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1146588346139824308\/1160883171596963840\/image.png?ex=653647b4&is=6523d2b4&hm=aef2d081a0608f15419bc3a79e2ff82f22e02b9b52de66d08559f766e83f62a0&=&width=739&height=531",
            # # "MapLink":"",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1136522561?c=14.72,0,0,0,dh",
            "OneLiner":"취향을 타지만 다양하게 맛있는 중식당"
          },
          {
            "name":"서브웨이",
            "address":"서울특별시 마포구 백범로 21 1층 1호",
            "category":"양식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":9800,
            "tags":[
              "샌드위치"
            ],
            "times":[
              "08:00",
              "22:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1089910486901993563\/EC849CEBB88CEC9BA8EC9DB4EBA19CEAB3A0_02.png",
            "MapLink":"https:\/\/goo.gl\/maps\/zP7hHSKpENXfhLG26",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1842171390?c=15.00,0,0,0,dh",
            "OneLiner":"변하지 않는 샌드위치계의 베이스라인. 누군가는 갈아서 마신다 카더라."
          },
          {
            "name":"세끼김밥",
            "address":"서울특별시 마포구 대흥동 286",
            "category":"한식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":4500,
            "tags":[
              "분식"
            ],
            "times":[
              "08:00",
              "15:00",
              "16:00",
              "20:00"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1046418973954158612\/1159081198694453298\/18f517a802b911ed8e6d0242ac110004.jpg?ex=651e95fc&is=651d447c&hm=90a6077549122cec0b630b5337e6e99f8d183d0a2ccbf7d3099290c1fe6fcbf0&",
            "MapLink":"https:\/\/goo.gl\/maps\/8TAxYX5Jh6zxfKZ36",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1223023730?c=15.00,0,0,0,dh",
            "OneLiner":"정문에 촌뜨기, 남문에 도샌, 대흥에 세끼"
          },
          {
            "name":"소구장",
            "address":"서울특별시 마포구 신수동 1-31",
            "category":"한식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":3600,
            "tags":[
              "떡볶이"
            ],
            "times":[
              "15:00",
              "22:00"
            ],
            "image":"https:\/\/lh3.googleusercontent.com\/p\/AF1QipPnimmFXZ17s_2HPUIJYFkGr6KBFJtVe_7Cvx1S=s0",
            "MapLink":"https:\/\/goo.gl\/maps\/g1CGkMog2gbYjMmBA",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1846586300?c=15.00,0,0,0,dh",
            "OneLiner":"떡볶퀸도 인정한 거구장 바로 앞 떡볶이 노점상."
          },
          {
            "name":"수엠부",
            "address":"서울특별시 마포구 신수동 81-54번지",
            "category":"기타",
            "trav_time":0,
            "place":"서강",
            "avg_Price":10500,
            "tags":[
              "카레",
              "난",
              "인도",
              "본토의_맛"
            ],
            "times":[
              "11:00",
              "21:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090166205538648157\/20210511_182350.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/CKg3XN4ETanWCK3J7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/37844952?c=15.00,0,0,0,dh",
            "OneLiner":"이색 밥약장소(음식 특성 상 초면 밥약하기에는 좀 애매할 수도 있음)"
          },
          {
            "name":"수저가",
            "address":"서울특별시 마포구 광성로4길 10",
            "category":"중식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":14000,
            "tags":[
              "짜장면",
              "짬뽕",
              "차돌짬뽕",
              "국물_공짜"
            ],
            "times":[
              "10:30",
              "15:00",
              "16:00",
              "20:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1089790288538632272\/495568_1515510553259_87074.png",
            "MapLink":"https:\/\/goo.gl\/maps\/VJw9Cy14t9NowK937",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1644340985?c=15.00,0,0,0,dh",
            "OneLiner":"근방 1km 이내 최고의 중국집"
          },
          {
            "name":"순이네 칼국수",
            "address":"서울특별시 마포구 대흥동 대흥로 114-1",
            "category":"한식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":8000,
            "tags":[
              "칼국수"
            ],
            "times":[
              "08:30",
              "22:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090900352326451220\/2022-10-05.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/3KgMJ8oQtz3WHaNy9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/20929090?c=15.00,0,0,0,dh",
            "OneLiner":"변함없는 맛, 엄청난 양, 부담없는 가격"
          },
          {
            "name":"술탄커피",
            "address":"서울특별시 마포구 백범로 89-4",
            "category":"간식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":5200,
            "tags":[
              "카페",
              "술",
              "서강대생_할인"
            ],
            "times":[
              "08:00",
              "22:00"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1046418973954158612\/1159081417511272498\/c7bbd93efac111ec8e6d0242ac110004.jpg?ex=651e9630&is=651d44b0&hm=be076c9fbedff0d1f8add1926d803cdd33a8cd77869ea7b598d0b8a974e1915a&",
            "MapLink":"https:\/\/goo.gl\/maps\/TW2zt61sztipKnMQ9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/38487719?c=15.00,0,0,0,dh",
            "OneLiner":"스벅 가기 싫을 때 들르면 되게 좋습니다. + 서강대생 10% 할인합니다! "
          },
          {
            "name":"숲길해장",
            "address":"서울특별시 마포구 대흥동 248-13번지 1층",
            "category":"한식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":24200,
            "tags":[
              "해장국"
            ],
            "times":[
        
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090172451872309359\/2021-12-18.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/Kju4PAFdm8zhoZVk9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1998832713?c=15.00,0,0,0,dh",
            "OneLiner":"양평해장국 맛집. 비올때 가면 낭만있음."
          },
          {
            "name":"슈퍼두퍼 버거",
            "address":"서울특별시 마포구 동교동 159-1",
            "category":"양식",
            "trav_time":3,
            "place":"홍대",
            "avg_Price":13400,
            "tags":[
              "햄버거"
            ],
            "times":[
              "10:30",
              "22:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1022464938800857098\/1114373769700589658\/2d864c97-d66c-4bc6-a70c-bf1077f5b149.jpg",
            "MapLink":"https:\/\/g.co\/kgs\/M56YH2",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1349823588?c=15.00,0,0,0,dh",
            "OneLiner":"햄버거랑 사이드랑 쉐이크랑 다 맛있는데 비쌈."
          },
          {
            "name":"슈퍼파인",
            "address":"서울특별시 서대문구 신촌역로 17 1층",
            "category":"기타",
            "trav_time":2,
            "place":"이대",
            "avg_Price":2800,
            "tags":[
              "브런치",
              "샌드위치"
            ],
            "times":[
              "10:00",
              "20:00"
            ],
            "image":"https:\/\/mp-seoul-image-production-s3.mangoplate.com\/931158_1647532925794152.jpg?fit=around|512:512&crop=512:512;*,*&output-format=jpg&output-quality=80",
            "MapLink":"https:\/\/goo.gl\/maps\/EeULkgWXWTTJegTU9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1202078058?c=15.00,0,0,0,dh",
            "OneLiner":"이화여대 맛집게시판 기준 별점 5점. 방문 후 후기 부탁드립니다."
          },
          {
            "name":"신촌칼국수",
            "address":"서울특별시 신촌로 124",
            "category":"한식",
            "trav_time":1,
            "place":"신촌",
            "avg_Price":12000,
            "tags":[
              "칼국수",
              "샤브샤브"
            ],
            "times":[
              "09:00",
              "23:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090898968621351005\/2023-03-08.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/duTva13uHFx4PXud6",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1018581179?c=15.00,0,0,0,dh",
            "OneLiner":"칼국수 사리 무한리필되는 샤브샤브 칼국수집."
          },
          {
            "name":"아피시온",
            "address":"서울특별시 마포구 서교동 368-34",
            "category":"주점",
            "trav_time":3,
            "place":"합정",
            "avg_Price":11000,
            "tags":[
              "술",
              "바",
              "하츠네미쿠"
            ],
            "times":[
              "17:00",
              "23:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090175303143395348\/20230303_184444.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/Wo3vDvj7kSPZShw88",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1238274157?c=15.00,0,0,0,dh",
            "OneLiner":"みくみくにしてあげる♪~ 소문의 미쿠바"
          },
          {
            "name":"야마노라멘",
            "address":"서울특별시 서대문구 명물1길 2 ",
            "category":"일식",
            "trav_time":2,
            "place":"신촌",
            "avg_Price":5000,
            "tags":[
              "라멘",
              "가성비"
            ],
            "times":[
              "11:00",
              "16:30",
              "17:00",
              "19:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1089794358838054972\/SE-eea7160e-de5a-4e6d-9538-6713e8893a0c.png",
            "MapLink":"https:\/\/goo.gl\/maps\/Uqkafrr9Ww9kyAPs9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1143616128?c=15.00,0,0,0,dh",
            "OneLiner":"가성비 갑 라멘집"
          },
          {
            "name":"양지분식",
            "address":"서울특별시 마포구 대흥동 37-8",
            "category":"한식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":5900,
            "tags":[
              "덮밥,찌개",
              "분식"
            ],
            "times":[
        
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090900144054075453\/2021-01-22.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/prCifZcMVhheaxAh7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/20898424?c=15.00,0,0,0,dh",
            "OneLiner":"너무 배고픈데 \"밥\" 이 먹고싶은 경우 추천합니다."
          },
          {
            "name":"여우골초밥",
            "address":"서울특별시 서대문구 신촌동 연세로5다길 10",
            "category":"일식",
            "trav_time":2,
            "place":"신촌",
            "avg_Price":24600,
            "tags":[
              "초밥"
            ],
            "times":[
              "11:30",
              "22:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090166778010804294\/2022-06-20.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/13jfwz3PZvjmQRPb7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/31253999?c=15.00,0,0,0,dh",
            "OneLiner":"서강대생 연대생 모두 오순도순 손잡고 가는 가성비 초밥집"
          },
          {
            "name":"연어초밥",
            "address":"서울특별시 서대문구 이화여대1길 42-1 3층",
            "category":"일식",
            "trav_time":2,
            "place":"이대",
            "avg_Price":13300,
            "tags":[
              "초밥",
              "연어"
            ],
            "times":[
              "11:30",
              "14:30",
              "17:00",
              "20:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090172572102045807\/2022-09-06.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/AwSr2cdWYE3Di4SS6",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1221500434?c=15.00,0,0,0,dh",
            "OneLiner":"매우 직관적이고 간결한 식당 이름. 맛있는데 가성비도 챙겼다!"
          },
          {
            "name":"옐로우피자",
            "address":"서울특별시 마포구 신수동 광성로 28",
            "category":"양식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":17800,
            "tags":[
              "피자",
              "가성비"
            ],
            "times":[
              "11:00",
              "15:00",
              "17:00",
              "21:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1089808914473816094\/output_2930805925.png",
            "MapLink":"https:\/\/goo.gl\/maps\/MmCqj4QRp58BFxCY8",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/35272001?c=14.00,0,0,0,dh",
            "OneLiner":"서강대가 키운 피자 맛집"
          },
          {
            "name":"옥면가",
            "address":"서울특별시 마포구 염리동 백범로26길 4-5",
            "category":"한식",
            "trav_time":1,
            "place":"서강",
            "avg_Price":10400,
            "tags":[
              "옥수수면"
            ],
            "times":[
              "11:00",
              "14:00",
              "17:00",
              "21:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090163809676693504\/2023-03-15.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/SHBA11akzRe7vkzv7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1773162927?c=15.00,0,0,0,dh",
            "OneLiner":"옥수수면 + 통장각(닭다리)를 나름 저렴하게 먹을 수 있는 최고 맛집"
          },
          {
            "name":"옥정",
            "address":"서울특별시 마포구 신수동 신수로 106",
            "category":"한식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":11400,
            "tags":[
              "칼국수",
              "만두"
            ],
            "times":[
              "11:30",
              "14:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090164481377701898\/2023-01-09.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/NzmWoVTzp1GqgdSB6",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/37046010?c=15.00,0,0,0,dh",
            "OneLiner":"칼국수나 만두국이 생각나는 겨울에 딱 좋은 장소! (점심시간에만 염)"
          },
          {
            "name":"올디스타코",
            "address":"서울특별시 중구 충무로4길 3",
            "category":"양식",
            "trav_time":3,
            "place":"을지로",
            "avg_Price":7000,
            "tags":[
              "타코"
            ],
            "times":[
              "12:00",
              "15:30",
              "17:00",
              "21:00"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1046418973954158612\/1129687448344076358\/SE-40bfcdbf-d2f5-4350-93f2-d44d8b43c079.jpg",
            "MapLink":"https:\/\/g.co\/kgs\/5R7QN9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1253387841?c=15.00,0,0,0,dh",
            "OneLiner":"ㄹㅇ 미쳤음"
          },
          {
            "name":"옹고집",
            "address":"서울특별시 마포구 노고산동 31-110",
            "category":"주점",
            "trav_time":1,
            "place":"서강",
            "avg_Price":16300,
            "tags":[
              "닭볶음탕",
              "뒷풀이"
            ],
            "times":[
        
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1089813147080208466\/167781_1569689957071_69549.png",
            "MapLink":"https:\/\/goo.gl\/maps\/D1YmmGX2LZAkQy5D6",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/18329717?c=15.00,0,0,0,dh",
            "OneLiner":"술 마시고 싶을 때 사람이 많을 경우 유일한 선택지."
          },
          {
            "name":"용싸키친",
            "address":"서울특별시 마포구 신수동 25-2",
            "category":"기타",
            "trav_time":0,
            "place":"서강",
            "avg_Price":8800,
            "tags":[
              "스테이크덮밥",
              "김치볶음밥",
              "카레우동"
            ],
            "times":[
              "11:00",
              "22:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090601979899805706\/2020-10-13.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/5AEJUwfXdHr6PcSx8",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/20034184?c=15.00,0,0,0,dh",
            "OneLiner":"없는게 없는 식당. 점심시간에 이 식당 손님 평균학력이 기하급수적으로 올라간다 카더라."
          },
          {
            "name":"원더풀 샤브샤브",
            "address":"서울특별시 마포구 신수동 457",
            "category":"중식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":12600,
            "tags":[
              "짜장면",
              "짬뽕",
              "볶음밥",
              "꿔바로우",
              "유니마늘쫑면"
            ],
            "times":[
              "11:30",
              "15:00",
              "17:00",
              "21:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090638433120170125\/2017-02-21.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/eyxSyT8tAixbTt9D7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/13360128?c=15.00,0,0,0,dh",
            "OneLiner":"회식 가능 중국집. 볶음밥, 흰 짬뽕, 꿔바로우가 주력이다."
          },
          {
            "name":"월화식당",
            "address":"서울특별시 마포구 도화길 29 1, 2층",
            "category":"한식",
            "trav_time":2,
            "place":"공덕",
            "avg_Price":18000,
            "tags":[
              "고기"
            ],
            "times":[
              "16:00",
              "23:00"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1046418973954158612\/1156785951490703441\/image0.jpg?ex=65163c5e&is=6514eade&hm=3326fcc81ba5bf1f4abe9dec2c3acd9df9d9e7c1b088dc340e837c86a2a95e40&",
            # "MapLink":"",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1905133643?c=18.38,0,0,0,dh",
            "OneLiner":"소금이 기가 막혀"
          },
          {
            "name":"웰빙숯불생고기",
            "address":"서울특별시 마포구 신수동 91-385",
            "category":"한식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":12000,
            "tags":[
              "고기",
              "찌개"
            ],
            "times":[
              "11:00",
              "01:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090899968677646356\/2021-11-07.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/dkhW6nn1WGxaBnv49",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/18776563?c=15.00,0,0,0,dh",
            "OneLiner":"고기도 맛있지만 김치찌개도 맛있습니다."
          },
          {
            "name":"유",
            "address":"서울특별시 서대문구 대현동 이화여대길 65-3",
            "category":"중식",
            "trav_time":2,
            "place":"이대",
            "avg_Price":11700,
            "tags":[
              "중식"
            ],
            "times":[
              "11:00",
              "14:30",
              "16:00",
              "19:30"
            ],
            "image":"https:\/\/emmaru.com\/matzip\/include\/pics\/2021\/10\/10\/m_89144E202456_1.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/F4XGHsENPUWKRiN47",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/37585750?c=15.00,0,0,0,dh",
            "OneLiner":"이화여대 맛집게시판 기준 별점 5점. 방문 후 후기 부탁드립니다."
          },
          {
            "name":"을밀대",
            "address":"서울특별시 마포구 숭문길 24",
            "category":"한식",
            "trav_time":1,
            "place":"서강",
            "avg_Price":29600,
            "tags":[
              "평양냉면",
              "호불호"
            ],
            "times":[
              "11:00",
              "22:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1089916284893921460\/99CD8E3C5C1E404439.png",
            "MapLink":"https:\/\/goo.gl\/maps\/SRJ7tCnhXESmUgBQ7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/11679611?c=15.00,0,0,0,dh",
            "OneLiner":"호불호가 극적으로 갈리는 집. 꼭 여기 가자는 사람들이 있어요"
          },
          {
            "name":"이치젠",
            "address":"서울특별시 마포구 포은로 109 101호",
            "category":"일식",
            "trav_time":3,
            "place":"마포",
            "avg_Price":8900,
            "tags":[
              "텐동"
            ],
            "times":[
              "12:00",
              "15:00",
              "17:30",
              "20:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090175101296717854\/9944C7455BAC7BB408.png",
            "MapLink":"https:\/\/goo.gl\/maps\/Di4LsdEjSiH82Dpq9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/993406814?c=15.00,0,0,0,dh",
            "OneLiner":"느끼하지 않은 텐동집. 여기 간장을 따로 파는데 ㄹㅇ 밥도둑."
          },
          {
            "name":"이태리 부대찌개",
            "address":"서울특별시 마포구 신수동 백범로 36",
            "category":"한식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":30500,
            "tags":[
              "부대찌개"
            ],
            "times":[
              "11:00",
              "15:00",
              "16:00",
              "21:00"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1022464938800857098\/1116197992924450866\/750_750_20221211092740_photo1_f845b5a58a5c.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/FY8PAqbBfApuBfNL7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1643092709?c=15.00,0,0,0,dh",
            "OneLiner":"정문에서 완전 가까운 부대찌개, 1시 이후 혼밥 가능!"
          },
          {
            "name":"정든그릇",
            "address":"서울특별시 마포구 독막로 239 1층 101호",
            "category":"일식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":9600,
            "tags":[
              "퓨전일식"
            ],
            "times":[
              "11:30",
              "15:00",
              "17:00",
              "20:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090164915601428551\/08B9262C-952A-4913-A43C-BE756846314C.jpeg",
            "MapLink":"https:\/\/goo.gl\/maps\/zm986Ry2AyXrKPnS6",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1288392698?c=15.00,0,0,0,dh",
            "OneLiner":"메뉴가 다양해서 자주 들르기 좋음, 대신 재료 소진 시 영업종료 - 저녁엔 못 간다고 봐야할 듯"
          },
          {
            "name":"정육면체",
            "address":"서울특별시 서대문구 연세로5다길 22-8",
            "category":"일식",
            "trav_time":2,
            "place":"신촌",
            "avg_Price":8000,
            "tags":[
              "탄탄멘"
            ],
            "times":[
              "11:30",
              "20:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1089809434928222309\/75223_1592357220417420.png",
            "MapLink":"https:\/\/goo.gl\/maps\/9m3CANEhWgRPY6N17",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1229208931?c=14.00,0,0,0,dh",
            "OneLiner":"미슐랭 선정 탄탄면 맛집"
          },
          {
            "name":"족발야시장",
            "address":"서울특별시 마포구 신수동 번지 지 457 벽산이-솔렌스힐아파트 2층 105호",
            "category":"한식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":42200,
            "tags":[
              "덮밥",
              "보쌈",
              "찌개",
              "라면"
            ],
            "times":[
              "11:30",
              "23:50"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1022464938800857098\/1116198380356522096\/750_750_20221121073240094_photo_cc3c9a806e41.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/89nMiGtRREeCZMnJ7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1687285363?c=15.00,0,0,0,dh",
            "OneLiner":"보쌈정식, 마포쌈밥보다 싸다! 원래는 족발집이지만 점심메뉴 한정 미가 2호기. 혼밥인데 얼음물 나옴. 원샤 옆. (점심메뉴 11:30~17:00)"
          },
          {
            "name":"진돈부리",
            "address":"서울특별시 서대문구 신촌로 149 자이엘라 B104",
            "category":"일식",
            "trav_time":2,
            "place":"이대",
            "avg_Price":12100,
            "tags":[
              "덮밥",
              "동",
              "연어"
            ],
            "times":[
              "12:00",
              "14:00",
              "16:30",
              "21:00"
            ],
            "image":"https:\/\/mblogthumb-phinf.pstatic.net\/MjAyMjA1MDhfMTY3\/MDAxNjUxOTM2Mjk0NzQy.lVDKf2uttHywbDziXRrz8pFKNFnfLbum36XYB16Uk6Qg.s6CfrEOpcnof8fqJEMEmvaM_jD-d4VJgRcDQI_usBgog.JPEG.shcj0519\/1651936279429.jpg?type=w800",
            "MapLink":"https:\/\/goo.gl\/maps\/5UfEnmAKr6pVjhnw9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1674726200?c=15.00,0,0,0,dh",
            "OneLiner":"연어덮밥 최고 맛집."
          },
          {
            "name":"짜장상회",
            "address":"서울특별시 마포구 신수동 백범로 52",
            "category":"중식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":5200,
            "tags":[
              "짜장면"
            ],
            "times":[
              "11:00",
              "15:30",
              "16:30",
              "20:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090898639460778044\/2022-04-06.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/2c12TKVQRyfSvAdA6",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/856641183?c=15.00,0,0,0,dh",
            "OneLiner":"갓성비 짜장면집"
          },
          {
            "name":"짬뽕지존 홍대점",
            "address":"서울 마포구 어울마당로 44-1 1층",
            "category":"중식",
            "trav_time":3,
            "place":"홍대",
            "avg_Price":12000,
            "tags":[
              "짬뽕",
              "수제비짬뽕"
            ],
            "times":[
              "00:00",
              "24:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1146588346139824308\/1160878571838001222\/1651306419014.png?ex=6536436b&is=6523ce6b&hm=aa554db6fbcb86f9f84208c79796cd50ecb25788162e36e8f40572db9a29154e&",
            # "MapLink":"",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1811586372?c=15.00,0,0,0,dh",
            "OneLiner":"수제비짬뽕이라는 이색 메뉴를 팝니다."
          },
          {
            "name":"쭈꾸미블루스",
            "address":"서울 마포구 백범로1길 21",
            "category":"한식",
            "trav_time":1,
            "place":"신촌",
            "avg_Price":16000,
            "tags":[
              "쭈꾸미",
              "홍합탕",
              "쭈삼"
            ],
            "times":[
              "11:30",
              "15:00",
              "17:00",
              "22:00"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1146588346139824308\/1160872685283328040\/common.png?ex=65363df0&is=6523c8f0&hm=5becb4387af4e890ed393f4f3f038543677ea40241c888018d7b28ae39404ce2&=&width=732&height=549",
            # "MapLink":"",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/35849217?c=18.38,0,0,0,dh",
            "OneLiner":"매운거 좋아하는 2-4명이 가면 좋은 곳"
          },
          {
            "name":"천하의 문타로",
            "address":"서울특별시 마포구 동교동 203-26",
            "category":"주점",
            "trav_time":3,
            "place":"홍대",
            "avg_Price":23800,
            "tags":[
              "이자카야",
              "술"
            ],
            "times":[
              "18:00",
              "00:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090174599817347132\/SmartSelect_20230328_162425_Instagram.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/R5kssz451EtaLw7c7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/34806924?c=15.00,0,0,0,dh",
            "OneLiner":"홍대 근처 최고의 이자카야라고 장담합니다. 사케는 아카부."
          },
          {
            "name":"청석골",
            "address":"서울특별시 마포구 노고산동 31-90",
            "category":"한식",
            "trav_time":1,
            "place":"서강",
            "avg_Price":17800,
            "tags":[
              "감자탕",
              "뼈해장국"
            ],
            "times":[
              "10:00",
              "22:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090603008112480347\/2022-12-18.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/3gadMCEKDW5qtyvc7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/32466789?c=15.00,0,0,0,dh",
            "OneLiner":"\"뼈석골\"이라 부르는 사람은 화석입니다."
          },
          {
            "name":"츠키젠",
            "address":"서울특별시 마포구 독막로8길 23",
            "category":"일식",
            "trav_time":3,
            "place":"합정",
            "avg_Price":14500,
            "tags":[
              "돈카츠"
            ],
            "times":[
              "11:30",
              "15:00",
              "17:00",
              "21:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090601064631369768\/2021-04-03.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/Px1t2h6k4pihk4Mh6",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1172910030?c=15.00,0,0,0,dh",
            "OneLiner":"만돈보다 맛있다!"
          },
          {
            "name":"치즈밥있슈",
            "address":"서울특별시 마포구 염리동 숭문길 98",
            "category":"한식",
            "trav_time":1,
            "place":"서강",
            "avg_Price":6200,
            "tags":[
              "치즈덮밥"
            ],
            "times":[
              "10:00",
              "21:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1022464938800857098\/1090898084931829841\/2019-12-06.jpg",
            "MapLink":"https:\/\/maps.app.goo.gl\/G43vptKmMzh4yAiy7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1062359035?c=15.00,0,0,0,dh",
            "OneLiner":"값도 싼데 치즈가 기본으로 들어간다?!"
          },
          {
            "name":"카라멘야",
            "address":"서울특별시 서대문구 연세로7안길 34-1 1층",
            "category":"일식",
            "trav_time":2,
            "place":"신촌",
            "avg_Price":7600,
            "tags":[
              "라멘"
            ],
            "times":[
              "11:30",
              "15:30",
              "17:00",
              "21:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1089806078826528810\/2019EB8584_08EC9B94_07EC9DBC_EC8BA0ECB48C_ECB9B4EB9DBCEBA998EC95BC_00.png",
            "MapLink":"https:\/\/goo.gl\/maps\/zDhexEYGcnWidfik7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1767701213?c=15.00,0,0,0,dh",
            "OneLiner":"누군가가 동방에서 매일 배달시켜먹는 라멘집"
          },
          {
            "name":"카와카츠 오토코",
            "address":"서울특별시 마포구 서교동 395 154",
            "category":"일식",
            "trav_time":3,
            "place":"합정",
            "avg_Price":14000,
            "tags":[
              "돈카츠"
            ],
            "times":[
              "11:30",
              "15:00",
              "17:30",
              "20:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090811367700824184\/20230325_114327.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/R2vMwpz8U2iwn3Ct7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1924306900?c=15.00,0,0,0,dh",
            "OneLiner":"돼지가 소를 이긴 날"
          },
          {
            "name":"카츠 오모이",
            "address":"서울특별시 마포구 와우산로 162-14",
            "category":"일식",
            "trav_time":2,
            "place":"홍대",
            "avg_Price":13500,
            "tags":[
              "돈카츠"
            ],
            "times":[
              "11:30",
              "14:15"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090601379950772255\/2022-03-17.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/Ah1nxChad1UiXjFX9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1376612537?c=15.00,0,0,0,dh",
            "OneLiner":"고기는 평균 이상이지만 밥이 먼저나와서 실제로 먹을때에는 좀 마르게 됨."
          },
          {
            "name":"카츠오우 공덕점",
            "address":"서울특별시 마포구 마포대로10길 11 1층",
            "category":"일식",
            "trav_time":2,
            "place":"공덕",
            "avg_Price":11000,
            "tags":[
              "돈카츠",
              "카레",
              "돈부리",
              "나베"
            ],
            "times":[
              "11:00",
              "15:00",
              "17:00",
              "21:00"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1046418973954158612\/1156788528617893959\/image0.jpg?ex=65163ec5&is=6514ed45&hm=6107310474265e76a8271c94d4c814af9962c6f1ab0b0821188ec07b52a852fa&",
            # "MapLink":"",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1041155881?c=18.38,0,0,0,dh",
            "OneLiner":"생각나는 일식 메뉴는 다 있는 그런 곳."
          },
          {
            "name":"카페 나팔꽃",
            "address":"서울 마포구 독막로 147-14 1층",
            "category":"간식",
            "trav_time":1,
            "place":"서강",
            "avg_Price":4500,
            "tags":[
              "카페"
            ],
            "times":[
              "10:00",
              "19:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1146588346139824308\/1160876671189135441\/20230729_133835.jpg?ex=653641a6&is=6523cca6&hm=c4fbb53124b7752503a2be4b1f993dba8ddc129c3bfb13cadb9f63808d15329c&",
            # "MapLink":"",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1497691822?placePath=%2Fhome&c=15.00,0,0,0,dh",
            "OneLiner":"커피도 맛있지만 시즌 메뉴가 진국."
          },
          {
            "name":"카페아늑",
            "address":"서울특별시 서대문구 대현동 37-59번지",
            "category":"간식",
            "trav_time":2,
            "place":"이대",
            "avg_Price":5700,
            "tags":[
              "카페"
            ],
            "times":[
              "11:00",
              "22:00"
            ],
            "image":"https:\/\/mblogthumb-phinf.pstatic.net\/MjAyMTA0MDdfMjMw\/MDAxNjE3NzcyMDI2NzI2.jVeFdXDjiarRc3d3OMoYAMhiCKAxsJhNf3xUPSWorCEg.YngnKtNdLMoQBg7ALvynaQS6YfQiSweij5lLZGRrnjIg.JPEG.thddl5414\/IMG_4498.jpg?type=w800",
            "MapLink":"https:\/\/goo.gl\/maps\/coh6nBHFCmfL978v5",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/37812798?c=15.00,0,0,0,dh",
            "OneLiner":"이화여대 맛집게시판 기준 별점 5점. 방문 후 후기 부탁드립니다."
          },
          {
            "name":"카페올리브",
            "address":"서울 마포구 독막로28길 46",
            "category":"간식",
            "trav_time":2,
            "place":"서강",
            "avg_Price":5000,
            "tags":[
              "카페",
              "빙수"
            ],
            "times":[
              "9:30",
              "20:00"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1146588346139824308\/1160881741855199242\/image.png?ex=6536465f&is=6523d15f&hm=d49a47d07b1364bc41b195b38344e747f7ce84ba1fa33f95a1d715c4399b18eb&=&width=907&height=549",
            # "MapLink":"",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1534442753?c=14.72,0,0,0,dh",
            "OneLiner":"육각형 스탯이 큰 카페"
          },
          {
            "name":"카페코지",
            "address":"서울특별시 서대문구 이화여대길 88-19",
            "category":"간식",
            "trav_time":2,
            "place":"이대",
            "avg_Price":3400,
            "tags":[
              "카페"
            ],
            "times":[
              "10:00",
              "20:00"
            ],
            "image":"https:\/\/d12zq4w4guyljn.cloudfront.net\/750_750_20221203111136888_photo_7d22c69bdc89.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/Usf9oF7GN9m2Ehyt8",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1366550708?c=15.00,0,0,0,dh",
            "OneLiner":"이화여대 맛집게시판 기준 별점 5점. 방문 후 후기 부탁드립니다."
          },
          {
            "name":"코코가츠",
            "address":"서울특별시 마포구 백범로 68 1층 코코가츠",
            "category":"일식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":8000,
            "tags":[
              "돈까스"
            ],
            "times":[
              "10:30",
              "20:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090164028145401946\/20220214_122740.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/3zYpakt8j8PnK9aL8",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/20419231?c=15.00,0,0,0,dh",
            "OneLiner":"생각없이 3~4인이서 가기 좋은 돈가스집"
          },
          {
            "name":"쿠츠(고이짱)",
            "address":"서울특별시 마포구 백범로16길 25",
            "category":"한식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":11400,
            "tags":[
              "돈까스"
            ],
            "times":[
              "11:00",
              "20:00"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1046418973954158612\/1159081674177527919\/5cd1d6cabd4811ec8fe80242ac110004.jpg?ex=651e966d&is=651d44ed&hm=916deab2cfa12c5d0aa9d7a04e72fa00ee99f76cd566540346574ceb964295d5&",
            "MapLink":"https:\/\/goo.gl\/maps\/VhJ4fTW5uLosqPSL7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/732407620?c=15.00,0,0,0,dh",
            "OneLiner":"고이짱의 피를 물려받은 왕돈까쓰 맛집"
          },
          {
            "name":"크래프트한스",
            "address":"서울특별시 마포구 서교동 양화로23길 22",
            "category":"주점",
            "trav_time":3,
            "place":"홍대",
            "avg_Price":37400,
            "tags":[
              "맥주"
            ],
            "times":[
        
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090174756646563850\/2022-06-06.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/y9PJ7cTBYX44nTkn7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1646907705?c=15.00,0,0,0,dh",
            "OneLiner":"맥주에는 사실 소시지가 잘 어울린다는 사실, 알고계셨나요? 여가 와서 알아가세요!"
          },
          {
            "name":"태광식당",
            "address":"서울특별시 마포구 신수동 85-5",
            "category":"한식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":5600,
            "tags":[
              "백반"
            ],
            "times":[
        
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1046418973954158612\/1159080312106651729\/9bb06bc63aee11eda84a0242ac110004.jpg?ex=651e9529&is=651d43a9&hm=cd2c090186d1cda66c3818d8ac1ce529da536df37541231d275ee81b38cfa7ad&",
            "MapLink":"https:\/\/goo.gl\/maps\/mUyberhKPMUAw8py9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1644821089?c=15.00,0,0,0,dh",
            "OneLiner":"고시생의 낙원"
          },
          {
            "name":"포엔띠우",
            "address":"서울특별시 마포구 광성로4길 11-10",
            "category":"기타",
            "trav_time":0,
            "place":"서강",
            "avg_Price":8200,
            "tags":[
              "쌀국수"
            ],
            "times":[
              "11:00",
              "21:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090815091257114724\/2020-06-21.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/eqmu6ptMVs7ErENt9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1738019358?c=15.00,0,0,0,dh",
            "OneLiner":"포옹남보다 맛있다는 소문이..."
          },
          {
            "name":"포옹남",
            "address":"서울특별시 마포구 신수동 서강로16길 67",
            "category":"기타",
            "trav_time":0,
            "place":"서강",
            "avg_Price":10000,
            "tags":[
              "쌀국수"
            ],
            "times":[
              "11:00",
              "22:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1089810733723820062\/14650_1621837869776_12139.png",
            "MapLink":"https:\/\/goo.gl\/maps\/BWWrsPH67KdZdEZp7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1225539791?c=15.00,0,0,0,dh",
            "OneLiner":"비싸다고 하는 사람은 봤어도 맛없다고 하는 사람은 못 봄"
          },
          {
            "name":"프랭크버거",
            "address":"서울특별시 마포구 신수동 광성로 42",
            "category":"양식",
            "trav_time":1,
            "place":"서강",
            "avg_Price":5200,
            "tags":[
              "햄버거"
            ],
            "times":[
              "11:00",
              "21:00"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1089810520430891118\/3672844822_7f869740_7428329.png",
            "MapLink":"https:\/\/goo.gl\/maps\/T9fDHXxCtDabzahK9",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1443936886?c=15.00,0,0,0,dh",
            "OneLiner":"\"구...궁극의...미...미식 버거...하..하나....주세요....\""
          },
          {
            "name":"프릳츠 도화점",
            "address":"서울특별시 마포구 새창로2길 17",
            "category":"간식",
            "trav_time":2,
            "place":"공덕",
            "avg_Price":5000,
            "tags":[
              "카페",
              "빵"
            ],
            "times":[
              "8:00",
              "22:00"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1146588346139824308\/1160869696552321054\/common.png?ex=65363b27&is=6523c627&hm=3db161515636f995fd7f19928fb02ad62708e052e74e7aa26f3da3f5d829aa44&=&width=823&height=549",
            # # "MapLink":"",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/35524251?c=18.38,0,0,0,dh",
            "OneLiner":"감성 넘치는 공덕 롱블랙 맛집."
          },
          {
            "name":"피자알볼로",
            "address":"서울특별시 마포구 독막로28길 7 성원아파트",
            "category":"양식",
            "trav_time":1,
            "place":"서강",
            "avg_Price":26500,
            "tags":[
              "피자"
            ],
            "times":[
              "11:00",
              "22:30"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1046418973954158612\/1096732707775598672\/4772965322a6835690ed8f91a87c5a550da59f94e3842221909eeab5a4d93238.webp",
            "MapLink":"https:\/\/goo.gl\/maps\/QGcR7TeQkga3tDxN8",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/31690094?c=15.00,0,0,0,dh",
            "OneLiner":"생활의 달인에 나온 그 피자알볼로 프랜차이즈. 값은 좀 비싸요."
          },
          {
            "name":"하노이별",
            "address":"서울특별시 마포구 백범로 84 1층",
            "category":"기타",
            "trav_time":0,
            "place":"서강",
            "avg_Price":12800,
            "tags":[
              "쌀국수"
            ],
            "times":[
              "11:00",
              "19:30"
            ],
            "image":"https:\/\/mblogthumb-phinf.pstatic.net\/MjAyMTExMTVfMjYw\/MDAxNjM2OTU2NzY2NzU2.gLi10Z31acb2rKa_a_mi0I9__i6q3xMxofe2gX07YE4g.Y-B3VBTApikY2A1XNqeMQLyXo5Lp5wbbiFhdfiYgFHUg.JPEG.zoiia\/20211115%25EF%25BC%25BF125204.jpg?type=w800",
            "MapLink":"https:\/\/goo.gl\/maps\/Ed2LgKXsnDMs9s8JA",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1947355907?c=15.00,0,0,0,dh",
            "OneLiner":"양이 많음. 근데 쌀국수집이라 냄새가 배길 위험이 있어요"
          },
          {
            "name":"한솥",
            "address":"서울특별시 마포구 백범로 35",
            "category":"한식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":5300,
            "tags":[
              "도시락",
              "가성비"
            ],
            "times":[
              "08:30",
              "20:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1089908830093180938\/8916e2417be74a81bdca66e2a5542bb420220127081225.png",
            "MapLink":"https:\/\/goo.gl\/maps\/QsX7ta37sfoxzoGr6",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1861415841?c=15.00,0,0,0,dh",
            "OneLiner":"돈을 아끼고 싶을 때."
          },
          {
            "name":"홍대개미",
            "address":"서울특별시 서대문구 연세로 18 2층",
            "category":"일식",
            "trav_time":1,
            "place":"신촌",
            "avg_Price":12000,
            "tags":[
              "덮밥"
            ],
            "times":[
              "11:00",
              "20:20"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1022464938800857098\/1116197667853316146\/6.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/3KjiYE6QnBokZdsY7",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/880225042?c=15.00,0,0,0,dh",
            "OneLiner":"무난한 덮밥집. 큐브스테이크 덮밥이 맛있어요."
          },
          {
            "name":"홍두깨 칼국수",
            "address":"서울특별시 마포구 백범로1길 10 1층",
            "category":"한식",
            "trav_time":1,
            "place":"서강",
            "avg_Price":17200,
            "tags":[
              "칼국수"
            ],
            "times":[
              "11:00",
              "19:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090602822929764364\/20200205_093105.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/TiyWVwWFVAuQBvc9A",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/13051635?c=15.00,0,0,0,dh",
            "OneLiner":"칼국수집인데 왜인지 모르게 솥밥이 더 맛있는건 기분탓인가...."
          },
          {
            "name":"홍원",
            "address":"서울특별시 마포구 백범로 23 (신수동)",
            "category":"중식",
            "trav_time":0,
            "place":"서강",
            "avg_Price":13800,
            "tags":[
              "짜장면",
              "쟁반짜장"
            ],
            "times":[
              "11:00",
              "20:30"
            ],
            "image":"https:\/\/cdn.discordapp.com\/attachments\/1046418973954158612\/1090900586339237908\/20220312_125958.jpg",
            "MapLink":"https:\/\/goo.gl\/maps\/9XLsWru3ro3ww4N97",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/33239749?c=15.00,0,0,0,dh",
            "OneLiner":"괜찮은 중국집. 다만 새우탕면은 먹지 말자."
          },
          {
            "name":"희희",
            "address":"서울특별시 마포구 독막로 291-5",
            "category":"일식",
            "trav_time":1,
            "place":"서강",
            "avg_Price":15000,
            "tags":[
              "소바"
            ],
            "times":[
              "11:30",
              "15:00",
              "18:00",
              "22:00"
            ],
            "image":"https:\/\/media.discordapp.net\/attachments\/1046418973954158612\/1156785203507900487\/image0.jpg?ex=65163bac&is=6514ea2c&hm=5c5f3ae5cd1355e9d077e4a853338cacfab9703e4e2a6565bb422ec6f6c3ac13&",
            # "MapLink":"",
            "NaverMap":"https:\/\/map.naver.com\/p\/entry\/place\/1416540834?c=18.38,0,0,0,dh",
            "OneLiner":"경의선숲길 감성 소바집. 먹고 후기 바랍니다."
          }
        ]

        for entry in data:
            restaurant = Restaurant.objects.create(
                name=entry['name'],
                address=entry['address'],
                category=entry['category'],
                trav_time=entry['trav_time'],
                place=entry['place'],
                avg_Price=entry['avg_Price'],
                times=entry['times'],
                image=entry['image'],
                # MapLink=entry['MapLink'],
                NaverMap=entry['NaverMap'],
                OneLiner=entry['OneLiner']
            )

            for tag_name in entry['tags']:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                restaurant.tags.add(tag)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with restaurant data'))
