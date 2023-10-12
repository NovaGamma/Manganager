import requests
import os
from bs4 import BeautifulSoup
import sys
import time

def get_page(text):
    return text.split('-')[1]

def get_pages(soup):#mangatx
    pages = []
    temp = soup.find_all('div',class_ = "page-break")
    for item in temp:
        page_number = get_page(item.contents[1].attrs['id'])
        url = item.contents[1].attrs["data-src"].strip()
        pages.append([page_number,url])
    return pages

def get_chapter_list(soup):
    s = soup.find_all('select',class_ = "selectpicker single-chapter-select")
    result = [item for item in s[0].contents if not (item == '\n' or item == ' ')]
    return clean(result)

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

result = result[::-1]

print('Found {} chapters !'.format(len(result)))
#print('Found {} chapters !\nThe first is chapter number {}'.format(len(result),result[0].attrs['data-redirect'].split('/')[-1]))
for chapter in result:
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
        if not os.path.exists(dirName+"/Chapter "+str(chapter_number)+'/page '+str(int(page[0])+1)+".png"):

            image = requests.get(page_url)

            if image.status_code==404:
                nBroken += 1
                print(f"error 404 {page_url}\n{image}")
                continue
            with open(dirName+"/Chapter "+str(chapter_number)+'/page '+str(int(page[0])+1)+".png",'wb') as f:
                f.write(image.content)
    t1 = time.time()
    sys.stdout.write(f"{t1-t0} s\n")
