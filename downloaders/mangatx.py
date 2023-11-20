import requests
import os
from bs4 import BeautifulSoup
import sys
import time

def get_page(text):
    return text.split('-')[1]

def get_pages(soup):
    pages = []
    temp = soup.find_all('div',class_ = "page-break no-gaps")
    for item in temp:
        page_number = get_page(item.contents[1].attrs['id'])
        url = item.contents[1].attrs["data-src"].strip()
        pages.append([page_number,url])
    return pages

def clean(list):
    for item in list:
        if item == '\n':
            list.remove('\n')
    return list

def download_chapter(url: str, dirName: str):
    chapter_number = url.split('/')[-2].lstrip('chapter-')
    chapter_request = requests.get(url)
    if(chapter_request.status_code == 404):
        print(f"Chapter not found : {url}")
        return
    chapter_soup = BeautifulSoup(chapter_request.text,'html.parser')
    pages = get_pages(chapter_soup)
    if not os.path.exists(f"{dirName}/Chapter {chapter_number}/"):
        os.mkdir(f"{dirName}/Chapter {chapter_number}/")
    for page in pages:
        page_url = page[1]
        img_type = '.'+page_url.split('.')[-1]
        img_path = dirName+"/Chapter "+str(chapter_number)+'/page '+str(int(page[0])+1)+img_type
        if os.path.exists(img_path) and not os.path.getsize(img_path) < 70000:
            continue
        image = requests.get(page_url)
        if not image.status_code == 200:
            print("error downloading", chapter_number, page_url)
        with open(img_path,'wb') as f:
            f.write(image.content)

path = sys.argv[1]
if len(sys.argv) < 3:
    start = 0
else:
    start = int(sys.argv[2])
name = path.split('/')[4]
dirName = f"static/manga/{name}"
if not(os.path.exists(dirName)):
    os.mkdir(dirName)
r = requests.get(path)
soup = BeautifulSoup(r.text,'html.parser')
result = get_chapter_list(soup)
print('Found {} chapters !'.format(len(result)))
for chapter in result[start:]:
    t0 = time.time()
    nBroken = 0
    url = chapter.attrs['data-redirect']
    chapter_number = url.split('/')[-2].lstrip('chapter-')
    print(chapter_number)
    chapter_request = requests.get(url)
    chapter_soup = BeautifulSoup(chapter_request.text,'html.parser')
    pages = get_pages(chapter_soup)
    if not os.path.exists(f"{dirName}/Chapter {chapter_number}/"):
        os.mkdir(f"{dirName}/Chapter {chapter_number}/")
    for page in pages:
        page_url = page[1]
        img_type = '.'+page_url.split('.')[-1]
        img_path = dirName+"/Chapter "+str(chapter_number)+'/page '+str(int(page[0])+1)+img_type
        if os.path.exists(img_path) and not os.path.getsize(img_path) < 70000:
            continue
        image = requests.get(page_url)
        if not image.status_code == 200:
            print(chapter_number,page_url)
        with open(img_path,'wb') as f:
            f.write(image.content)
    t1 = time.time()
    sys.stdout.write(f"{t1-t0} s\n")
