import subprocess

# 크롤링할 개설교과목 년도, 학기 조합
# 학기: 1학기(1), 여름학기(s), 2학기(2), 겨울학기(w)
commands = [
    ('일반공지', '10'),
    ('학사공지', '10'),
    ('장학공지', '10'),
]


def run_commands():
    # 학기별로 크롤링 실행
    for type, num in commands:
        cmd = ['python', 'crawl_notices.py', '--type=' + type, '--num=' + num]
        print(f"실행 중: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, check=True, text=True, capture_output=True)
            print("출력:\n", result.stdout)
            print("에러들:\n", result.stderr if result.stderr else "No errors.")
        except subprocess.CalledProcessError as e:
            # 서브프로세스 중 에러 발생 시 출력
            print(f"다음 크롤링 실행하는 중 에러: {' '.join(cmd)}: {e}")
            print(e.output)


if __name__ == "__main__":
    print("복수 공지사항 자동화 크롤링 시작")
    run_commands()
