import requests
import os
import sys
from bs4 import BeautifulSoup

def get_pages(soup):#mangatx
    pages = []
    temp = soup.find_all('div',class_ = "separator")
    for item in temp:
        url = item.contents[0].attrs['href']
        page_number = url.rstrip('.jpg')[-3:]
        pages.append([page_number,url])
    return pages


path = sys.argv[2]
dirName = "C:/Users/NovaGamma/Documents/Tower Of Gods"
if not(os.path.exists(dirName)):
    os.mkdir(dirName)

for i in range(2,489):
    url = "https://thetowerofgod.com/manga/tower-of-god-chapter-"+str(i)+"/"
    r = requests.get(path)
    soup = BeautifulSoup(r.text,'html.parser')
    pages = get_pages(soup)
    chapter_number = i
    for page in pages:
        page_url = page[1]
        image = requests.get(page_url)
        if image.status_code==404:
            nBroken += 1
            print("error 404")
        print("Page {} Chapter {}".format(page[0],i))
        pagePath = dirName +"/Chapter "+str(chapter_number)+' page '+str(int(page[0])+1)+".png"
        if not(os.path.exists(pagePath)):
            with open(pagePath,'wb') as f:
                f.write(image.content)
