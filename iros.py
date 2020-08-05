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
<<<<<<< HEAD
	
	#
	f = open("./response.txt", "w")
	f.write(str(html))
	f.close()

=======
>>>>>>> 0ef302b0c6c72710b99a35d493f7dae767eeaf55
	# parse html
	soup = BeautifulSoup(html, "html.parser")
	
	# find noti title / date / content
	noti_list = []
	noti_table = soup.find("table")
	for tr in noti_table.find_all("tr"): # 1 tr for 1 notice
		if tr.td == None: continue	# skip when td is None
		td = tr.find_all("td")

		# get title / date
<<<<<<< HEAD
		title = td[0].get_text().strip()
		date = td[1].get_text().strip()
=======
		title = tr.td.get_text().strip()
		date = tr.td.next_sibling.next_sibling.string
>>>>>>> 0ef302b0c6c72710b99a35d493f7dae767eeaf55

		# test compare date with today
		if date != today.strftime("%Y-%m-%d"):	# skip when not today
			continue

		logging.debug(title + date)
		
		# access noti detail page for get content
<<<<<<< HEAD
		html = opener.open("http://www.iros.go.kr" + td[0].a["href"]).read().decode('euc-kr')
=======
		html = opener.open("http://www.iros.go.kr" + tr.a["href"]).read().decode('euc-kr')
>>>>>>> 0ef302b0c6c72710b99a35d493f7dae767eeaf55

		# parse html
		sub_soup = BeautifulSoup(html, "html.parser")
		for br in sub_soup.find_all("br"):
			br.replace_with("\n")

		# get content
		content = sub_soup.find(class_="view_con")
		content_str = content.get_text()
		content_str = content_str.strip()
<<<<<<< HEAD

=======
>>>>>>> 0ef302b0c6c72710b99a35d493f7dae767eeaf55
		# append noti_list
		noti = {
			"title":title,
			"date":date,
			"content":content_str
		}
		noti_list.append(noti)
		
		logging.debug(noti_list)

	noti_list.sort(key=lambda x: x["date"], reverse=True)

	if len(noti_list) == 0:
		return check_mail.check("인터넷 등기소", mail_body)
	else:
		new = True
		abort_date = "N"
		abort_why = "N"
		abort_thing ="N"
		for noti in noti_list:
			for item in noti["content"].split("○"):
				#abort_date
				if abort_date == "N" and "중단일시" in item and "중단대상" in item:
					abort_date = item[:item.index('중단대상')]
				if "중단일시"  in item and abort_date == "N":
					abort_date = item
				if "중단 일시" in item:
					abort_date = item[item.find('중단 일시'):item.index('※')]

				#abort_why
				if "중단사유" in item or "작업사유" in item:
					abort_why = item[item.find('작업사유'):]

				#abort_thing
				if "중단대상" in item:
					abort_thing = item[item.find('중단대상'):item.find('※')]
				if "중단 대상" in item:
					abort_thing = item

			mail_body[noti["title"]] = abort_date
			return check_mail.check("인터넷 등기소", mail_body)

