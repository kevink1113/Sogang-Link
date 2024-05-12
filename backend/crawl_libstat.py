import os
import django
import requests
from bs4 import BeautifulSoup
import re

# Django 환경 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from maps.models import Building, Facility

def clean_seats(seat_string):
    # 숫자만 추출하는 정규 표현식
    match = re.search(r'\d+', seat_string)
    return int(match.group(0)) if match else None

def fetch_seat_info(url):
    try:
        # Send a GET request to the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        response.encoding = 'euc-kr'

        # Parse the HTML content of the page with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the specific table by characteristics, here assuming it's the only table or identifying by other means
        table = soup.find('table', {'border': '1', 'cellspacing': '0', 'cellpadding': '1', 'width': '900'})

        # Initialize a list to store seat information
        seat_info = []

        # Skip the first two rows (headers and other non-data entries) and iterate over each subsequent row
        for row in table.find_all('tr')[2:]:  # Adjust the index if header rows differ
            cols = row.find_all('td')
            if cols:
                # Extract text from each column and create a dictionary of the seat data
                # if(cols[1].text.strip() == 'K관 열람실'):
                #     # input data to database
                #     # building = Building.objects.get(name="김대건관(K관)")
                #     facility = Facility.objects.get(name="K관 열람실")
                #     facility.total_seats = clean_seats(cols[2].text.strip())
                #     facility.used_seats = clean_seats(cols[3].text.strip())
                #     facility.available_seats = clean_seats(cols[4].text.strip())
                #     # Facility.usage_rate = cols[5].text.strip()
                #     facility.save()

                if Facility.objects.filter(name=cols[1].text.strip()).exists():
                    facility = Facility.objects.get(name=cols[1].text.strip())
                    facility.total_seats = clean_seats(cols[2].text.strip())
                    facility.used_seats = clean_seats(cols[3].text.strip())
                    facility.available_seats = clean_seats(cols[4].text.strip())
                    # Facility.usage_rate = cols[5].text.strip()
                    facility.save()
                    print("Saved stat of ", cols[1].text.strip())

                room_info = {
                    'room_name': cols[1].text.strip(),
                    'total_seats': cols[2].text.strip(),
                    'used_seats': cols[3].text.strip(),
                    'remaining_seats': cols[4].text.strip(),
                    'usage_rate': cols[5].text.strip()
                }
                seat_info.append(room_info)

        return seat_info

    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None



# 결과 출력
if __name__ == "__main__":
    
    # Example usage
    url = "http://libseat.sogang.ac.kr/seat/"
    fetch_seat_info(url)
    # print(seat_info)
