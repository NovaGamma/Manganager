import requests
import os
from bs4 import BeautifulSoup
import sys
import time
from progressBar import Progress
import re

def get_page(text):
    return text.split('-')[1]

def get_pages(soup):
    pages = []
    temp = soup.find_all('div',class_ = "container-chapter-reader")
    temp = temp[0]
    images = temp.find_all('img')
    for item in images:
        if item.name == 'img':
            url = item.attrs["src"].strip()
            page_number = url.split('/')[-1].rstrip('.jpg')
            if re.search("-[a-z]", page_number):
                page_number = "".join(re.split("-[a-z]", page_number))
            pages.append([page_number,url])
    return pages

def get_chapter_list(soup):
    s = soup.find_all('select',class_ = "navi-change-chapter")
    data = s[0].find_all('option')
    print(data[0]['data-c'])
    result = [base_url+'-'+item['data-c'] for item in data if item != '\n']
    return result

def clean(list):
    for item in list:
        if item == '\n':
            list.remove('\n')
    return list

def filtering(string):
    if not string.isalnum():
        if string == " ":
            return True
        return False
    return True

path = sys.argv[1]
startChapter = int(sys.argv[2])
r = requests.get(path)
soup = BeautifulSoup(r.text,'html.parser')
div = soup.find_all('div',class_="panel-breadcrumb")[0]
name = ''.join(filter(filtering, div.find_all('a',class_="a-h")[1]['title'])).replace(' ','-')

dirName = f"static/manga/{name}"
if not(os.path.exists(dirName)):
    os.mkdir(dirName)

base_url = '-'.join(path.split('-')[:-1])

result = get_chapter_list(soup)[::-1]
print('Found {} chapters !\nThe first {}'.format(len(result),result[0]))
#print('Found {} chapters !\nThe first is chapter number {}'.format(len(result),result[0].attrs['data-redirect'].split('/')[-1]))
for chapter in result[startChapter:]:
    t0 = time.time()
    nBroken = 0
    url = chapter
    chapter_number = url.split('-')[-1]
    print(chapter_number)
    chapter_request = requests.get(url)
    chapter_soup = BeautifulSoup(chapter_request.text,'html.parser')
    pages = get_pages(chapter_soup)
    if not os.path.exists(f"{dirName}/Chapter {chapter_number}/"):
        os.mkdir(f"{dirName}/Chapter {chapter_number}/")
    p = Progress(len(pages))
    p.start()
    for page in pages:
        p.next()
        page_url = page[1]
        img_type = '.'+page_url.split('.')[-1]
        if not os.path.exists(dirName+"/Chapter "+str(chapter_number)+'/page '+page[0]+img_type):
            image = requests.get(page_url,headers ={"referer":"https://readmanganato.com/"})
            if image.status_code==404:
                print(f"error 404 {page_url}\n{image}")
                continue
            with open(dirName+"/Chapter "+str(chapter_number)+'/page '+page[0]+img_type,'wb') as f:
                f.write(image.content)
    t1 = time.time()
    sys.stdout.write(f"{t1-t0} s\n")
