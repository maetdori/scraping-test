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
    logging.info("today is "+str(today))
    # ===================================================#

    # 페이지 접속
    req = requests.get('https://www.gov.kr/portal/ntcItm')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    # 공지 테이블
    table = soup.find('tbody')

    # 제목, 게시일 찾기
    titles_dates = table.find_all('td', {'class': 'm-show'})
    # 인덱스 홀수는 날짜, 짝수(0포함)는 제목(링크)
    for i in range(1, len(titles_dates), 2):
        item = ""
        # HTML 태그 제거
        string_dates = titles_dates[i].text.strip()

        # 날짜 포맷 변경
        convert_to_date = datetime.datetime.strptime(string_dates, "%Y.%m.%d")

        if convert_to_date.strftime("%Y%m%d") <= today.strftime("%Y%m%d"):
            # 제목 선택
            current_title = titles_dates[(i - 1)]
            title_link = current_title.find('a')
            title = current_title.text
            if "중단" in title or "점검" in title:
                # 상세 페이지 이동
                ahref = "https://www.gov.kr" + title_link['href']
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
                    if str(today.month) + "." + str(today.day) in i:
                        check = True
                if check:
                    temp = re.split("[○,▶]", str(utf_content))
                    for item in temp:
                        logging.debug("item")
                        logging.debug(item)
                        # if "○" in item:
                        #     abort_why = item.split("○")[1].split("<")[0]

                # split return list
                # ex) "this is me" > split(" ") > ["this", "is", "me"]
                # for item in utf_content.split("○"):
                #
                # abort_why
                #         if "작업사유" in item:
                #             abort_why = item[item.find('작업사유'):item.find('※')]
                #         elif "중단사유" in item:
                #             abort_why = item
                #         elif "작업내용" in item:
                #             abort_why = item[item.find('작업내용'):item.find('작업내용') + 62]
                #         elif "중단 사유" in item:
                #             abort_why = item[item.find('중단 사유'):item.find('※')]

                        # # abort_thing
                        # if "중단업무" in item:
                        #     abort_why = item[item.find('중단업무'):item.find('※')]
                        # if "중단 업무" in item:
                        #     abort_why = item
                        # if "중단서비스" in item:
                        #     abort_why = item[item.find('중단서비스'):]
                        # if "대상" in item:
                        #     abort_why = item

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
                    #utf_title = title.encode('utf-8')
                    utf_title = title
                    #try:
                    #    logging.debug("here")
                    #    logging.debug(abort_why)
                    #    abort_why = abort_why.replace("\n", "").replace("-", " ").replace("○", " ").replace("시:","시 :").split(">")[1]
                    #    abort_why = abort_why.split("<")[0]
                        
                    #except:
                    #    abort_why = abort_why.replace("\n", "").replace("-", " ").replace("○", " ").replace("시:","시 :")
                    mail_body[utf_title] = abort_date
                    #abort_why = "N"
                else:
                    continue
    return check_mail.check("정부24", mail_body)