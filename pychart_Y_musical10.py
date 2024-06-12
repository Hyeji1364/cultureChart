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
filename = f"yes24musical/pychart_Y_musical10{current_date}.json"

# 웹드라이버 설치
options = ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
browser.get("http://ticket.yes24.com/Rank/All")
time.sleep(5)  # 페이지 로딩 대기

# 뮤지컬 카테고리로 이동
musical_link = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/New/Rank/Ranking.aspx?genre=15457')]"))
)
musical_link.click()
time.sleep(2)  # 뮤지컬 페이지 로딩 대기

# 월간 카테고리 선택
monthly_category = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[@categoryid='3']"))
)
monthly_category.click()
time.sleep(5)  # 월간 카테고리 로딩 대기

# 웹 페이지 소스 가져오기
page_source = browser.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# 정보 추출
musicals_data = []

# 1-3위 뮤지컬 데이터 추출
rank_best_div = soup.find('div', class_='rank-best')
if rank_best_div:
    musical_divs = rank_best_div.find_all('div', recursive=False)
    for musical_div in musical_divs:
        musical_info = {}
        musical_link = musical_div.find('a', href=True)
        if musical_link:
            musical_info['title'] = musical_link['title']
            musical_info['ImageURL'] = musical_link.find('img')['src']
            musical_info['Venue'] = musical_link.find('p', class_='rlb-sub-tit').get_text(strip=True)
            musical_info['rank'] = musical_link.find('p', class_='rank-best-number').find('span').get_text(strip=True)
            musical_info['site'] = "http://ticket.yes24.com" + musical_link['href']
            change_status = musical_link.find('span', class_='rank-best-number-new')
            if change_status:
                musical_info['change'] = 'NEW'
            else:
                change = musical_link.find('span', {'class': ['rank-best-number-up', 'rank-best-number-down']})
                if change:
                    if 'rank-best-number-up' in change['class']:
                        musical_info['change'] = f"{change.get_text(strip=True)}단계 상승"
                    elif 'rank-best-number-down' in change['class']:
                        musical_info['change'] = f"{change.get_text(strip=True)}단계 하락"
                else:
                    musical_info['change'] = '-'
            musicals_data.append(musical_info)
            
# 전체 뮤지컬 순위 정보 추출
rank_lists = soup.find_all('div', class_='rank-list')  # 모든 rank-list 컨테이너 선택
for rank_list in rank_lists:
    items = rank_list.find_all('div', recursive=False)  # 모든 항목 추출
    for item in items:
        musical_info = {}
        title_link = item.find('p', class_='rank-list-tit').find('a')
        image = item.find('img', class_='rank-list-img')
        date_location = item.find_all('p')[-1]
        fluctuation_div = item.find('div', class_='fluctuation')  # 순위 정보를 포함하는 div 태그를 찾는다.

        # 순위 정보를 추출
        if fluctuation_div:
            rank_span = fluctuation_div.find('p').find('span')  # 첫 번째 <p> 태그 내의 <span>에서 순위를 찾는다.
            rank = rank_span.text.strip() if rank_span else '순위 정보 없음'
            
            # 변동 상태 추출
            change_class = fluctuation_div.find_all('p')[-1].get('class', [])
            if 'rank-list-number-new' in change_class:
                change = 'NEW'
            elif 'rank-list-number-up' in change_class:
                change_value = fluctuation_div.find('p', class_='rank-list-number-up').text.strip()
                change = f"{change_value}단계 상승"
            elif 'rank-list-number-down' in change_class:
                change_value = fluctuation_div.find('p', class_='rank-list-number-down').text.strip()
                change = f"{change_value}단계 하락"
            else:
                change = '-'
        else:
            rank = '순위 정보 없음'
            change = '-'

        musical_info['title'] = title_link.text.strip() if title_link else '제목 정보 없음'
        musical_info['ImageURL'] = image['src'] if image else '이미지 정보 없음'
        musical_info['Venue'] = date_location.get_text(strip=True) if date_location else '날짜 및 장소 정보 없음'
        musical_info['rank'] = rank
        musical_info['change'] = change
        musical_info['site'] = "http://ticket.yes24.com" + title_link['href'] if title_link else '사이트 정보 없음'
        musicals_data.append(musical_info)

# 결과를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as file:
    json.dump(musicals_data, file, ensure_ascii=False, indent=4)

# 브라우저 닫기
browser.quit()
