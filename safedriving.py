from selenium import webdriver
from email.mime.image import MIMEImage
import os
import check_mail
import datetime
import PIL
from PIL import Image
import pytesseract
from PIL import Image
from pytesseract import *
import cv2
pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def go():

	#===================================================#
	#메일에 들어갈 내용
	mail_body = {}
	#오늘날짜
	today = datetime.datetime.now()
	# #===================================================#
	# 헤드리스
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('window-size=1920x1080')
	options.add_argument("disable-gpu")
	driver = webdriver.Chrome('chromedriver', options=options)
	driver.get("https://www.safedriving.or.kr/main.do")

	#화면 최대화
	driver.maximize_window()
	#스크린샷
	filename = os.getcwd() + "/todayscreen" + ".png"
	shot = driver.get_screenshot_as_file(filename)
	driver.quit()

	#이미지에서 텍스트 읽기
	image = cv2.imread('todayscreen.png', cv2.IMREAD_COLOR)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	image = cv2.bitwise_not(image)
	image = cv2.resize(image, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
	cv2.imwrite('1invert.jpg', image)
	image = PIL.Image.fromarray(image)
	text = pytesseract.image_to_string(image, 'kor').split('\n')

	# MIMEImage로 변환
	fp = open("todayscreen.png", 'rb')
	img = MIMEImage(fp.read())
	fp.close()

	#오늘날짜가 있으면 메일 보내기
	for item in text:
		item = item.replace(" ", "").replace(',','.')
		if str(today.month) + "." + str(today.day) in item:
			mail_body["도로교통공단 안전운전 통합민원"] = item
			return check_mail.check("도로교통공단 안전운전 통합민원",mail_body,attach_img=img)
	return check_mail.check("도로교통공단 안전운전 통합민원", {})