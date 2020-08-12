import requests
from bs4 import BeautifulSoup
import http.cookiejar
import urllib
import check_mail
import send_email
import datetime
import json
import logging

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

	#===================================================#
	# 공지사항 화면 체크 

	# make session
	cj = http.cookiejar.LWPCookieJar()
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
	url = "https://www.hikorea.go.kr/board/BoardNtcListR.pt?page=1&CATEGORY=TITLE"

	# access to notification page and get html
	html = opener.open(url).read().decode("utf-8")

	# response
	f = open("./response.txt", "w", -1, "utf-8")
	f.write(str(html))
	f.close()

	soup = BeautifulSoup(html, 'html.parser')
	table = soup.find('table', {'class': 'grid'})
	trs = table.find_all('tr')

	for tr in trs:
		if tr.td == None: 
			continue
		tds = tr.find_all('td')
		
		title = tds[2].get_text().strip()

		if "중단" in title or "점검" in title:
		#if "후베이성" in title: # test
			# access detail page to get content
			param = tds[2].find("a").get("onclick").split("'")
			seq = param[1]
			ahref = boardDetailR(seq)
			html = opener.open(ahref).read().decode('utf-8')

			f = open("./response2.txt", "w", -1, "utf-8")
			f.write(str(html))
			f.close()

			# parse html
			sub_soup = BeautifulSoup(html, "html.parser")
			table = sub_soup.find('table', {'class': 'grid'})
			content = table.find('td', {'colspan': '2'})
			content_str = content.get_text()
			content_str = content_str.strip()
			content_line = content_str.replace(". ", ".").split("\n")

			for line in content_line:
				if str(today.month) + "." + str(today.day) in line:
				#if "20.08.10" in line: # test
					abort_date = line
					mail_body[title] = abort_date	
		else: 
			continue
	#===================================================#

	#===================================================#
	# Main 화면 체크

	# make session
	cj = http.cookiejar.LWPCookieJar()
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
	url = "https://www.hikorea.go.kr/Main.pt"

	# access to notification page and get html
	html = opener.open(url).read().decode("utf-8")

	# response
	f = open("./response.txt", "w", -1, "utf-8")
	f.write(str(html))
	f.close()

	soup = BeautifulSoup(html, 'html.parser')
	table = soup.find('div', {'class': 'visual_text'})
	title = table.find('div', {'class': 'title'}).get_text().strip()
	content = table.find('div', {'class': 'desc'}).get_text().strip()

	if "점검" in title or "중단" in title:
		if str(today.month) + "." + str(today.day) in content:
			mail_body[title] = content

	#===================================================#
	return check_mail.check("하이코리아", mail_body)		

def boardDetailR(NTCCTT_SEQ):
    return "https://www.hikorea.go.kr/board/BoardNtcDetailR.pt?BBS_SEQ=1&BBS_GB_CD=BS10&NTCCTT_SEQ=" + NTCCTT_SEQ + "&page=1"
