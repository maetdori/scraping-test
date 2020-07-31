import requests
from bs4 import BeautifulSoup
import datetime

import check_mail
import send_email


def go():
    # ===================================================
    # 메일에 들어갈 내용
    mail_body = {}
    # 오늘날짜
    today = datetime.datetime.now()

    # ===================================================

    # 사이트 접속------------------------------------
    req = requests.get('http://maker.ecar.go.kr/Services')
    html = req.text

    # 데이터 수집------------------------------------
    soup = BeautifulSoup(html, 'html.parser')

    div = soup.find('div')
    # 공지 세부 페이지 접속을 위해 공지사항 제목을 모두 찾아서 한번씩 접속해보기
    title = div.find_all('p', {'class': 'tit'})[0].text.strip()
    content = str(BeautifulSoup(
        str(div.find_all('div', {'class': 'text'})[0])
        .replace("<br/>", "꿻"), 'html.parser').get_text())\
        .replace("꿻", "<br/>")\
        .replace("년 ", ".")\
        .replace("월 ", ".")\
        .replace("일(", "(")\
        .replace(".시", "일 시")
    today = str(today).replace("-", ".").split(" ")

    # 오늘이면 전송합니다.
    #
    # if today[0] in content:
    #     mail_body[title] = content
    #     check_mail.check('금융감독원', mail_body)