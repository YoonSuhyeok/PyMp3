# parser.py
import requests
from bs4 import BeautifulSoup
import re
import pytube
import os
import subprocess

# HTTP GET Request
req = requests.get('https://music.bugs.co.kr/')
# HTML 소스 가져오기
html = req.text
# BeautifulSoup으로 html소스를 python객체로 변환하기
# 첫 인자는 html소스코드, 두 번째 인자는 어떤 parser를 이용할지 명시.
# 이 글에서는 Python 내장 html.parser를 이용했다.
soup = BeautifulSoup(html, 'html.parser')

find100 = soup.find("div", {"class":"trackChart"}).find("a", {"class":"btnMore"})
find100 = find100.get('href')

req = requests.get(find100)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

findData = soup.find("div", {"id":"CHARTrealtime"}).findAll("p",{"class":"title"})
toplist = []
for i in findData:
	toplist.append(i.find("a", {"aria-label":"새창"}).get_text())

findArtistData = soup.find("div", {"id":"CHARTrealtime"}).findAll("p",{"class":"artist"})

ArtistList = []
for i in findArtistData:
    ArtistList.append(i.get_text())

for i in range(0, 100):
    ArtistList[i] = ArtistList[i].replace("\n", "")
    
    ArtistList[i] = ArtistList[i].replace("\r", "")

print(ArtistList)
