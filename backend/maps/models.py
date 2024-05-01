from django.db import models
from django.db.models import JSONField

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