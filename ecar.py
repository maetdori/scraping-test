# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import http.cookiejar
import urllib
import check_mail
import send_email
import datetime
import json
import logging

def go():
    #===================================================#
    #메일에 들어갈 내용
    mail_body = {}
    abort_date = "N"
    abort_thing = "N"
    abort_why = "N"

    #오늘날짜
    today = datetime.datetime.now()
    #===================================================#

    # make session
    cj = http.cookiejar.LWPCookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    url = "http://www.ecar.go.kr/Index.jsp"

    # access to notification page and get html
    html = opener.open(url).read().decode('utf-8')

    # parse html
    soup = BeautifulSoup(html, "html.parser")

    # 쿠키값만 빼오기
    cookie = soup.body.find('link').attrs['href']
    cookie = cookie.split("=")
    cookie = cookie[1]

    # 헤더 세팅해서 새로 request 보낸다
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "Set-Cookies" : cookie
        }

    response = requests.get(url, headers=headers)
    html = response.text
    
    soup = BeautifulSoup(html, "html.parser")

    # 공지사항 리스트를 뽑아온다
    notice_list = soup.find('div', {'class': 'notic'}).find_all('dt')

    for dt in notice_list:
        title = dt.text
        if "작업" in title:
            param = dt.find("a").get("onclick").split("'")
            bbs = param[1]
            ntce = param[3]
            inquire = param[5]

            # 상세 페이지 이동
            ahref = "http://www.ecar.go.kr" + fn_BoardDetail(bbs, ntce, inquire)
            sub_req = requests.get(ahref, headers = headers)
            html = sub_req.text
            
            sub_soup = BeautifulSoup(html, 'html.parser')
            content = sub_soup.find('div', {'class': 'table_txt'})

            # 공지 세부 내용
            temp = str(content).replace(" ","").split("<br/>")
            for i in temp: 
                flag = False
                # content에 오늘 날짜 있는지 확인
                if str(today.month) + "월" + str(today.day) in i:
                    abort_date = i
                    mail_body[title] = abort_date
                    flag = True
                if flag and "작업내용" in i:
                    abort_why = i
                if flag and "대상" in i:   
                    abort_thing = i

    return check_mail.check("자동차민원 대국민포털", mail_body)

def fn_BoardDetail(bbs_se_code, ntce_artc_no, inquire_co):
    return "/Application.jsp?nc_menuId=NTA001&bbs_se_code="+bbs_se_code+"&ntce_artc_no="+ntce_artc_no+"&inqire_co="+inquire_co

