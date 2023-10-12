import requests
import os
from bs4 import BeautifulSoup
import sys
import time

def get_page(text):
    return text.split('-')[1]

def get_pages(soup):
    temp = soup.find_all('img',class_ = 'img-loading')
    pages = [[page['title'].rstrip(' - Mangakakalot').split(' ')[-1],page['data-src']] for page in temp]
    return pages

def get_chapter_list(soup):
    s = soup.find('select',id="c_chapter").contents
    s = clean(s)
    result = [i['value'].lstrip('chapter-') for i in s]
    return result

def clean(list):
    for item in list:
        if item == '\n':
            list.remove('\n')
    return list

def main():
    path = sys.argv[1]
    chapter_start = int(sys.argv[2])
    url_base = '-'.join(path.split('-')[:2])
    r = requests.get(path)
    soup = BeautifulSoup(r.text,'html.parser')
    name = clean(soup.find('div',class_ = 'info-top-chapter').contents)[0].contents[0].split('\n')[0].lower().replace(' ','_')
    name = ''.join(e for e in name if e.isalnum() or e == '_' or e == ' ')
    dirName = f"static/manga/{name}"
    if not(os.path.exists(dirName)):
        os.mkdir(dirName)
    result = get_chapter_list(soup)[::-1]
    print('Found {} chapters !\n'.format(len(result)))
    #print('Found {} chapters !\nThe first is chapter number {}'.format(len(result),result[0].attrs['data-redirect'].split('/')[-1]))
    for chapter in result[chapter_start:]:
        t0 = time.time()
        nBroken = 0
        url = url_base+'-'+chapter
        print(url)
        chapter_number = chapter
        print(chapter_number)
        chapter_request = requests.get(url)
        chapter_soup = BeautifulSoup(chapter_request.text,'html.parser')
        pages = get_pages(chapter_soup)
        if not os.path.exists(f"{dirName}/Chapter {chapter_number}/"):
            os.mkdir(f"{dirName}/Chapter {chapter_number}/")
        for page in pages:
            page_url = page[1]
            if not os.path.exists(dirName+"/Chapter "+str(chapter_number)+'/page '+str(page[0])+".png"):
                image = requests.get(page_url)
                if image.status_code==404:
                    print(f"error 404 {page_url}\n{image}")
                    continue
                with open(dirName+"/Chapter "+str(chapter_number)+'/page '+str(page[0])+".png",'wb') as f:
                    f.write(image.content)
        t1 = time.time()
        sys.stdout.write(f"{t1-t0} s\n")

main()
