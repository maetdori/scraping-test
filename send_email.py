# -*- coding:utf-8 -*-
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import json
import datetime
import logging
#----------------------------------------#
#민원기관별 제품 사용
#정부24(민원24) : 옴니독, 옴니체크
#하이코리아 : 옴니체크
#건강보험공단 : 옴니독
#인터넷등기소 : 옴니체크, 옴니리얼
#안전운전 : 옴니체크
#ecar : 옴니리얼
#KCB : 카뱅전용, 빼자
#----------------------------------------#
import send_dooray


def send(sitetype, dict, attach_img=None, to=[], cc=[], bcc=['odong2@flyhigh-x.com']):

    sender = "플라이하이<no_reply@flyhigh-x.com>"
    sender_account = "no_reply@flyhigh-x.com"
    sender_password = "mail@flyhigh9"

    top = """<!DOCTYPE html><html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"> <head> <meta charset="utf-8"/> <meta name="viewport" content="width=device-width"/> <meta http-equiv="X-UA-Compatible" content="IE=edge"/> <meta name="x-apple-disable-message-reformatting"/><meta name="format-detection" content="telephone=no, date=no, address=no"> <title></title> <style>/* What it does: Remove spaces around the email design added by some email clients. */ /* Beware: It can remove the padding / margin and add a background color to the compose a reply window. */ html, body{margin: 0 auto !important; padding: 0 !important; height: 100% !important; width: 100% !important;}/* What it does: Stops email clients resizing small text. */ *{-ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;}/* What it does: Centers email on Android 4.4 */ div[style*="margin: 16px 0"]{margin: 0 !important;}/* What it does: Stops Outlook from adding extra spacing to tables. */ table, td{mso-table-lspace: 0pt !important; mso-table-rspace: 0pt !important;}/* What it does: Fixes webkit padding issue. */ table{border-spacing: 0 !important; border-collapse: collapse !important; table-layout: fixed !important; margin: 0 auto !important;}/* What it does: Uses a better rendering method when resizing images in IE. */ img{-ms-interpolation-mode: bicubic;}/* What it does: Prevents Windows 10 Mail from underlining links despite inline CSS. Styles for underlined links should be inline. */ a{text-decoration: none;}/* What it does: A work-around for email clients meddling in triggered links. */ a[x-apple-data-detectors], /* iOS */ .unstyle-auto-detected-links a, .aBn{border-bottom: 0 !important; cursor: default !important; color: inherit !important; text-decoration: none !important; font-size: inherit !important; font-family: inherit !important; font-weight: inherit !important; line-height: inherit !important;}/* What it does: Prevents Gmail from changing the text color in conversation threads. */ .im{color: inherit !important;}/* What it does: Prevents Gmail from displaying a download button on large, non-linked images. */ .a6S{display: none !important; opacity: 0.01 !important;}/* If the above doesn't work, add a .g-img class to any image in question. */ img.g-img+div{display: none !important;}.logo{display: block;}/* What it does: Removes right gutter in Gmail iOS app: https://github.com/TedGoas/Cerberus/issues/89 */ /* Create one of these media queries for each additional viewport size you'd like to fix */ /* iPhone 4, 4S, 5, 5S, 5C, and 5SE */ @media only screen and (min-device-width: 320px) and (max-device-width: 374px){u~div .email-container{min-width: 320px !important;}}/* iPhone 6, 6S, 7, 8, and X */ @media only screen and (min-device-width: 375px) and (max-device-width: 413px){u~div .email-container{min-width: 375px !important;}}/* iPhone 6+, 7+, and 8+ */ @media only screen and (min-device-width: 414px){u~div .email-container{min-width: 414px !important;}}@media only screen and (max-device-width: 414px){.footer-social > td{text-align: left !important;padding-left: 0px !important;padding-right: 2px !important; padding-bottom: 10px !important;}}a[href^="x-apple-data-detectors:"]{color: inherit;text-decoration: inherit;}/* What it does: Hover styles for buttons */ .button-td, .button-a{transition: all 100ms ease-in;}.button-td-primary:hover, .button-a-primary:hover{background: #555555 !important; border-color: #555555 !important;}/* Media Queries */ @media screen and (max-width: 480px){/* What it does: Forces table cells into full-width rows. */ .stack-column, .stack-column-center{display: block !important; width: 100% !important; max-width: 100% !important; direction: ltr !important;}/* And center justify these ones. */ .stack-column-center{text-align: left !important;}/* What it does: Generic utility class for centering. Useful for images, buttons, and nested tables. */ .center-on-narrow{text-align: center !important; display: block !important; margin-left: auto !important; margin-right: auto !important; float: none !important;}table.center-on-narrow{display: inline-block !important;}/* What it does: Adjust typography on small screens to improve readability */ .email-container p{font-size: 14px !important;}.logo{display: inline-block !important;}}</style></head><body width="100%" style="margin: 0; padding: 0 !important; mso-line-height-rule: exactly; background-color: white"> <center style="width: 100%; background-color: white"><!--[if mso | IE]> <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: white;"> <tr> <td><![endif]--> <div style="max-width: 550px; margin: 0 auto;" class="email-container"><!--[if mso]> <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="550"> <tr> <td><![endif]--> <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto;"> <tr> <td style="background-color: #ffffff;"> <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%"> </table> </td></tr><tr> <td style="text-align: center; background-color: #4477cf; background-position: center center !important; background-size: cover !important;"><!--[if mso]><table align="center" role="presentation" border="0" cellspacing="0" cellpadding="0" width="100%"><tr><td width="100%" style="padding-top: 10px; padding-bottom: 10px;"><![endif]--> <div> <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="margin:auto;"> <tr> <td style="padding: 10px 15px; font-family: sans-serif; font-size: 15px; line-height: 10px; color: #ffffff;"><!--[if mso]><table role="presentation" border="0" cellspacing="0" cellpadding="0" width="100%"><tr><td width="100%" style="text-align: left; font-family: sans-serif; font-size: 15px; color: #ffffff;"><![endif]--><div style="line-height: 1.7; font-size: 1px;">&#160;</div><a href="https://www.flyhigh-x.com" title="Flyhigh" target="_blank"><img class="logo fixedwidth" border="0" src="https://d1c0ni26j4ozgk.cloudfront.net/logo_horiz.png" alt="logo" title="Image" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; clear: both; border: 0; height: auto; float: none; width: 100%; max-width:210px; display:block;" width="210"></a><div style="line-height: 1.7;font-size:1px;">&#160;</div></div></td></tr></table> </div><!--[if mso]></td></tr></table><![endif]--> </td></tr><tr> <td style="background-color: #ffffff;"><!--[if mso]> <table align="center" role="presentation" border="0" cellspacing="0" cellpadding="0" width="100%"> <tr> <td valign="top" width="100%"><![endif]--> <table align="center" role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:550px;"><tr> <td align="center" valign="top" style="font-size:12px; padding-top: 10px; color: #323a39;">"""
    body = """<h2><strong>점검 공지 안내 (%s)</strong></h2>""" % sitetype
    body += """</td></tr></table> </td></tr><tr> <td style="background-color: #ffffff;"><!--[if mso]> <table align="center" role="presentation" border="0" cellspacing="0" cellpadding="0" width="100%"> <tr> <td valign="top" width="100%"><![endif]--> <table align="center" role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:550px;"> <tr> <td align="center" valign="top" style="font-size:0; padding: 10px 0;"><!--[if mso]> <table role="presentation" border="0" cellspacing="0" cellpadding="0" width="100%"> <tr> <td valign="top" width="100%"><![endif]--> <div style="display:inline-block; margin: 0 -2px; width:100%; min-width:200px; vertical-align:top;" class="stack-column"> <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%"> <tr> <td style="padding-bottom: 10px; padding-left: 20px; padding-right: 20px;"> <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="font-size: 14px; text-align: left;"> <tr> <td style="font-family: sans-serif; font-size: 15px; line-height: 1.5; color: #555555; padding-top: 10px; line-height: 1.7" class="stack-column-center"> <p> 안녕하세요, 플라이하이입니다. </p>"""

    bot = """<br><p> 플라이하이 드림 </p></td></tr></table> </td></tr></table> </div><!--[if mso]> </td><td valign="top" width="100%"><![endif]--><!--[if mso]> </td></tr></table><![endif]--> </td></tr></table><!--[if mso]> </td></tr></table><![endif]--> </td></tr><tr> <td style="background-color: #ffffff;"> <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%"> <tr> <td style="padding-top: 24px; font-family: sans-serif; font-size: 15px; line-height: 20px; color: #4472fc; background-color: ffffff; text-align: center;"> <h5 style="margin: 0 0 10px 0;"> 플라이하이를 이용해 주셔서 감사합니다.<br>편리한 서비스를 위해 최선을 다하겠습니다. </h5> </td></tr></table> </td></tr></table> <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="max-width: 550px;"> <tr style="background-color: #132f40;"> <td> <table align="left" style="text-align: left;"> <tr> <td style="padding-right: 5px; padding-left: 20px; padding-top: 15px; padding-bottom: 15px; font-family: sans-serif; line-height: 1.7; color: #ffffff; font-size: 12px;"> <span>(주)플라이하이 <br>서울시특별시 강남구 테헤란로8길8 홍은빌딩</span><br><span>contact@flyhigh-x.com</span> </td></tr></table> </td><td width="20%" style="width:20%; padding-right: 20px;"> <table cellspacing="0" cellpadding="0" border="0" align="right" width="100%" style="text-align: right; border-collapse: collapse; border-spacing: 0; mso-table-lspace: 0pt; mso-table-rspace: 0pt; vertical-align: middle; "> <tr> <td style="padding-top: 15px; padding-bottom: 15px; margin-right: 10px; font-family: sans-serif; font-size: 12px; line-height: 1.7; text-align: right; color: #ffffff; font-size: 12px;"> <table align="right" border="0" cellspacing="0" cellpadding="0" width="32" height="32" style="border-collapse: collapse; table-layout: fixes; border-spacing: 0; mso-table-lspace: 0pt; mso-table-rspace: 0pt; vertical-align: middle; Margin-right: 10px"> <tbody> <tr style="vertical-align: middle"> <td align="left" valign="middle" style="word-break; break-word; border-collapse: collapse !important; vertical-align: middle"> <a href="https://www.facebook.com/myflyhigh" title="Facebook" target="_blank" style="display: inline-block;"> <img src="https://d1c0ni26j4ozgk.cloudfront.net/facebook@2x.png" alt="Facebook" title="Facebook" width="32" style="outline: none; text-decoration: none;-ms-interpolation-mode: bicubic;clear:both;display:inline-block !important;border:none;height: auto;float:none;max-width: 32px !important; padding: 2px;"> </a> </td></tr></tbody> </table> </td></tr></table> </td></tr></table> <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="max-width: 550px;"> <tr> <td style="padding: 10px 0px; font-family: sans-serif; font-size: 12px; line-height: 1.5; text-align: center; color: #555555;"> Copyright © FlyHigh Co., LTD. All Rights Reserved. </td></tr></table><!--[if mso]> </td></tr></table><![endif]--> </div><!--[if mso | IE]> </td></tr></table><![endif]--> </center></body></html>"""

    #스크린샷 체크 // 옴니체크
    if(sitetype == "도로교통공단 안전운전 통합민원"):

        title = "시스템 점검으로 인한 옴니체크 일시중단 안내("+sitetype+")"
        body += """<p> %s의 시스템 정기 점검으로 인해 옴니체크 서비스의 일시중단을 안내해드립니다. </p><br>""" % sitetype
        body += """- 중단일시 : %s</p>""" % dict['도로교통공단 안전운전 통합민원']

        msg = MIMEMultipart()
        msg.attach(attach_img)
        msg.attach(MIMEText(top + body + bot, "html", _charset="utf-8"))
        msg['Subject'] = Header(s=title, charset="utf-8")

    elif(sitetype == "인터넷 등기소"):

        title = "시스템 점검으로 인한 옴니리얼 일시중단 안내("+sitetype+")"
        body = """<h2><strong>점검 공지 안내 (%s)</strong></h2>""" % sitetype
        body += """</td></tr></table> </td></tr><tr> <td style="background-color: #ffffff;"><!--[if mso]> <table align="center" role="presentation" border="0" cellspacing="0" cellpadding="0" width="100%"> <tr> <td valign="top" width="100%"><![endif]--> <table align="center" role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:550px;"> <tr> <td align="center" valign="top" style="font-size:0; padding: 10px 0;"><!--[if mso]> <table role="presentation" border="0" cellspacing="0" cellpadding="0" width="100%"> <tr> <td valign="top" width="100%"><![endif]--> <div style="display:inline-block; margin: 0 -2px; width:100%; min-width:200px; vertical-align:top;" class="stack-column"> <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%"> <tr> <td style="padding-bottom: 10px; padding-left: 20px; padding-right: 20px;"> <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="font-size: 14px; text-align: left;"> <tr> <td style="font-family: sans-serif; font-size: 15px; line-height: 1.5; color: #555555; padding-top: 10px; line-height: 1.7" class="stack-column-center"> <p> 안녕하세요, 플라이하이입니다. </p>"""
        body += """<p> %s의 시스템 정기 점검으로 인해 옴니리얼 서비스의 일시중단을 안내해드립니다. <br></p>""" % sitetype

        for k in dict.keys():
            # k == noti["title"]
            body +="""<br><p style="margin:0px; padding:0px;">%s<br>""" % (k)
            # mail_body[noti["title"]] = abort_date
            body +="""%s<br></p>""" % dict[k]

        msg = MIMEText(top+body+bot, "html", _charset="utf-8")
        msg['Subject'] = Header(s=title, charset="utf-8")

    elif(sitetype == "국민연금공단"):

        title = "시스템 점검으로 인한 옴니독 일시중단 안내("+sitetype+")"
        body += """<p> %s의 시스템 정기 점검으로 인해 옴니독 서비스의 일시중단을 안내해드립니다. </p><br/> """ % sitetype
        for k in dict.keys():
            body += """<br><img src="%s"><br/>""" % (dict[k])
        msg = MIMEText(top + body + bot, "html", _charset="utf-8")
        msg['Subject'] = Header(s=title, charset="utf-8")
    elif(sitetype == "전자가족관계등록시스템"):

        title = "시스템 점검으로 인한 옴니독 일시중단 안내("+sitetype+")"
        body += """<p> %s의 시스템 정기 점검으로 인해 옴니독 서비스의 일시중단을 안내해드립니다. </p><br/> """ % sitetype
        i = 0
        for k in dict.keys():
            body += """<br><p style="margin:0px; padding:0px;"> %s<br>""" % (k)
            body += """%s</p>""" % dict[k]
            i += 1
        msg = MIMEText(top + body + bot, "html", _charset="utf-8")
        msg['Subject'] = Header(s=title, charset="utf-8")

    # 옴니독
    else:
        title = "시스템 점검으로 인한 옴니독 일시중단 안내(" + sitetype + ")"
        body += """<p> %s의 시스템 정기 점검으로 인해 옴니독 서비스의 일시중단을 안내해드립니다. </p>""" % sitetype
        if sitetype == "계좌정보 통합관리":
            for k in dict.keys():
                if 'https' in dict[k]:
                    body += """<br><p style="margin:0px; padding:0px;"> [%s]<br>""" % (k)
                    body += """<br><img src="%s"><br/>""" % (dict[k])
                else:
                    body += """<br><p style="margin:0px; padding:0px;"> [%s]<br>""" % (k)
                    body += """<br>%s""" % (dict[k])
        elif sitetype == '크레딧포유':
            for k in dict.keys():
                body += """<br><p style="margin:0px; padding:0px;">%s""" % (k)
                body += """<br> 서비스 중단 일시 %s<br>""" % (dict[k])
        else:
            i = 0
            for k in dict.keys():
                #민원24의 [전라남도 해남군]부동산종합공부시스템 민원신청 서비스
                body +="""<br><p style="margin:0px; padding:0px;"> %s<br>""" % (k)
                #중단일시: 2019.2.22(금) 18:00 ~ 2019.2.27(수) 09:00
                body +="""- %s</p>""" % dict[k]
                i+=1
        msg = MIMEText(top + body + bot, "html", _charset="utf-8")
        msg['Subject'] = Header(s=title, charset="utf-8")

    msg['From'] = sender_account
    msg['To'] = sender

    s = smtplib.SMTP_SSL('smtp.dooray.com', "465")
    s.login(sender_account, sender_password)
    s.sendmail(sender_account, [sender_account] + to + cc + bcc, msg.as_string())
    s.quit()
    return ""
