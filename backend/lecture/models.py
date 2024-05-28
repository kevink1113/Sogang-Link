from django.db import models
import datetime
from users.models import User


class Course(models.Model):
    course_id = models.CharField(max_length=10, null=True)
    semester = models.IntegerField()
    name = models.CharField(max_length=30, null=True)
    credit = models.IntegerField(null=True)  # 학점
    day = models.IntegerField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    classroom = models.CharField(max_length=15, default='', null=True)
    advisor = models.CharField(max_length=30, null=True)
    major = models.CharField(max_length=30, null=True)
    objects = models.Manager()

    @classmethod
    def get_course_by_id(cls, course_id, semester):
        try:
            return cls.objects.get(course_id=course_id, semester=semester)
        except cls.DoesNotExist:
            return None

    def update_name(self, new_name):
        self.name = new_name
        self.save()

    def update_time(self, new_day, start_hour, start_minute, end_hour, end_minute):
        self.day = new_day
        self.start_time = datetime.time(start_hour, start_minute)
        self.end_time = datetime.time(end_hour, end_minute)
        self.save()

    def update_classroom(self, new_classroom):
        self.classroom = new_classroom
        self.save()

    def delete_course(self):
        self.delete()


class Takes(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='takes')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)  # TODO: 모든 학기를 크롤링 했다 가정할 때 null=False
    middle_grade = models.CharField(null=True, max_length=4)
    final_grade = models.CharField(null=True, max_length=4)
    real = models.BooleanField()
    objects = models.Manager()

    def delete_takes(self):
        self.delete()


class CalendarEvent(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title



__all__ = ['Course', 'Takes', 'CalendarEvent']
