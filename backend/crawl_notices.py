import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip  # 클립보드 사용을 위해

def scrape_links():
    driver = webdriver.Chrome()
    driver.get("https://sogang.ac.kr/ko/story/notification-general")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))

    # 첫 번째 행을 찾아 클릭
    first_row = driver.find_element(By.CSS_SELECTOR, "table tr:nth-child(2) td:nth-child(1)")
    driver.execute_script("arguments[0].click();", first_row)
    collected_data = []  # 제목과 링크를 저장할 리스트

    for _ in range(10):  # 10번 반복
        # 새 페이지 로딩 대기
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.cursor-pointer")))
        
        # 링크 아이콘 클릭
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'set-alt-image')))
        # find element by id
        time.sleep(1)  # 클립보드 복사를 위한 충분한 시간 확보
        title = driver.find_element(By.ID, 'set-alt-image').text

        link_icon = driver.find_element(By.CSS_SELECTOR, "img[alt='link']")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(link_icon))
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='link']")))
        ActionChains(driver).move_to_element(link_icon).click().perform()

        # driver.execute_script("arguments[0].scrollIntoView(true);", link_icon)
        driver.execute_script("arguments[0].click();", link_icon)
        
        # 클립보드에서 링크 가져오기
        # time.sleep(1)  # 클립보드 복사를 위한 충분한 시간 확보
        link_url = pyperclip.paste()


        print("title: ", title, " link: ", link_url)
        collected_data.append({'title': title, 'link': link_url})

        # 이전 페이지 버튼 클릭
        span = driver.find_element(By.XPATH, "//span[text()='이전 페이지']")
        span.click()
    driver.quit()
    return collected_data

# 결과 출력
if __name__ == "__main__":
    extracted_links = scrape_links()
    print("========== Extracted Links ==========")
    for link in extracted_links:
        print(link)
