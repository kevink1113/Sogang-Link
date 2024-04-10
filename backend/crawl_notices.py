import requests
from bs4 import BeautifulSoup

def fetch_table_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table, you might need to adjust the selector based on actual HTML structure
    table = soup.find('table')
    
    data = []
    if table:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if not cols:
                # This skips the header row with 'th' elements
                continue
            # Extract text from each cell in the row and form a list
            cols = [ele.text.strip() for ele in cols]
            data.append(cols)
    return data

def scrape_pages(base_url, start_page, end_page):
    all_data = []
    for page in range(start_page, end_page + 1):
        url = f"{base_url}?page={page}"
        print(f"Scraping data from {url}")
        page_data = fetch_table_data(url)
        all_data.extend(page_data)
        print(f"Scraped data from {url}")
    
    return all_data

# Define the base URL and the range of pages to scrape
base_url = "http://sogang.ac.kr/ko/story/notification-general"
data = scrape_pages(base_url, 1, 5)

# Print the combined data from all pages
for entry in data:
    print(entry)
