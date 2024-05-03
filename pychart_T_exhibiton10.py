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
filename = f"ticketexhibiton/pychart_T_exhibiton10{current_date}.json"

# 웹드라이버 설치
options = ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)
browser.get("https://www.ticketlink.co.kr/ranking")

# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "ranking_product"))
)

# "전시" 탭 버튼을 찾아서 클릭하기
try:
    exhibiton_tab_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='전시']"))
    )
    exhibiton_tab_button.click()
    print("Clicked '전시' tab.")
    time.sleep(3)  # 페이지가 완전히 로드될 때까지 대기
except Exception as e:
    print("Error clicking '전시' tab:", e)

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

    music_data.append({
        "rank": rank,
        "title": title,
        "artist": place,
        "imageURL": image_url
    })

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(music_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()
