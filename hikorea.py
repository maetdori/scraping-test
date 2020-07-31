from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import check_mail


def go():
	#===================================================#
	#메일에 들어갈 내용
	mail_body = {}

	#오늘날짜
	today = datetime.datetime.now()
	#===================================================#
	# 헤드리스
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('window-size=1920x1080')
	options.add_argument("disable-gpu")
	driver = webdriver.Chrome('chromedriver', options=options)
	wait = WebDriverWait(driver, 20)
	driver.get(
		'https://www.hikorea.go.kr/pt/NtcCotnPageR_kr.pt?bbsNm=%EA%B3%B5%EC%A7%80%EC%82%AC%ED%95%AD&bbsGbCd=BS10&langCd=KR&bbsSeq=1&locale=ko')

	soup = BeautifulSoup(driver.page_source, 'html.parser')
	td = soup.find_all('td', {'class': 'tdData'})

	for i in range(1, 3):
		# 오늘날짜인 공지가 있으면 들어가서 내용 가져오기
		if today in td:
			xpath = '//*[@id="contents"]/table/tbody/tr[%d]/td[2]/a' % i
			wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

			soup = BeautifulSoup(driver.page_source, 'html.parser')
			td = soup.find_all('td', {'class': 'tdData'})
			title = td[0].get_text()
			mail_body[title] = soup.find('div',{'class':'insertHtml'}).get_text()
			driver.back()
		else:
			break
	driver.quit()

	return check_mail.check("하이코리아", mail_body)