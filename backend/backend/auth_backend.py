from django.contrib.auth.backends import ModelBackend
from users.models import User
from lecture.models import Course, Takes
from .crawl_saint import get_saint_cookies, get_student_info, get_takes_info_by_semester, get_takes_info, get_grade_info

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
            self.manage_all_takes(user, cookies)
            # 성적 정보 처리
            self.manage_all_grades(user, cookies)

            print("새 사용자 정보 업데이트 및 수강/성적 정보 처리 완료")

        return user

    @staticmethod
    def serialize_cookies(cookies):
        import pickle
        import base64
        return base64.b64encode(pickle.dumps(cookies)).decode('utf-8')

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
        print("COOKIES: ", cookies)
        if cookies is not None:
            user.login_cookie = self.serialize_cookies(cookies)
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
        # all_grade_info = get_grade_info(cookies)
        # print("================ All Grade Info =====================")
        # print(all_grade_info)
        # print("=====================================================")


        # Course ID를 유니크한 값으로 만들기 위해 course_id와 course_semester를 병합 (재수강 고려)
        existing_takes = {
            f"{take.course.course_id}-{take.course.semester}": take
            for take in user.takes.all()
        }

        # print("existing takes: ", existing_takes)

        for (semester_code, semester_info) in all_semester_info.items():
            for key, value in semester_info.items():
                # Course ID를 유니크한 값으로 만들기 위해 course_number와 course_class(분반)를 병합 (재수강 고려)
                course_id = f"{value['course_number']}-{value['course_class']}-{semester_code}"
                if course_id not in existing_takes:
                    # Create new Takes if not existing

                    new_take = Takes()
                    new_take.course = Course.get_course_by_id(value['course_number'] + '-' + value['course_class'],
                                                              semester_code)
                    # 예외 처리: Course가 존재하지 않을 경우 어떻게든 정보를 넣는다.

                    defaults = {
                        'major': '대학',  # Default major if not set in conditions
                        'credit': 0,  # Default credit
                    }
                    # 개설교과목 정보 목록에 없는 이수교과목이 있을 경우 예외 처리
                    if new_take.course is None:
                        # 성찰과성장의 경우
                        if value['course_name'] == '성찰과성장':
                            defaults.update({
                                'major': '전인교육원',
                                'course_number': 'COR1007',
                                'credit': 1,
                            })
                        # 차후 다른 예시 추가 가능

                        new_take.course = Course(course_id=value['course_number'] + '-' + value['course_class'],
                                                 semester=semester_code,
                                                 name=value['course_name'],
                                                 major=defaults['major'],
                                                 credit=defaults['credit'],
                                                 # day=value['day'],
                                                 # start_time=value['start_time'],
                                                 # end_time=value['end_time'],
                                                 # classroom=value['classroom'],
                                                 # advisor=value['advisor'],
                                                 # major=value['major']
                                                 )
                        new_take.course.save()

                    new_take.student = user
                    new_take.real = True
                    new_take.save()

                    print(f"Added new take for {course_id}")
                else:
                    print(f"Takes for {course_id} already exists")


    def manage_all_grades(self, user, cookies):
        """
        현재 유저의 전체 성적 정보를 업데이트하는 함수
        """

        all_grade_info = get_grade_info(cookies)
        existing_takes = {
            f"{take.course.course_id}-{take.course.semester}": take
            for take in user.takes.all()
        }

        for semester_code, courses in all_grade_info.items():
            for course_code, course_details in courses.items():
                # "과목코드-학기코드" 형태로 partial_course_id를 만들어 일치 여부를 확인
                partial_course_id = f"{course_code}-{semester_code}"
                # '-' 기준으로 course_code와 semester_code를 분리, 
                # course_code가 일치하고 semester_code가 일치하는 Takes를 찾음
                matched_takes = {
                    key: val for key, val in existing_takes.items()
                    if key.split('-')[0] == course_code and key.split('-')[-1] == semester_code
                }
                if matched_takes:
                    for full_course_id, take in matched_takes.items():
                        # 만약 중간/기말 성적이 존재하면 업데이트
                        take.middle_grade = course_details.get('midterm_grade', '')
                        take.final_grade = course_details.get('final_grade', '')
                        take.save()
                        print(
                            f"Updated grades for {full_course_id} - Midterm: {take.middle_grade}, Final: {take.final_grade}")
                else:
                    print(f"No matching takes found for {partial_course_id}")


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
        # print("existing takes: ", existing_takes)

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
