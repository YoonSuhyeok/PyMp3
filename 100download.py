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


for i in range(0, 100):
    toplist[i] = toplist[i].replace(" ", "+")

YouTubeLinkList = []
for i in toplist:
    findImage = "https://www.youtube.com/results?search_query=" + i
    YouTubeLinkList.append(findImage)
#----------------------------------------------------------------------------
for i in range(0, 100):
    toplist[i] = toplist[i].replace("+", " ")

#---------------------------------------------------------------------------

for j in range(0, 100):
    req = requests.get(YouTubeLinkList[j])
    html = req.text
    soup = BeautifulSoup(html,'html.parser')


    hrefList = []

    for i in soup.find("div", {"id":"content"}).findAll("a"):
         hrefList.append(i.get('href'))

    watchlist = []
    for i in hrefList:
      if i.find("/watch")==0:
           link = "https://www.youtube.com/" + i
           watchlist.append(link)


    yt = pytube.YouTube(watchlist[0])

    vids = yt.streams.all()

#for i in range(len(vids)):
#    print(i, '. ', vids[i])
    
    vnum = 0

    parent_dir = "./mp4"
    vids[vnum].download(parent_dir)

    new_filename = toplist[j] + ".mp3"
    default_filename = vids[vnum].default_filename


    default_filename = vids[vnum].default_filename 
    subprocess.call(['ffmpeg', '-i',                 #cmd 명령어 수행
      os.path.join('./mp4', default_filename),
      os.path.join('./mp3', new_filename)
    ])
    
    
    
    os.system("rm ./mp4/*")