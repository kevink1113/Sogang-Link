from django.contrib.auth.backends import ModelBackend
from users.models import User
# from pybo.models import *
from lecture.models import *
from .crawl_saint import get_saint_cookies, pretty_print_takes_info, get_takes_info, get_student_info, \
    get_takes_info_by_semester


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password.

    """

    def authenticate(self, username=None, cookies=None):
        info = get_student_info(cookies)
        try:
            user = User.objects.get(username=username)
            student = User.get_student_by_id(username)
            print("기존 사용자 로그인")
        except User.DoesNotExist:
            user = User(username=username)
            user.set_unusable_password()  # 비밀번호를 설정하지 않습니다.
            user.save()
            # student = User()
            print("새 사용자 만듦")
        # print(info)
        user.username = username
        user.name = info['성명']
        user.state = 1
        user.year = int(info['현학년/학기'][0])
        user.semester = int(info['현학년/학기'].split("/")[-1].strip().replace("학기", ""))
        user.advisor = info['지도교수']
        user.major = info['전공']
        user.login_cookie = cookies
        user.save()
        print(f"{user.username} 정보 업데이트 함.")
        # TODO: Uncomment this code after implementing the Course model,Dynamic semester, and Takes model
        info = get_takes_info_by_semester(cookies, '2024010')
        takes = User.get_takes(username=username)
        for i in takes.all():
            if i.real is True & i.course.semester == 241:
                print(i)
                Takes.delete_takes(i)
        print(info)

        # TODO: 로그인 할 때 중복 수강 정보는 추가하지 않기
        for key, value in info.items():
            take = Takes()
            print(value)
            # TODO: Dynamic semester
            take.course = Course.get_course_by_id(value['course_number'] + '-' + value['course_class'], 241)
            take.student = user
            take.real = True
            take.save()
        # info = get_takes_info_by_semester(cookies, '2019010')
        # takes = User.get_takes(username=username)
        # for i in takes.all():
        #     if i.real is True & i.course.semester == 191:
        #         print(i)
        #         Takes.delete_takes(i)
        # print(info)

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
