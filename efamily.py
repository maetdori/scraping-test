# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import requests
import datetime

import check_mail
import send_email

# ===================================================#
# 메일에 들어갈 내용
mail_body = {}

# 오늘날짜
today = datetime.datetime.now()


# ===================================================#

def go():
    count = 0
    db_list = []
    # userAgency 설정을 위한 head 설정
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)     Chrome/37.0.2049.0 Safari/537.36'
}
    # requests 이용
    req = requests.get('http://efamily.scourt.go.kr/index.jsp', headers=headers)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    # 공지사항 리스트를 뽑아온다
    notice_list = soup.find('div', {'class', 'notice'}).find_all('li','con')
    # 날짜 리스트를 뽑아온다
    date_list = soup.find('div', {'class', 'notice'}).find_all('li', {'class', 'date'})
    # 오늘날짜인지 확인하기
    for i in range(len(date_list)):
        if date_list[i].get_text().strip() == today.strftime(str(today.year) + "." + str(today.month) + "." + str(today.day)):  #"%Y.%m.%d"):
        # if date_list[i].get_text().strip() == '2020.08.03':  # 테스트용으로 8월 3일 공지를 넣음
            utf_notice = notice_list[i].get_text().strip()
            print( today.strftime(str(today.year) + "." + str(today.month) + "." + str(today.day)))
            mail_body[utf_notice] = str(date_list[i]) + ' 공지사항이 있습니다. (홈페이지 확인 요망)'
    if mail_body:  # 금일 날짜로 된 공지가 있을 때 메일을 보낸다.
        return check_mail.check("전자가족관계등록시스템", mail_body)
    else:
        return check_mail.check("전자가족관계등록시스템", {})