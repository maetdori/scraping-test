# -*- coding:utf-8 -*-
from datetime import datetime

import requests
from bs4 import BeautifulSoup

import check_mail
import send_email
import send_dooray
import datetime
import logging
import json
import re

#log config
with open("./globalval.json",'r') as file:
    json_data = json.load(file)
file_name = json_data["log_file_path"]
log_level = json_data["log_level"]

logging.basicConfig(filename=file_name,level=log_level)
def emergency():
    # 페이지 접속
    req = requests.get('https://www.gov.kr/mntnce_notice.html')
    soup = BeautifulSoup(req.content, 'html.parser', from_encoding='utf-8')

    abort_date = soup.find('p', {'class': 'time'})

def go():
    # ===================================================#
    # 메일에 들어갈 내용
    mail_body = {}
    abort_date = "N"
    abort_thing = "N"
    abort_why = "N"

    # 오늘날짜
    today = datetime.datetime.now()
    # ===================================================#

    # 페이지 접속
    try:
        req = requests.get('https://www.gov.kr/portal/ntcItm')
    except requests.ConnectionError: 
        return check_mail.check("정부24(서버연결실패)", mail_body)
    except TimeoutError: 
        return check_mail.check("정부24(서버연결실패_타임아웃)", mail_body)

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    # 공지 테이블
    table = soup.find('table', {'class': 'md'})
    noti = table.find_all('td', {'class': 'subj m-show'})

    for i in noti:
        title = i.get_text()
        if "중단" in title or "점검" in title:
            # 상세 페이지 이동
            title_link = i.find('a').attrs['href']
            ahref = "https://www.gov.kr" + title_link
            sub_req = requests.get(ahref)
            html = sub_req.text
            sub_soup = BeautifulSoup(html, 'html.parser')
            content = sub_soup.find('div', {'class': 'view-contents'})

            # 공지 세부 내용
            string_content = content
            utf_content = string_content
            temp = str(utf_content).replace("년",".").replace("월",".").replace("일",".").replace(" ","").split("<br/>")
            check = False
            for i in temp:
                if str(today.month) + "." + str(today.day) in i and "중단" in i:
                    check = True
            if check:
                temp = re.split("[○,▶]", str(utf_content))
                for item in temp:
                    # abort_date
                    if "중단일시" in item:
                        abort_date = item
                    if "작업일시" in item:
                        abort_date = item[item.find('작업일시'):item.find('작업일시') + 53]
                    if "중단 시간" in item and abort_date == "N":
                        abort_date = item

                    # abort_why
                    if "중단사유" in item:
                        abort_why = item

                    # abort_thing
                    if "중단대상" in item or "중단업무" in item:
                        abort_thing = item

                check = False
                mail_body[title] = abort_date
            
    return check_mail.check("정부24", mail_body)