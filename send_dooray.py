# import urllib2
import smtplib
import urllib.request
import json
from email._header_value_parser import Header
from email.mime.text import MIMEText
import requests
from requests import Request
from httplib2 import Http

def send_dooray_noti(name,noti_total, k):
    # req = urllib.request.urlopen(url, json.dups(data), {'Content-Type': 'application/json'}).read()
    # return req

    url = "https://hook.dooray.com/services/2271045959672406714/2803437871967119166/92V0y5P1Sc6GYp_R5xX3pA"
    data = {
        "botName": "공지사항 봇",
        "text":  " 금일 하기 사이트는 공지사항이 없습니다. ("+str(k)+"/"+str(noti_total)+")",
        "attachments": [
            {
                "text": name,
                "color": "#FFD700"
            }
        ]
    }
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, data=data)
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers= {'Content-Type': 'application/json'},
        body= json.dumps(data),
    )

def send(title):
    str1 = ""
    try:
        str1 = str(bytes(title), encoding="utf-8")
    except:
        str1 = str(title)
    print(1)
    # data = {
    #     "botName": "DocBot",
    #     "botIconImage": "https://translate.nhnent.com/icon/botimage.jpg",
    #     "text": str(sitetype) + " 공지 확인 결과",
    #     "attachments": [
    #         {
    #             "title": str1,
    #             "text": str(content),
    #             "color": "#FFD700"
    #         }
    #     ]
    # }
    # data = {}
        # data[title] = "오늘 공지 없음."
        # # send_dooray_noti("ce38fc65d4@fhx.dooray.com",
        # #                  data)
        # sender_account = "no_reply@flyhigh-x.com"
        # sender_password = "mail@flyhigh9"
        # s = smtplib.SMTP_SSL("smtp.dooray.com", "465")
        # s.login(sender_account, sender_password)
        # to = ['ce38fc65d4@fhx.dooray.com']
        # cc = []
        # bcc = ['ce38fc65d4@fhx.dooray.com']
        # msg = MIMEText("오늘 공지 없음", "html", _charset="utf-8")
        # msg['Subject'] = title
        # msg['From'] = sender_account
        # msg['To'] = 'ce38fc65d4@fhx.dooray.com'
        # s.sendmail(sender_account, [sender_account] + to + cc + bcc, msg.as_string())
        # s.quit()
    print(title)
def test_send(sitetype, title, content):
    data = {
        "botName": "DocBot",
        "botIconImage": "https://translate.nhnent.com/icon/botimage.jpg",
        "text": sitetype + " 공지 확인 결과",
        "attachments": [
            {
                "title": title,
                "text": content,
                "color": "#FFD700"
            }
        ]
    }

    send_dooray_noti("https://hook.dooray.com/services/2271045959672406714/2418073129534065736/2nkpAeNiQDaGVzhuua661Q", data)
    
