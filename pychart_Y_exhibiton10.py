from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
filename = f"yes24exhibiton/pychart_Y_exhibiton10{current_date}.json"

# 웹드라이버 설정
options = ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)

# 웹 사이트 접속
browser.get("http://ticket.yes24.com/Rank/All")
time.sleep(2)  # 페이지 로딩 대기

# 전시/행사 카테고리로 이동
event_link = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/New/Rank/Ranking.aspx?genre=15460')]"))
)
event_link.click()
time.sleep(2)  # 전시/행사 페이지 로딩 대기

# 월간 카테고리 선택
monthly_category = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(@categoryid, '3') and contains(text(), '월간')]"))
)
monthly_category.click()
time.sleep(2)  # 월간 카테고리 로딩 대기

# 웹 페이지 소스 가져오기
page_source = browser.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# 정보 추출
events_data = []

# Extracting data from rank-best div
rank_best_div = soup.find('div', class_='rank-best')
if rank_best_div:
    event_divs = rank_best_div.find_all('div')
    for event_div in event_divs:
        event_info = {}
        event_link = event_div.find('a', href=True)
        if event_link:
            event_info['title'] = event_link['title']
            event_info['image_url'] = event_link.find('img')['src']
            event_info['date_and_location'] = event_link.find('p', class_='rlb-sub-tit').get_text(strip=True)
            event_info['rank'] = event_link.find('p', class_='rank-best-number').find('span').get_text(strip=True)
            events_data.append(event_info)

# 전시/행사 순위 정보 추출
rank_list = soup.find('div', class_='rank-list')  # 첫번째 rank-list 컨테이너 선택
if rank_list:
    items = rank_list.find_all('div', recursive=False)[:7]  # 4위부터 10위까지의 정보 추출
    for item in items:
        event_info = {}
        title_link = item.find('p', class_='rank-list-tit').find('a')
        image = item.find('img', class_='rank-list-img')
        date_location = item.find_all('p')[-1]
        fluctuation_div = item.find('div', class_='fluctuation')

        # 순위 정보를 추출
        if fluctuation_div:
            rank_span = fluctuation_div.find('p').find('span')
            rank = rank_span.text.strip() if rank_span else 'No rank provided'
        else:
            rank = 'No rank provided'

        event_info['title'] = title_link.text.strip() if title_link else 'No title provided'
        event_info['image_url'] = image['src'] if image else 'No image provided'
        event_info['date_and_location'] = date_location.get_text(strip=True) if date_location else 'No date and location provided'
        event_info['rank'] = rank
        events_data.append(event_info)

# 결과를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as file:
    json.dump(events_data, file, ensure_ascii=False, indent=4)

# 브라우저 닫기
browser.quit()
