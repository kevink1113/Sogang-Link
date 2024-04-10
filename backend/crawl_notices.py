User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

def fetch_table_and_links(driver, url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table')
    data = []
    
    if table:
        rows = table.find_all('tr')[1:]
        for index, row_html in enumerate(rows):
            if index == 0:
                continue  # Skip header row
            
            # Extract text from each cell
            cols = [ele.text.strip() for ele in row_html.find_all('td')]
            if not cols:
                continue  # Skip empty rows
            
            # Selenium to handle clicks and dynamic URLs
            row = driver.find_elements(By.CSS_SELECTOR, "table tr")[index]  # +1 to adjust for header
            ActionChains(driver).move_to_element(row).click().perform()
            
            # Handle new tabs/windows if they open
            if len(driver.window_handles) > 1:
                original_window = driver.current_window_handle
                driver.switch_to.window(driver.window_handles[-1])
                cols.append(driver.current_url)
                driver.close()
                driver.switch_to.window(original_window)
            else:
                cols.append(driver.current_url)  # Assume current URL is the result
            
            data.append(cols)
            driver.get(url)  # Reload to reset the state for next row
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    
    return data

def scrape_pages(base_url, start_page, end_page):
    all_data = []
    driver = webdriver.Chrome()  # Initialize the WebDriver
    
    for page in range(start_page, end_page + 1):
        url = f"{base_url}?page={page}"
        print(f"Scraping data from {url}")
        page_data = fetch_table_and_links(driver, url)
        all_data.extend(page_data)
        print(f"Scraped data from {url}")
    
    driver.quit()  # Close the WebDriver after scraping
    return all_data

# Base URL and page range
base_url = "http://sogang.ac.kr/ko/story/notification-general"
data = scrape_pages(base_url, 1, 1)

# Output the data, including dynamic links
for entry in data:
    print(entry)