from django.db import models
from django.db.models import JSONField
from django.utils.timezone import now

# Create your models here.

class Building(models.Model): # 건물별 정보
    name = models.CharField(max_length=100)                         # 건물 이름
    abbr = models.CharField(max_length=16, blank=True, null=True)   # 건물 약어
    description = models.TextField(blank=True, null=True)           # 건물 설명
    facilities = JSONField(default=dict)                            # 건물 시설 정보

    def __str__(self):
        return self.name

class Facility(models.Model): # 열람실, 프린트샵, 카페 등
    building = models.ForeignKey(Building, related_name='facility', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    open_hours = models.CharField(max_length=100, blank=True, null=True)
    total_seats = models.IntegerField(null=True, blank=True)  # Null이 가능하여 열람실이 아닌 경우 좌석 수를 두지 않을 수 있음
    used_seats = models.IntegerField(null=True, blank=True)   # 사용 중인 좌석 수
    available_seats = models.IntegerField(null=True, blank=True)  # 사용 가능한 좌석 수
    facility_type = models.CharField(max_length=100)  # 예: 'reading_room', 'print_shop', 'cafe', 등

    def __str__(self):
        return f"{self.name} in {self.building.name}"


class Menu(models.Model):
    facility = models.ForeignKey(Facility, related_name='menus', on_delete=models.CASCADE)
    date = models.DateField(default=now)
    items_by_corner = JSONField(default=dict)  # Store items grouped by corners

    def __str__(self):
        return f"{self.facility.name} menu for {self.date}"
    

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=100)             # ex. 수저가
    address = models.CharField(max_length=255)          # ex. 서울특별시 마포구 광성로4길 10
    category = models.CharField(max_length=50)          # ex. 중식
    trav_time = models.IntegerField()                   # ex. 0
    place = models.CharField(max_length=50)             # ex. 서강
    avg_Price = models.IntegerField()                   # ex. 14000
    tags = models.ManyToManyField(Tag, related_name='restaurants')  # ex. ['매운', '밥맛']
    times = models.JSONField()  # ex. ["10:30", "15:00", "16:00", "20:00"]
    image = models.URLField()   
    # MapLink = models.URLField()
    NaverMap = models.URLField(max_length=512)    # 네이버 지도 주소
    OneLiner = models.TextField()   # 한줄평

    def __str__(self):
        return self.name

    def get_open_hours(self):
        if len(self.times) == 2:
            return f"Open from {self.times[0]} to {self.times[1]}"
        elif len(self.times) > 2:
            open_time = self.times[0]
            close_time = self.times[-1]
            break_times = ", ".join([f"{self.times[i]}~{self.times[i+1]}" for i in range(1, len(self.times) - 2, 2)])
            return f"Open from {open_time} to {close_time}, Break times: {break_times}"
        return "Time information not available"