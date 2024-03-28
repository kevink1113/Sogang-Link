
import requests
from bs4 import BeautifulSoup

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
}

# Make sure these credentials are correct
LOGIN_INFO = {
    'id': '아이디',  # Your student ID
    'pass_wd': '비밀번호',  # Your password
}

login_url = "https://libetc3.sogang.ac.kr/mobile/MA/xml_login.php"  # Mobile SAINTE login URL

session = requests.session()  # Create a session to receive cookies
response = session.post(login_url, headers=header, data=LOGIN_INFO, verify=False)

print(response.text)  # Check login result

seat = session.get("https://libetc3.sogang.ac.kr/mobile/PA/xml_seat_map.php?param_room_no=2", verify=False)
print(seat.text)


cookies = response.cookies
session.close()  # Close the session