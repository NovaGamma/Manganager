import requests
import os
from bs4 import BeautifulSoup
import sys
import time

def get_page(text):
    return text.split('-')[1]

def get_pages(soup):
    temp = soup.find('div',id="readerarea")
    temp2 = temp.find_all('p')

    pages = []
    for number, item in enumerate(temp2):
        page_number = str(number+1)
        if('src' in item.contents[0].attrs):
            url = item.contents[0].attrs['src'].strip()
            pages.append([page_number,url])
    return pages

def get_chapter_list(soup):
    print(soup)
    s = soup.find_all('ul', class_ = "clstyle")
    print(s[0])
    result = [item.contents[1].contents[1].contents[1].attrs['href'] for item in s[0].contents if not (item == '\n' or item == ' ')]
    return result

def clean(list):
    for item in list:
        if item == '\n':
            list.remove('\n')
    return list

path = sys.argv[1]
name = path.split('/')[4]
dirName = f"static/manga/{name}"
if not(os.path.exists(dirName)):
    os.mkdir(dirName)
r = requests.get(path)
soup = BeautifulSoup(r.text,'html.parser')
result = get_chapter_list(soup)
print('Found {} chapters !'.format(len(result)))
result = result[::-1]
for chapter in result:
    t0 = time.time()
    url = chapter
    chapter_number = url.split('/')[-2].split('-')[-1]
    print(chapter_number)
    chapter_request = requests.get(url)
    chapter_soup = BeautifulSoup(chapter_request.text,'html.parser')
    pages = get_pages(chapter_soup)
    if not os.path.exists(f"{dirName}/Chapter {chapter_number}/"):
        os.mkdir(f"{dirName}/Chapter {chapter_number}/")
    for page in pages:
        page_url = page[1]
        img_type = '.'+page_url.split('.')[-1]
        if not os.path.exists(dirName+"/Chapter "+str(chapter_number)+'/page '+page[0]+img_type):
            image = requests.get(page_url,headers ={"referer":"https://mangakakalot.com/"})
            if image.status_code==404:
                print(f"error 404 {page_url}\n{image}")
                continue
            with open(dirName+"/Chapter "+str(chapter_number)+'/page '+page[0]+img_type,'wb') as f:
                f.write(image.content)
    t1 = time.time()
    sys.stdout.write(f"{t1-t0} s\n")
