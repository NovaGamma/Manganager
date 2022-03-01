from bs4 import BeautifulSoup
import requests
from utils import clean

def url_scheme():
    return "https://mangakakalot.com/manga-"

URL = "https://mangakakalot.com/chapter/nc923742/chapter_237"

r = requests.get(URL)
if r.status_code == 200:
    soup = BeautifulSoup(r.text, "html.parser")
    new_link = soup.find('div', class_ = "breadcrumb breadcrumbs bred_doc")
    bread = clean(clean(clean(new_link.contents)[0].contents)[2].contents)[0]
    title = bread.attrs['title']
    link = bread.attrs['href']
    print(title, link)

    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    chapter_list = soup.find('div', class_ = "chapter-list")
    chapter_list = clean(chapter_list.contents)
    for chapter in chapter_list:
        a = clean(chapter.contents)[0].contents[0]
        chapter_name = a.contents[0]
        url = a.attrs['href']
        print(chapter_name, url)
