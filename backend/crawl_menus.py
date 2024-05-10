from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime  # Import the datetime class directly
import time
import re


import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django.setup()
from maps.models import Facility, Menu


def setup_driver():
    # Setup Chrome webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1400,1500")
        
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disk-cache-size=4096")
    options.add_argument("--disable-infobars")  # Disables the "Chrome is being controlled" infobar
    options.add_argument("--disable-extensions")  # Disables existing extensions
    options.add_argument("--disable-popup-blocking")  # Disables popups
    options.add_argument("--ignore-certificate-errors")  # Ignores certificate-related errors
    options.add_argument("--disable-print-preview")  # Disables features that can interfere
    driver = webdriver.Chrome(options=options)
    return driver

def fetch_menus(driver, url):
    driver.get(url)
    # Loop until there is no menu info in the table
    for _ in range(2):
      print("Moved to next page")
      print("current page url: " + driver.current_url)
      # Wait for the table to load
      WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, "table.tableInBWHall1"))
      )
      
      # Fetch the table
      table = driver.find_element(By.CSS_SELECTOR, "table.tableInBWHall1")
      rows = table.find_elements(By.TAG_NAME, "tr")  # Get all rows in the table

      menu_by_date_and_corner = {}
      # Assume first row is for dates and subsequent rows for menu data
      if len(rows) > 2:
          dates = rows[0].find_elements(By.TAG_NAME, "td")
          # Skip the last cell in the dates row as it's for origin info which spans multiple rows
          date_headers = [date.text.strip() for date in dates[:-1]] 
          
          # Each subsequent row contains menu data
          for row in rows[1:]:
              items = row.find_elements(By.TAG_NAME, "td")
              for i, item in enumerate(items[:-1]):  # Skip the last column if it's not needed
                  date_key = date_headers[i]
                  menu_detail = item.text.strip().split("\n")
                  corner_name = menu_detail[0]
                  corner_menu = "\n".join(menu_detail[1:])
                  
                  if date_key not in menu_by_date_and_corner:
                      menu_by_date_and_corner[date_key] = {}
                  
                  if corner_name in menu_by_date_and_corner[date_key]:
                      menu_by_date_and_corner[date_key][corner_name].append(corner_menu)
                  else:
                      menu_by_date_and_corner[date_key][corner_name] = [corner_menu]
      else:
        break
        
      next_button = driver.find_element(By.XPATH, "/html/body/div[1]/html/div/main/div/div[4]/div/div[3]/div/div/div[2]/div[3]")
      next_button.click()

    return menu_by_date_and_corner



def save_menus(menu_data, facility_name):
    try:
        # Fetch the facility instance instead of building
        facility = Facility.objects.get(name=facility_name)
        
        for date_str, corners in menu_data.items():
            match = re.search(r'\((\d{2})\.(\d{2})\)', date_str)
            if not match:
                print(f"Date format error in '{date_str}'")
                continue

            month, day = match.groups()
            year = datetime.now().year
            date_str_formatted = f"{year}-{month}-{day}"
            
            try:
                date = datetime.strptime(date_str_formatted, "%Y-%m-%d").date()
            except ValueError as e:
                print(f"Error parsing date '{date_str_formatted}': {e}")
                continue

            menu, created = Menu.objects.update_or_create(
                facility=facility,
                date=date,
                defaults={'items_by_corner': corners}
            )
            if created:
                print(f"Created new menu for {facility.name} on {date}")
            else:
                print(f"Updated menu for {facility.name} on {date}")

    except Facility.DoesNotExist:
        print(f"Facility '{facility_name}' not found in the database.")


def main():
    url = 'https://www.sogang.ac.kr/ko/menu-life-info'
    driver = setup_driver()
    try:
        facility_name = "우정원 학생식당"
        menu_data = fetch_menus(driver, url)
        save_menus(menu_data, facility_name)
        
        facility_name = "엠마오 학생식당"
        menu_data = fetch_menus(driver, url+"?tab1=1")
        save_menus(menu_data, facility_name)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
