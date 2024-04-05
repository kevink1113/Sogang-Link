from django.contrib.auth.backends import ModelBackend
from users.models import User
from lecture.models import Course, Takes
from .crawl_saint import get_saint_cookies, get_student_info, get_takes_info_by_semester, get_takes_info


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password."""

    def authenticate(self, username=None, cookies=None):
        """
        사용자 인증 함수
        :param username: 학번
        :param cookies: 세인트 로그인 쿠키값
        :return: 인증한 사용자 객체
        """
        info = get_student_info(cookies)
        try:
            user = User.objects.get(username=username)
            print("기존 사용자 로그인")
        except User.DoesNotExist:
            user = User(username=username)
            user.set_unusable_password()  # 비밀번호를 설정하지 않음. (비밀번호 방식 인증이 아니므로)
            user.save()
            print("새 사용자 만듦")

        # 사용자 정보 업데이트
        self.update_user_info(user, info, cookies)
        # 수강 정보 처리
        # self.manage_takes(user, cookies, '2024010')
        self.manage_all_takes(user, cookies)
        return user

    def update_user_info(self, user, info, cookies):
        """
        사용자 정보 업데이트 함수
        """
        user.name = info['성명']
        user.state = 1
        user.year = int(info['현학년/학기'][0])
        user.semester = int(info['현학년/학기'].split("/")[-1].strip().replace("학기", ""))
        user.advisor = info['지도교수']
        user.major = info['전공']
        user.login_cookie = cookies
        user.save()
        print(f"{user.username} 정보 업데이트 함.")

    def manage_all_takes(self, user, cookies):
        """
        현재 유저의 전체 수강 정보를 업데이트하는 함수
        :param user: 현재 로그인한 사용자
        :param cookies: 모바일 세인트 로그인 쿠키값
        :return: None
        """
        all_semester_info = get_takes_info(cookies)

        # Course ID를 유니크한 값으로 만들기 위해 course_id와 course_semester를 병합 (재수강 고려)
        existing_takes = {
            f"{take.course.course_id}-{take.course.semester}": take
            for take in user.takes.all()
        }
        print("existing takes: ", existing_takes)

        for (semester_code, semester_info) in all_semester_info.items():
            for key, value in semester_info.items():
                # Course ID를 유니크한 값으로 만들기 위해 course_number와 course_class(분반)를 병합 (재수강 고려)
                course_id = f"{value['course_number']}-{value['course_class']}-{semester_code}"
                if course_id not in existing_takes:
                    # Create new Takes if not existing

                    new_take = Takes()
                    new_take.course = Course.get_course_by_id(value['course_number'] + '-' + value['course_class'],
                                                              semester_code)
                    new_take.student = user
                    new_take.real = True
                    new_take.save()

                    print(f"Added new take for {course_id}")
                else:
                    print(f"Takes for {course_id} already exists")

    def manage_takes(self, user, cookies, semester_code):
        """
        현재 유저의 현학기 수강 정보를 업데이트하는 함수
        :param user: 현재 로그인한 사용자
        :param cookies: 모바일 세인트 로그인 쿠키값
        :param semester_code: ex. 2024010
        :return:
        """
        current_semester_info = get_takes_info_by_semester(cookies, semester_code)

        # Course ID를 유니크한 값으로 만들기 위해 course_number와 course_class를 병합 (재수강 고려)
        existing_takes = {
            f"{take.course.course_id}": take
            for take in user.takes.all()
        }  # ex: {'CSE2010-01': Takes object (1), 'CSE2010-02': Takes object (2)}
        print("existing takes: ", existing_takes)

        for key, value in current_semester_info.items():
            # Course ID를 유니크한 값으로 만들기 위해 course_number와 course_class(분반)를 병합 (재수강 고려)
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
