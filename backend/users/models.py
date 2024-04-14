import pickle
from django.contrib.auth.models import AbstractUser
from django.db import models

# Serializing
def serialize_cookies(cookies):
    return base64.b64encode(pickle.dumps(cookies)).decode('utf-8')

# Deserializing
def deserialize_cookies(cookies_str):
    return pickle.loads(base64.b64decode(cookies_str.encode('utf-8')))


class User(AbstractUser):
    username = models.CharField(max_length=30, default='', primary_key=True, unique=True)   # 학번
    name = models.CharField(max_length=30, default='')                                      # 이름
    state = models.IntegerField(default=0)                                                  # 0: 재학, 1: 휴학, 2: 졸업
    year = models.IntegerField(null=True)                                                   # 학년
    semester = models.IntegerField(null=True)                                               # 학기
    major = models.CharField(max_length=100, null=True)                                     # 전공
    advisor = models.CharField(max_length=30, null=True)                                    # 지도교수
    login_cookie = models.CharField(max_length=500, null=True)                              # 로그인 쿠키
    nickname = models.CharField(max_length=30, default='', null=True, blank=True)           # 닉네임
    avatar = models.ImageField(upload_to="avatars", blank=True)                             # 프로필 사진
    thread = models.CharField(max_length=100, default='', null=True)                        # 챗봇 스레드

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        try:
            resized_avatar = Image.open(self.avatar)
            if resized_avatar.width > 400 or resized_avatar.height > 400:
                output_size = (400, 400)
                resized_avatar.thumbnail(output_size)
                resized_avatar.save(self.avatar.path)
        except Exception:
            print("Could not resize avatar img.\n")

    @classmethod
    def get_student_by_id(cls, username):
        return cls.objects.get(username=username)

    # @classmethod
    # def get_login_cookie(cls, username):
    #     return cls.objects.get(username=username).login_cookie
    def set_login_cookie(self, cookies):
        self.login_cookie = serialize_cookies(cookies)
        self.save()

    def get_login_cookie(self):
        return deserialize_cookies(self.login_cookie) if self.login_cookie else None

    def update_student_major(self, new_major):
        self.major = new_major
        self.save()

    def update_student_name(self, new_name):
        self.name = new_name
        self.save()

    def update_student_state(self, new_state):
        self.state = new_state
        self.save()

    def update_student_grade(self, new_year, new_semester):
        self.year = new_year
        self.semester = new_semester
        self.save()

    def update_student_cookie(self, new_cookie):
        self.cookie = new_cookie
        self.save()

    def delete_student(self):
        self.delete()

    @classmethod
    def get_takes(cls, username):
        return cls.objects.get(username=username).takes

#
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     profile_picture = models.ImageField(upload_to='profile_pictures/')
#
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#
#         img = Image.open(self.profile_picture.path)
#         if img.width != img.height:
#             size = min(img.width, img.height)
#             left = (img.width - size) // 2
#             top = (img.height - size) // 2
#             right = (img.width + size) // 2
#             bottom = (img.height + size) // 2
#             img = img.crop((left, top, right, bottom))
#             img.save(self.profile_picture.path)
