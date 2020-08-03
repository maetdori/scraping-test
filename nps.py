from bs4 import BeautifulSoup
from urllib.request import urlopen
import check_mail
import datetime
import json
import logging

#log config
with open("./globalval.json",'r') as file:
    json_data = json.load(file)
file_name = json_data["log_file_path"]
log_level = json_data["log_level"]

logging.basicConfig(filename=file_name,level=log_level)

def go():
	# ===================================================#
	# 메일에 들어갈 내용
	mail_body = {}
	# 오늘날짜
	today = datetime.datetime.now()
	today = str(today.strftime('%y/%m/%d'))
	# ===================================================#
	html = urlopen('https://www.nps.or.kr/jsppage/app/cms/list.jsp?cmsId=news')
	soup = BeautifulSoup(html, 'html.parser')
	soup = soup.find_all('td', {'class':'tl'})
	for i in soup:
		title = i.get_text()
		# 공지 제목에 '중단'이 있으면 들어가서 날짜 확인후 이미지 가져오기
		if '중단' in title:
			href = 'https://www.nps.or.kr/jsppage/app/cms/' + i.find('a').get('href')
			html = urlopen(href)
			detail_soup = BeautifulSoup(html, 'html.parser')
			date = detail_soup.find('dd',{'class':'view_dd2_2'}).get_text()
			if today in date:
				img = detail_soup.find('dl', {'class':'view_dl3'})
				try:
					mail_body[title] = img.find('img').get('src')
				except:
					pass
	return check_mail.check("국민연금공단", mail_body)