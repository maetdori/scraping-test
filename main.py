import send_email
import mw24
import gov24
import iros
import nhis
import safedriving
import hikorea
import nps
import efamily
import gygd
import credit4u
import payinfo
import send_dooray
import logging
import json

############################################################################################################################################################################################
#   mw24-민원   /goc24-정부  /iros-인터넷 등기소    /nhis-건보    /nps-국민연금공단
#   efamily-전자가족관계등록시스템 /safedriving-도로교통공단 /hikorea-하이코리아 /gygd-금융감독원 통합연금포털
#   noti_list : 사이트들의 공지를 확인하는 실행을 할 수 있는 리스트
#   noti_total : 총 개수(직관을 위해 직접 써둔다)
#   noti_string : 공지가 없는 곳들의 이름을 \n 으로 구분하여 여러 라인으로 저장
#   noti : dooray messenger 로 전송될 메시지이며 noti_string 에 있는 라인들을 넘버링하기위한 또다른 변수
#   send_mail.py : 이메일 보냄
#   send_dooray.py : messenger 로 보냄
#   check_mail.py : 메일 내용을 대충 보고 분류함
############################################################################################################################################################################################

#log config
with open("./globalval.json",'r') as file:
    json_data = json.load(file)
file_name = json_data["log_file_path"]
log_level = json_data["log_level"]

logging.basicConfig(filename=file_name,level=log_level)

# noti_list = [gov24.go(), iros.go(), nhis.go(), nps.go(), efamily.go(), safedriving.go(), hikorea.go(),  gygd.go(), credit4u.go(),payinfo.go()]  # gygd : 금융감독원 통합연금포털
noti_list = [safedriving.go()]  # gygd : 금융감독원 통합연금포털
noti_total = 11
noti_string = ""
noti = ""

#   noti_list 의 원소들을 실행시킨 return 값을 문자열로 바꾸어 noti_string 에 저장한다.
for i in noti_list:
    try:
        noti_string += str(i)
    except:
        send_email("비정상1",['에러 발생'])

#   noti_string 의 문자열을 넘버링하여 noti 로 저장.
k = 0
for i in noti_string.split("\n"):
    if i == "":
        break
    k += 1
    
    noti += str(k) + ") " + i + "\n"
#   dooray messenger 전송
if k != 0:
    send_dooray.send_dooray_noti(noti, noti_total, k)
