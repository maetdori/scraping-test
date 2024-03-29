# notice_scrap
사용자의 컴퓨터 환경에 따라서 **tesseract**와 **chromedriver**설치를 각각 해줘야 한다.   
[chromedriver_상세설명](https://beomi.github.io/2017/02/27/HowToMakeWebCrawler-With-Selenium/ "chromedriver 설정 방법블로그")       
현재 자신의 컴퓨터에 설치된 크롬 버전을 확인하려면 크롬브라우저를 열어 **chrome://version**을 친다.  
[chromedriver 다운](https://sites.google.com/a/chromium.org/chromedriver/home "다운링크")   
[tesseract](https://github.com/UB-Mannheim/tesseract/wiki "tesseract 다운링크")  
chromedriver는 **safedriver , payinfo , hikorea**의 공지를 가져올 때 사용함.  
chormedriver는 설치 후, 소스내에서 wevdriver.Chrome()에서 경로를 기존의것에서 변경하여 사용.  
tesseract은 **savedriver**의 공지를 가져올 때 사용한다.

리눅스(linux)에서 **chromedriver,tesseract**를 실행시 파일에 따로 실행파일확장자가 없기 때문에 실행권한을 따로 줘야하고, safedriving.py의 options.add_argument의 내용도 바뀐다.  
#### options.add_argument('--headless')  
#### options.add_argument('--no-sandbox')  
#### options.add_argument("disable-dev-shm-usage")


그 외 외부 라이브러리 설치가 많다.
* pip install httplib2
* pip install selenium
* pip install pillow
* pip install opencv-python   opencv같은 경우 aws나 google cloud와 같은 가상환경에서 실행할 경우에 GUI가 없을 가능성이 높아서 **pip install opencv-python-headless**를 설치해야함.
* pip install beautifulsoup4
* pip install requests
* pip install logging
* pip install pytesseract


파일들에서 쓰이는 공통 변수는 globalval.json에 넣어놨다.  
파일 경로를 변경하고 싶으면 globalval.json에서 변경한다.  
json작성시 loglevel 참고.  
#### CRITICAL = 50,
#### FATAL = CRITICAL,
#### ERROR = 40,
#### WARNING = 30,
#### WARN = WARNING,
#### INFO = 20,
#### DEBUG = 10,
#### NOTSET = 0

## 공지사항 url 
**정부24(gov24)**  : https://www.gov.kr/portal/ntcItm?Mcode=11186  
**건강보험공단(nhis)** : https://si4n.nhis.or.kr/jpca/JpCad00101.do
!["nhis 공지사항"](nhis.PNG)    
**국민연금(nps)** : https://www.nps.or.kr/jsppage/news/new_news/new_news_01.jsp  
**안전운전통합민원(safedriving)** : https://www.safedriving.or.kr/main.do  
**계좌정보통합관리서비스(payinfo)** : https://www.payinfo.or.kr/account.html  
**하이코리아(hikorea)** : https://www.hikorea.go.kr/board/BoardNtcListR.pt?page=1  ,https://www.hikorea.go.kr/Main.pt
!["hikorea 공지사항"](hikorea.PNG)      
**자동차민원 대국민포털(ecar)** : http://www.ecar.go.kr/Index.jsp
!["ecar 공지사항"](ecar.PNG)   
**인터넷 등기소(iros)** : http://www.iros.go.kr/pos1/pfrontservlet?cmd=PCMS6GetBoardC&menuid=001004003001&boardTypeID=2
!["iros 공지사항"](iros.PNG)   
**전자가족관계(efamily)** : http://efamily.scourt.go.kr/index.jsp
!["efamily 공지사항"](efamily.PNG)  


