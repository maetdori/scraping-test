import requests
from bs4 import BeautifulSoup
import http.cookiejar
import urllib
import check_mail
import send_email
import datetime
import json
import logging
from email.mime.image import MIMEImage
import PIL
import pytesseract
from PIL import Image
from pytesseract import *
import re
import cv2

#log config
with open("./globalval.json",'r') as file:
    json_data = json.load(file)
file_name = json_data["log_file_path"]
log_level = json_data["log_level"]
chromedriver = json_data["chromedrive_exe_path"]

logging.basicConfig(filename=file_name,level=log_level)

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
    url = "https://www.payinfo.or.kr/main/main.do?mode=null"
    html = opener.open(url).read().decode("utf-8")

    soup = BeautifulSoup(html, 'html.parser')
    noti = soup.find('span', {'class': 'notice_conlist'})
    title = noti.get_text().split("(")[0]

    #if "점검" in title or "중단" in title:
    href = noti.find('a').attrs['href']

    # 상세페이지
    url = "https://www.payinfo.or.kr" + href
    html = opener.open(url).read().decode("utf-8")

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class': 'tbl_view'})

    # 공지사항 이미지 받아오기
    img_url = table.find('img').attrs['src']
    urllib.request.urlretrieve(img_url, 'payinfo' + '.png')

    # 이미지 텍스트 변환
    img = Image.open('payinfo.png')
    text = pytesseract.image_to_string(img, lang='kor')

    content = text.replace("\nㅁ", "-").split("\n")
    for element in content:
        if "점검" in element and str(today.month) + "." + str(today.date) in element:
        #if "2019.12.30" in element:
            abort_date = element
            mail_body[title] = abort_date

    return check_mail.check("계좌정보통합관리서비스", mail_body)