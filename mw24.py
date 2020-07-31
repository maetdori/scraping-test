# -*- coding:utf-8 -*-
import requests
import urllib
from bs4 import BeautifulSoup
import datetime

import check_mail
import send_email


def go():
    # ===================================================
    # 메일에 들어갈 내용
    mail_body = {}
    abort_date = "N"
    abort_thing = "N"
    abort_why = "N"

    # 오늘날짜
    today = datetime.datetime.now()
    # ===================================================

    # 사이트 접속------------------------------------
    req = requests.get('http://www.minwon.go.kr/main?a=AA140NoticeListApp&cp=1')
    html = req.text

    # 데이터 수집------------------------------------
    soup = BeautifulSoup(html, 'html.parser')

    # find noti table--------------------------------
    table = soup.find('tbody')

    # 공지 세부 페이지 접속을 위해 공지사항 제목을 모두 찾아서 한번씩 접속해보기
    titles = table.find_all('td', {'class': 'tl'})

    for i in range(len(titles)):

        # 공지 세부 페이지 접속
        current_title = titles[i]
        title_link = current_title.find('a')
        ahref = "http://www.minwon.go.kr" + title_link['href']

        sub_req = requests.get(ahref)
        sub_html = sub_req.text

        # 데이터 수집
        soup = BeautifulSoup(sub_html, 'html.parser')

        # 세부 페이지에서 공지 제목과 날짜 수집
        title_date = soup.find_all('dd', {'class': 'w02'})

        # 제목
        title = title_date[0].get_text()  # .encode('utf-8')
        # 날짜
        date_to_string = title_date[1].get_text()
        formatting = date_to_string.replace(" ", "0")
        t1 = ""
        # 날짜 포맷 변경
        string_to_date = datetime.datetime.strptime(formatting, "%Y.%m.%d.")
        # 오늘 날짜의 새로운 공지가 있니?
        if string_to_date.strftime("%Y%m%d") == today.strftime("%Y%m%d"):
            t1 = title
            # 새로운 공지가 있으면 해당 공지 내용을 수집
            content = soup.find('dd', {'class': 'w_all pl5 pt5'})
            # 스트링 인코딩 utf-8
            string_content = content.text
            utf_content = string_content

            # 내용 쪼개기 : 중단 일시, 작업사유, 중단 대상 업무
            for item in utf_content.split("\n"):
                # abort_date
                if "중단일시" in item:
                    abort_date = item[item.find('중단일시'):item.find('중단일시') + 68]
                if "작업일시" in item:
                    abort_date = item
                if "중단 일시" in item:
                    abort_date = item[item.find('중단일시'):item.find('중단일시') + 68]
                if "작업 일시" in item:
                    abort_date = item
                if "중단 일시" in item:
                    abort_date = item[item.find('○'):]
                if "지연 일시" in item:
                    abort_date = item[item.find('○'):]

                # abort_why
                if "작업사유" in item:
                    abort_why = item[item.find('작업사유'):item.find('○')]
                if "중단사유" in item:
                    abort_why = item[item.find('중단사유'):]
                if "작업내용" in item:
                    abort_why = item

                # abort_thing
                if "중단업무" in item:
                    abort_thing = item[item.find('중단업무'):]
                if "중단서비스" in item:
                    abort_thing = item
            mail_body[title] = abort_date.replace("○","")
    #send_email.send("민원24", mail_body)
    return go_popup(mail_body)

# to do 팝업이 새로 올라올때만 접속해서 확인하자.
def go_popup(mail_body):
    # ===================================================#
    # 메일에 들어갈 내용
    # 오늘날짜
    today = datetime.datetime.now()
    # ===================================================#
    req = urllib.request.urlopen('http://www.minwon.go.kr/popup/routine_notice.jsp')
    html = req.read()
    html_decode = html.decode("euc-kr")
    soup = BeautifulSoup(html_decode, 'html.parser')

    title = soup.find('title').text.strip()

    why = soup.find('div', {'id': 'm2'})
    abort_why = why.text.strip()
    date_and_thing = soup.find_all('div', {'id': 'date_imsi'})
    abort_date = str(date_and_thing[0].text.strip()).replace("               ", " ")
    abort_thing = date_and_thing[1].text.strip()
    #mail_body[title] = abort_date
    if str(today.year) + "." + str(today.month) + "." + str(today.day) in abort_date:
        mail_body[title] =  abort_date
        return check_mail.check("민원24", mail_body)
    else:
        return check_mail.check("민원24", mail_body)