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
filename = f"ticketconcert/pychart_T_concert10{current_date}.json"

# 웹드라이버 설치
options = ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)
browser.get("https://www.ticketlink.co.kr/ranking")

# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "ranking_product"))
)

# "콘서트" 탭 버튼을 찾아서 클릭하기
try:
    concert_tab_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='콘서트']"))
    )
    concert_tab_button.click()
    print("Clicked '콘서트' tab.")
    time.sleep(3)  # 페이지가 완전히 로드될 때까지 대기
except Exception as e:
    print("Error clicking '콘서트' tab:", e)

# "월간" 탭 버튼을 찾아서 클릭하기
try:
    monthly_tab_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='월간']"))
    )
    monthly_tab_button.click()
    print("Clicked '월간' tab.")
    time.sleep(3)  # 페이지가 완전히 로드될 때까지 대기
except Exception as e:
    print("Error clicking '월간' tab:", e)

# 페이지 소스 가져오기
page_source = browser.page_source

# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(page_source, 'html.parser')

# 데이터 추출
music_data = []
tracks = soup.select(".ranking_product .ranking_product_table tbody tr")
for track in tracks:
    rank = track.select_one(".rank_number").text.strip()
    title = track.select_one(".ranking_product_title").text.strip()
    place = track.select_one(".ranking_product_place").text.strip()
    image_url = track.select_one(".ranking_product_imgbox img").get('src')
    date = track.select_one(".ranking_product_period").text.strip()
    site_url = "https://www.ticketlink.co.kr/ranking?ranking=genre&categoryId=10&category2Id=16&category3Id=16&period=monthly&currentDate"
    
    # 순위 변동 상태 추출
    change_element = track.select_one(".rank_status span")
    change = change_element.get('class', [''])[0] if change_element else ''
    change_text = change_element.text.strip() if change_element else '변동 없음'
    
    # 불필요한 공백 제거 및 변환 로직 추가
    change_text = ' '.join(change_text.split())
    if '상승' in change_text:
        change_text = change_text.replace('계단', '단계')
    elif '하락' in change_text:
        change_text = change_text.replace('계단', '단계')
    elif '신규 진입' in change_text:
        change_text = 'NEW'
    elif '변동 없음' in change_text:
        change_text = '-'

    music_data.append({
        "rank": rank,
        "change": change_text,
        "title": title,
        "Venue": place,
        "date": date,
        "ImageURL": image_url,
        "site": site_url
    })

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(music_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()
