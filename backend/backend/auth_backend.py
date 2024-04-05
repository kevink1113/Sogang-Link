from django.contrib.auth.backends import ModelBackend
from users.models import User
from lecture.models import Course, Takes
from .crawl_saint import get_saint_cookies, get_student_info, get_takes_info_by_semester

class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password."""

    def authenticate(self, username=None, cookies=None):
        info = get_student_info(cookies)
        try:
            user = User.objects.get(username=username)
            print("기존 사용자 로그인")
        except User.DoesNotExist:
            user = User(username=username)
            user.set_unusable_password()  # 비밀번호를 설정하지 않습니다.
            user.save()
            print("새 사용자 만듦")

        # 사용자 정보 업데이트
        self.update_user_info(user, info, cookies)
        # 수강 정보 처리
        self.manage_takes(user, cookies, '2024010')

        return user

    def update_user_info(self, user, info, cookies):
        user.name = info['성명']
        user.state = 1
        user.year = int(info['현학년/학기'][0])
        user.semester = int(info['현학년/학기'].split("/")[-1].strip().replace("학기", ""))
        user.advisor = info['지도교수']
        user.major = info['전공']
        user.login_cookie = cookies
        user.save()
        print(f"{user.username} 정보 업데이트 함.")

    def manage_takes(self, user, cookies, semester_code):
        current_semester_info = get_takes_info_by_semester(cookies, semester_code)
        # Map existing takes by course ID and semester to ensure uniqueness
        existing_takes = {
            f"{take.course.course_id}": take
            for take in user.takes.all()
        }
        print("existing takes: ", existing_takes)

        for key, value in current_semester_info.items():
            # Construct the unique identifier for course
            course_id = f"{value['course_number']}-{value['course_class']}"
            if course_id not in existing_takes:
                # Create new Takes if not existing

                new_take = Takes()
                new_take.course = Course.get_course_by_id(value['course_number'] + '-' + value['course_class'], 241)
                new_take.student = user
                new_take.real = True
                new_take.save()

                print(f"Added new take for {course_id}")
            else:
                print(f"Takes for {course_id} already exists")



    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
