from bs4 import BeautifulSoup
import requests
from utils import clean

#mangadex.tv

def url_scheme():
    return "https://mangadex.tv/chapter/manga"

RAW_URL = "https://mangadex.tv/chapter/manga-bn978870/chapter-2004"

raw_r = requests.get(RAW_URL)
raw_soup = BeautifulSoup(raw_r.text, "html.parser")
link_container = raw_soup.find("a", class_="manga-link")
title = link_container.attrs['title']
URL = "https://mangadex.tv" + link_container.attrs['href']
print(URL, title)

r = requests.get(URL)
if r.status_code == 200:
    soup = BeautifulSoup(r.text, "html.parser")
    chapterList = soup.find_all("div", class_="row no-gutters")
    chapter = chapterList[1].find("a", class_="text-truncate")
    url = chapter.attrs['href']
    chapter_name = chapter.contents[0]
    print(chapter_name, url)
    '''
    for col in chapterList:
        a = clean(li.contents)[0]
        url = a.attrs['href']
        chapter_name = a.contents[0].strip()
        print(chapter_name, url)
    name = soup.find('ol', class_ = "breadcrumb").contents
    title = clean(name[3].contents)[0].contents[0].strip()
'''
