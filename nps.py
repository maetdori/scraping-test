from bs4 import BeautifulSoup
from urllib.request import urlopen
import check_mail
import datetime
import json
import logging
import urllib
import PIL
import pytesseract
from PIL import Image

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
	# ===================================================#
	html = urlopen('https://www.nps.or.kr/jsppage/app/cms/list.jsp?cmsId=news')
	soup = BeautifulSoup(html, 'html.parser')
	soup = soup.find_all('td', {'class':'tl'})
	for i in soup:
		title = i.get_text()
		# 공지 제목에 '중단'이 있으면 들어가서 날짜 확인후 이미지 가져오기
		if '중단' in title:
			# 상세페이지
			href = 'https://www.nps.or.kr/jsppage/app/cms/' + i.find('a').get('href')
			html = urlopen(href)
			
			detail_soup = BeautifulSoup(html, 'html.parser')
			dl = detail_soup.find('dl', {'class':'view_dl3'})

			# 공지사항 이미지 받아오기
			img_url = dl.find('img').get('src')
			urllib.request.urlretrieve(img_url, 'nps' + '.png')

			# 이미지 텍스트 변환
			img = Image.open('nps.png')
			text = pytesseract.image_to_string(img, lang='kor')
			
			content = text.replace(". ", ".").replace(" ~ ", "~")
			if str(today.month) + "." + str(today.day) in content:
				mail_body[title] = img_url
				
	return check_mail.check("국민연금공단", mail_body)