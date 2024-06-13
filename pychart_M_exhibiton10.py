from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
filename = f"melonexhibiton/pychart_M_exhibiton10{current_date}.json"

# 웹 드라이버 설정
options = ChromeOptions()
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
options.add_argument("--headless")
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)

# 웹 페이지에 접속
url = "https://ticket.melon.com/ranking/index.htm"
browser.get(url)
time.sleep(5)  # 페이지 로딩 대기

# "전시/클래식/기타" 버튼 클릭
try:
    concert_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@value='NEW_GENRE_EXH']"))
    )
    concert_button.click()
    print("Clicked '전시/클래식/기타' button.")
    time.sleep(5)  # 페이지가 완전히 로드될 때까지 대기
except Exception as e:
    print("Error clicking '전시/클래식/기타' button:", e)
    browser.quit()
    raise

# 페이지 소스 가져오기
try:
    page_source = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".tbl.tbl_style02 tbody"))
    ).get_attribute('innerHTML')
except Exception as e:
    print("Error loading the table:", e)
    browser.quit()
    raise

# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(page_source, 'html.parser')

# 데이터 추출
music_data = []
tracks = soup.select("tr")
for track in tracks:
    rank = track.select_one("td.fst .ranking").text.strip() if track.select_one("td.fst .ranking") else None
    change = track.select_one("td.fst .change").text.strip()
    # change 텍스트에서 불필요한 공백 제거
    change = ' '.join(change.split())
    title = track.select_one("div.show_infor p.infor_text a").text.strip() if track.select_one("div.show_infor p.infor_text a") else None
    place = track.select_one("td:nth-child(4)").text.strip() if track.select_one("td:nth-child(4)") else None
    image_url = track.select_one("div.thumb_90x125 img").get('src') if track.select_one("div.thumb_90x125 img") else None
    site_url = "https://ticket.melon.com/ranking/index.htm"
    date_elements = track.select("ul.show_date li")
    date = " ".join([element.text.strip() for element in date_elements])

    if rank and change and title and place and image_url and site_url and date:
        music_data.append({
            "rank": rank,
            "change": change,
            "title": title,
            "Venue": place,
            "ImageURL": image_url,
            "site": site_url,
            "date":date
        })

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(music_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()
