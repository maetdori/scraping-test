# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import json
import time
import datetime

import check_mail
import send_email

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
	noti_data = {}

	req = urllib.request.urlopen("https://si4n.nhis.or.kr/jpza/JpZaa00101.do")

	html = req.read()
	html_decode = html.decode("utf-8")
	soup = BeautifulSoup(html_decode, "html.parser")

	noti_data["banner"] = []

	# find all banner from front page
	banner_list = soup.find_all("div", attrs={"class", "banner"})

	for banner in banner_list:
		# skip when invisible div
		if "display:none;" in banner.attrs["style"]:
			continue

		# make dict
		banner_dict = {}
		li_list = banner.find_all("li")
		if len(li_list) >= 3:
			banner_dict["term"] = li_list[0].contents[1].strip()
			banner_dict["reason"] = li_list[1].contents[1].strip()
			banner_dict["target"] = li_list[2].contents[1].strip()

			abort_date = banner_dict["term"]
			abort_why = banner_dict["reason"]
			abort_thing = banner_dict["target"]
			title = "점검 일정"
			content = "공단은 국민들에게 더 나은 인터넷 서비스를 제공하고자 다음과 같이 시스템 점검을 실시함을 알려드립니다."
			mail_body[title] = abort_date
		noti_data["banner"].append(banner_dict)

	url = "http://www.nhis.or.kr/bbs7/messages/boardMessages?boardKey=100&sort=sequence&order=desc&rows=10&messageCategoryKey=&pageNumber=1&viewType=generic&targetType=12&targetKey=100&status=&period=&startdt=&enddt=&queryField=&query="
	headers = {"Accept": "application/json"}
	req = urllib.request.Request(url, headers=headers)

	json_resp = urllib.request.urlopen(req).read()
	json_resp = str(json_resp, "utf-8")
	message = json.loads(json_resp)
	noti_list = message["page"]["list"]

	noti_data["noti"] = []

	for noti in noti_list:
		noti_dict = {}
		date_str = time.strftime("%Y-%m-%d", time.localtime(int(noti["updateDate"]/1000)))

		noti_dict["title"] = noti["title"]
		noti_dict["contents"] = noti["contents"].strip()
		noti_dict["date"] = date_str

		if date_str == today.strftime("%Y-%m-%d"):

			noti_data["noti"].append(noti_dict)
			utf_title = noti_dict["title"]

			mail_body[utf_title] = noti_dict["contents"]

	check_mail.check("건강보험공단(+사회보험통합징수포털)", mail_body)
	return go_popup()
def go_popup():
	# ===================================================#
	# 메일에 들어갈 내용
	mail_body = {}

	# 오늘날짜
	today = datetime.datetime.now()
	# ===================================================#
	req = urllib.request.urlopen('https://www.nhis.or.kr/serviceBreakPopup.html ')
	html = req.read()
	soup = BeautifulSoup(html, 'html.parser')
	title = ""
	why = soup.find('div', {'class': 'detail'})
	why = str(why.find('li').text.strip()).split("•")[1]
	mail_body[title] = why
	if str(today.year) + "." + str(today.month) + "." + str(today.day) in why:
		return check_mail.check("건강보험공단(+사회보험통합징수포털)", mail_body)
	today = today + datetime.timedelta(days=1)
	if str(today.year) + "." + str(today.month) + "." + str(today.day) in why:
		return check_mail.check("건강보험공단(+사회보험통합징수포털)", mail_body)

	return check_mail.check("건강보험공단 팝업",{})