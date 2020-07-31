## notice_scrap
사용자의 컴퓨터 환경에 따라서 **tesseract**와 **chromedriver**설치를 각각 해줘야 한다.   
[chromedriver_상세설명](https://beomi.github.io/2017/02/27/HowToMakeWebCrawler-With-Selenium/ "chromedriver 설정 방법블로그")  
[chromedriver 다운](https://sites.google.com/a/chromium.org/chromedriver/home "다운링크")   
[tesseract](https://github.com/UB-Mannheim/tesseract/wiki "tesseract 다운링크")  
chromedriver는 **safedriver , payinfo , hikorea**의 공지를 가져올 때 사용함.  
chormedriver는 설치 후, 소스내에서 wevdriver.Chrome()에서 경로를 기존의것에서 변경하여 사용.  
tesseract은 **savedriver**의 공지를 가져올 때 사용한다.

그 외 외부 라이브러리 설치가 많다.
* pip install httplib2
* pip install selenium
* pip install pillow
* pip install opencv-python
* pip install beautifulsoup4
* pip install requests
