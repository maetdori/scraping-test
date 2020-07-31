from bs4 import BeautifulSoup
import urllib.request
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

import send_email

import check_mail
import time

def go():
    # ===================================================
    # 메일에 들어갈 내용
    mail_body = {}
    # 오늘날짜
    today = datetime.datetime.now()

    # ===================================================
    # 헤드리스
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome('chromedriver', options=options)
    # 사이트 접속
    wait = WebDriverWait(driver, 20)
    driver.get('https://www.payinfo.or.kr/index.do')
    time.sleep(5)
    driver.switch_to.frame('startframe')
    driver.switch_to.frame('startframe')
    driver.find_element_by_xpath('//*[@id="gnb"]/li[7]/a').click()

    # 데이터 수집
    for i in range(1,4):
        xpath = '//*[@id="contents"]/div/table/tbody/tr[%d]/td[2]'%i
        if i > 1:
            driver.switch_to.frame('startframe')
            driver.switch_to.frame('startframe')
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        
        try:
            # 날짜 구하기
            notice_date = str(soup.find_all('span', {'class': 'bar'}))
            notice_date = re.sub('<.+?>', '', notice_date, 0).strip().replace('[', '').replace(']', '').split('.')
            notice_date = datetime.date(int(notice_date[0]),int(notice_date[1]),int(notice_date[2]))
        except:
            return "!!!계좌정보 통합관리 에러!!!"
        title = str(soup.find('th',{'scope':'col'}))
        title = re.sub('<.+?>', '', title, 0).strip().replace('[','').replace(']','')
        # 오늘 날짜와 같다면?
        if today == notice_date:
            # 이미지
            soup = soup.find('td', {'class': 'context'})
            if 'img' in str(soup):
                imgUrl = soup.find('img').get('src')
                mail_body[title] = imgUrl
                urllib.request.urlretrieve(imgUrl, "." + 'adldi%d'%i)
            # 텍스트
            else:
                text = str(soup).replace('<br/>','\n')
                text = re.sub('<.+?>', '', text, 0).strip().replace('[', '').replace(']', '')
                mail_body[title] = text
        else:
            break
        driver.back()

    driver.quit()
    mail_body = dict(sorted(mail_body.items(), key=lambda x: x[0]))
    return check_mail.check('계좌정보 통합관리', mail_body)


