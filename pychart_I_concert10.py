import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui.WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from datetime import datetime

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
filename = f"interparkconcert/pychart_I_concert10_{current_date}.json"

# ChromeDriver 설정
options = ChromeOptions()
options.add_argument("--headless")  # 브라우저 창 없이 실행
browser = webdriver.Chrome(options=options)
browser.get("https://tickets.interpark.com/contents/ranking")

# "콘서트" 탭 클릭
try:
    concert_tab_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '콘서트')]"))
    )
    concert_tab_button.click()
    print("Clicked '콘서트' tab.")
    time.sleep(3)  # 페이지 로드 대기
except Exception as e:
    print("Error clicking '콘서트' tab:", e)

# "월간" 탭 버튼을 찾아서 클릭하기
try:
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='월간']"))).click()
    print("Clicked '월간' tab.")
    time.sleep(3)
except Exception as e:
    print("Error clicking '월간' tab:", e)

# 페이지 소스 가져오기 및 파싱
page_source = browser.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# 순위 정보 컨테이너 추출
ranking_container = soup.find('div', class_='responsive-ranking-list_rankingListWrap__GM0yK')
concerts = []

# 데이터 추출
for ranking_item in ranking_container.find_all('div', class_='responsive-ranking-list_rankingItem__PuQPJ'):
    rank = ranking_item.find('div', class_='RankingBadge_badgeNumber__84aeb').text.strip()
    concert_name = ranking_item.find('li', class_='responsive-ranking-list_goodsName__aHHGY').text.strip()
    venue = ranking_item.find('li', class_='responsive-ranking-list_placeName__9HN2O').text.strip()
    image_url = ranking_item.find('img')['src']

    concert_data = {
        'Rank': rank,
        'ConcertName': concert_name,
        'Venue': venue,
        'ImageURL': image_url
    }
    concerts.append(concert_data)

# JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as file:
    json.dump(concerts, file, ensure_ascii=False, indent=4)

# 출력
for concert_data in concerts:
    print(concert_data)

browser.quit()
