# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import io
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import date, timedelta
import re

#전일 날짜 세팅
yesterday = date.today() - timedelta(days=1)
yesterdays = yesterday.strftime(' %Y'+'년'+' %m'+'월'+' %d'+'일')
#전일 날짜와 비교 대상인 reviewDate가 list unicode라 str -> unicode로 변경 필요
yesterdays = unicode(yesterdays, "utf-8")

#무신사 APP스토어 아이디/비번
appStore_id = 'musinsa.qa@gmail.com'
appStore_pw = 'X2soft!@'

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36")
driver = webdriver.Chrome(executable_path= r'/Users/parksanghyun/Desktop/Musinsa/AutomationTest/Python/chromedriver', chrome_options=options)

driver.get('https://appstoreconnect.apple.com/login?targetPrefix=%2FWebObjects%2FiTunesConnect.woa&targetUrl=%2Fra%2Fng%2Fapp%2F1003139529%2Factivity%2Fios%2FratingsResponses&authResult=FAILED')
time.sleep(3)

#로그인 영역이 iframe이라 switch 필요 
driver.switch_to.frame("aid-auth-widget-iFrame")

time.sleep(2)
#아이디 입력
driver.find_element_by_xpath('//*[@id="account_name_text_field"]').send_keys(appStore_id)
time.sleep(2)
#화살표 클릭
driver.find_element_by_xpath('//*[@id="sign-in"]').click()
time.sleep(2)
#패스워드 입력
driver.find_element_by_xpath('//*[@id="password_text_field"]').send_keys(appStore_pw)
time.sleep(2)
#화살표 클릭
driver.find_element_by_xpath('//*[@id="sign-in"]').click()
#switch 원복
driver.switch_to_default_content()
time.sleep(20)

#로그인 영역이 iframe이라 switch 필요, 아래 인덱스0은 id가 별도 없을때 0으로 하면 전환 가능함
driver.switch_to.frame(0)

#디폴트 국가가 미국이라 클릭해서 드롭다운 리스트 노출
driver.find_element_by_xpath('//*[@id="store-fronts-selector-menu"]').click()
time.sleep(2)
#대한민국 국가 클릭
driver.find_element_by_xpath('//*[@id="store-fronts-selector"]/ul/li[21]').click()
time.sleep(15)
#switch 원복
driver.switch_to_default_content()

driver.switch_to.frame(0)
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')


titles = soup.find_all("span", attrs={"ng-bind":"review.value.title"}) #제목 가져오기
reviewContents = soup.find_all("div", attrs={"ng-bind":"review.value.review"}) #리뷰 내용 가져오기
osVersions = soup.find_all("li", attrs={"ng-bind":"l10n.interpolate('ITC.apps.universal.activity.ratings.versionNum', {NUM: review.value.appVersionString})"}) #앱 버전 가져오기
reviewDates = soup.find_all("span", attrs={"ng-bind":"l10n.interpolate('ITC.apps.r2d2.universal.activity.ratings.review.meta', {USER: review.value.nickname, DATE: ITC.time.showAbbreviatedDate(review.value.lastModified)})"}) #날짜 가져오기
stars = soup.find_all("div", attrs={"class":"stars"}) #별점 가져오기

for i in range(0, 10):
    #리뷰 작성자:XXX - 2020년 XX월 XX일 에서 년,월,일 날짜만 가져옴
    reviewDate = reviewDates[i].get_text().split('-')
    #전일 날짜와 리뷰에서 가져온 날짜가 같으면 데이터를 출력
    if yesterdays == reviewDate[1]:
        print(reviewDate[1])
        print(titles[i].get_text())
        print(reviewContents[i].get_text())
        print(osVersions[i].get_text())
        print(stars[i].get_text()) 

   


