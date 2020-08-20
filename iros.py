# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

import check_mail
import send_email
import datetime
import http.cookiejar
import urllib
import json
import logging

#log config
with open("./globalval.json",'r') as file:
    json_data = json.load(file)
file_name = json_data["log_file_path"]
log_level = json_data["log_level"]

logging.basicConfig(filename=file_name,level=log_level)

#===================================================#
#메일에 들어갈 내용
mail_body = {}
abort_date = "N"
abort_thing = "N"
abort_why = "N"

#오늘날짜
today = datetime.datetime.now()
#===================================================#


def go():

	cj = http.cookiejar.LWPCookieJar()
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

	# access to notification page and get html
	html = opener.open("http://www.iros.go.kr/pos1/pfrontservlet?cmd=PCMS6GetBoardC&menuid=001004003001&boardTypeID=2&category=").read().decode('euc-kr')
	
	# parse html
	soup = BeautifulSoup(html, "html.parser")
	
	noti_table = soup.find("tbody")

	for tr in noti_table.find_all("tr"): # 1 tr for 1 notice
		td = tr.find("td", {"class": "tl"})
		title = td.get_text()

		if "중단" in title or "점검" in title:
			html = opener.open("http://www.iros.go.kr" + td.a["href"]).read().decode('euc-kr')
			sub_soup = BeautifulSoup(html, 'html.parser')
			content = sub_soup.find('div', {'class': 'view_con'})
			content = str(content).replace("년 ", ".").replace("월 ", ".").replace("일 ", ".").split("○")
			
			for i in content:
				if str(today.month) + "." + str(today.day) in i:
					abort_date = i
					mail_body[title] = abort_date

	return check_mail.check("인터넷 등기소", mail_body)