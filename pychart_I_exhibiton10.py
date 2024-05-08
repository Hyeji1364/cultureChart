import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from datetime import datetime

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
filename = f"interparkexhibiton/pychart_I_exhibiton10{current_date}.json"

# 웹드라이버 설정
options = ChromeOptions()
options.add_argument("--headless")
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
browser.get("https://tickets.interpark.com/contents/ranking")

# RadioButton_wrap__761f0 클래스를 가진 div 요소를 찾기
search_box = browser.find_element(By.CLASS_NAME, "RadioButton_wrap__761f0")

# "콘서트" 탭 버튼을 찾아서 클릭하기
try:
    concert_tab_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='전시/행사']"))
    )
    concert_tab_button.click()
    print("Clicked '전시/행사' tab.")
    time.sleep(3)  # 페이지가 완전히 로드될 때까지 대기
except Exception as e:
    print("Error clicking '전시/행사' tab:", e)

# "월간" 탭 버튼을 찾아서 클릭하기
try:
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='월간']"))).click()
    print("Clicked '월간' tab.")
    time.sleep(3)
except Exception as e:
    print("Error clicking '월간' tab:", e)

page_source = browser.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Find the parent container for ranking items
ranking_container = soup.find('div', class_='responsive-ranking-list_rankingListWrap__GM0yK')

concerts = []

# 1-3위 데이터 추출
for ranking_item in ranking_container.find_all('div', class_='responsive-ranking-list_rankingItem__PuQPJ'):
    rank = ranking_item.find('div', class_='RankingBadge_badgeNumber__84aeb').text.strip()
    concert_name = ranking_item.find('li', class_='responsive-ranking-list_goodsName__aHHGY').text.strip()
    venue = ranking_item.find('li', class_='responsive-ranking-list_placeName__9HN2O').text.strip()
    image_url = ranking_item.find('img')['src']  # Extracting image URL

    concert_data = {
        'Rank': rank,
        'ConcertName': concert_name,
        'Venue': venue,
        'ImageURL': image_url
    }
    concerts.append(concert_data)

# 4-10위 콘서트 순위 정보 추출
rank_list_4_to_10 = soup.find_all('div', class_='responsive-ranking-list_rankingItem__PuQPJ')[3:10]  # 4위부터 10위까지의 항목 추출
for ranking_item in rank_list_4_to_10:
    rank = ranking_item.find('div', class_='RankingBadge_badgeNumberColor__d45a0').text.strip()
    concert_name = ranking_item.find('li', class_='responsive-ranking-list_goodsName__aHHGY').text.strip()
    venue = ranking_item.find('li', class_='responsive-ranking-list_placeName__9HN2O').text.strip()
    image_url = ranking_item.find('img')['src']  # Extracting image URL

    concert_data = {
        'Rank': rank,
        'ConcertName': concert_name,
        'Venue': venue,
        'ImageURL': image_url
    }
    concerts.append(concert_data)

# json파일로 저장
with open(filename, 'w', encoding='utf-8') as file:
    json.dump(concerts, file, ensure_ascii=False, indent=4)

# 출력
for concert_data in concerts:
    print(concert_data)
