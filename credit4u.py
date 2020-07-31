import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date
import check_mail



def go():
    # ===================================================
    # 메일에 들어갈 내용
    mail_body = {}
    # 오늘날짜
    today = str(date.today())
    # ===================================================
    # 사이트 접속------------------------------------
    html = urlopen("http://www.credit4u.or.kr/menu06/menu0604_list.jsp?code=000&search_word=&page_num=1")
    soup = BeautifulSoup(html, "html.parser")

    # 공지 세부 페이지 접속을 위해 공지사항 제목을 모두 찾아서 한번씩 접속해보기
    notice_title = soup.find_all('td', {'class': 'txt_l'})
    for i in range(0,4):
        # 공지 세부 페이지 접속
        title_link = notice_title[i].find('a').get('href')
        ahref = 'http://www.credit4u.or.kr/menu06/' + title_link
        sub_html = urlopen(ahref)
        soup = BeautifulSoup(sub_html, 'html.parser')
        b_date = soup.find_all('span', {'class': 'b_date'})[0].get_text()

        if today in b_date:
            title = notice_title[i].get_text()
            content = str(soup.find_all('div',{'class':'b_contents'})[0]).split('<br/>')
            for i in range(0, len(content)):
                if '중단일시' in content[i]:
                    mail_body[title] = content[i + 1]
        else:
            break

    return check_mail.check('크레딧포유', mail_body)