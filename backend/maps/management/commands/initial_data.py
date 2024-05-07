from django.core.management.base import BaseCommand
from maps.models import Building, Facility

buildings = [
    "정문",
    "알바트로스 탑",
    "본관",
    "게페르트남덕우경제관(GN관)",
    "예수회공동체",
    "삼성가브리엘관(GA관)",
    "금호아시아나바오로경영관(PA관)",
    "토마스모어관(T관)",
    "마태오관(MA관)",
    "메리홀(M관)",
    "성이냐시오관(I관)",
    "엠마오관(E관)",
    "로욜라도서관",
    "최양업관(CY관)",
    "하비에르관(X관)",
    "다산관(D관)",
    "곤자가국제학사(GH)",
    "후문",
    "떼이야르관(TE관)",
    "정하상관(J관)",
    "포스코 프란치스코관(F관)",
    "리치별관(RA관)",
    "대운동장",
    "아담샬관(AS관)",
    "리치과학관(R관)",
    "예수회센터",
    "김대건관(K관)",
    "벨라르미노학사",
    "서강빌딩",
    "남문",
    "아루페관(AR관)",
    "체육관",
    "청년광장",
    "베르크만스 우정원(BW관)"
    ]

class Command(BaseCommand):
    help = 'Initializes the database with building and facility data'

    def find_abbr(self, building_name):
        abbr = ""
        # find alphabet in the building name, not korean
        for char in building_name:
            if 'a' <= char.lower() <= 'z':
                abbr += char
        return abbr
    

    def handle(self, *args, **options):
        # 건물 추가
        # building = Building.objects.create(name="중앙 도서관")
        # 생성하기 전에 모두 삭제
        Building.objects.all().delete()
        Facility.objects.all().delete()
        
        for building_name in buildings:
            # abbr is an alphabet in the building name
            Building.objects.create(name=building_name, abbr=self.find_abbr(building_name))
            # Building.objects.create(name=building_name)
        
        Facility.objects.create(
            building= Building.objects.get(name="김대건관(K관)"),
            name="K관 열람실",
            description="B1에 위치해 있습니다. 노트북 전용실 존재.",
            open_hours="08:00 - 20:00",
            facility_type='reading_room'
        )
        Facility.objects.create(
            building= Building.objects.get(name="김대건관(K관)"),
            name="인쇄소",
            description="3층에 위치해 있습니다. 계좌번호: 국민 123-456-7890",
            open_hours="08:00 - 20:00",
            facility_type='print_shop'
        )

        Facility.objects.create(
            building= Building.objects.get(name="정하상관(J관)"),
            name="J관 일반열람실",
            description="1층에 위치해 있습니다. 노트북 전용실 존재.",
            open_hours="08:00 - 20:00",
            facility_type='reading_room'
        )
        Facility.objects.create(
            building= Building.objects.get(name="정하상관(J관)"),
            name="인쇄소",
            description="2층에 위치해 있습니다. 계좌번호: 국민 123-456-7890",
            open_hours="08:00 - 20:00",
            facility_type='print_shop'
        )
        
        # # 중앙 도서관에 열람실 추가
        # Facility.objects.create(
        #     building=building,
        #     name="중앙 도서관 열람실",
        #     description="24시간 운영되는 열람실입니다.",
        #     open_hours="00:00 - 24:00",
        #     total_seats=120,
        #     available_seats=45,
        #     facility_type='reading_room'
        # )
        
        # # 중앙 도서관에 인쇄소 추가
        # Facility.objects.create(
        #     building=building,
        #     name="도서관 인쇄소",
        #     description="학생들의 인쇄 및 복사 요구를 충족시킵니다.",
        #     open_hours="09:00 - 18:00",
        #     facility_type='print_shop'
        # )
        
        self.stdout.write(self.style.SUCCESS('Successfully initialized the database.'))
