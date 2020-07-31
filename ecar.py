# -*- coding:utf-8 -*-
# import cookielib.cookiejar
import http.cookiejar
import urllib.request, urllib.error
import send_email
import send_dooray
import requests
from bs4 import BeautifulSoup


def go():
    # make session
    # cj = cookielib.CookieJar()
    cj = http.cookiejar.LWPCookieJar()
    # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    # access to notification page and get html
    html = opener.open("http://www.ecar.go.kr/Services").read()

    # parse html
    soup = BeautifulSoup(html, "html.parser")

   # print(soup)


go()
