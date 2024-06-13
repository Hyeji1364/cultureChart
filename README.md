# 파이썬 설치   

설치해야하는 파일
- pylance / python / python debugger

설치된 목록보기
````
    pip3 list
````

## requests

````
    pip install requests
    : 웹 페이지나 API로부터 데이터를 손쉽게 가져오는 Python 라이브러리
    
    pip install beautifulsoup4
    : HTML 및 XML 문서를 구문 분석하여 데이터를 추출하기 위한 파이썬 라이브러리

    pip install lxml
    : XML 및 HTML을 처리하기 위한 파이썬 라이브러리로, 파싱 및 문서 조작에 사용됨

    pip install pandas
    : 데이터 조작 및 분석을 위한 Python 라이브러리로, 데이터프레임을 다룰 때 유용함

    pip install selenium
    : 웹 애플리케이션 테스트 자동화를 위한 도구로, 브라우저를 제어하여 웹 페이지를 자동으로 조작할 수 있게 해줌

    pip install webdriver_manager
````

## 파일 불러오기

````
    import requests as req -> import requests as '파일명지정'

    res = req.get("https://music.bugs.co.kr/chart") ->  res = req.get("불러올 파일 주소")

    print(res.text) -> 텍스트만 불러옴
````

## 결과 확인

````
python bugsmusic.py -> python (파일명)
````
