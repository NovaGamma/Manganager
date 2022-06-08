from bs4 import BeautifulSoup
import requests
try:
    from crawlers.utils import clean
except:
    from utils import clean


def url_scheme():
    return "https://mangakakalot.com/manga-"

def get_soup(RAW_URL):
    URL = RAW_URL.split('/')[:3]+['manga']+[RAW_URL.split('/')[4]]
    URL = '/'.join(URL) + '/'
    r = requests.get(URL)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        return soup

def get_preview(RAW_URL, title):
    soup = get_soup(RAW_URL)
    box = soup.find('div', class_= "manga-info-pic")
    url = clean(box.contents)[0].attrs['src']

    img_type = url.split('.')[-1]
    image = requests.get(url)
    with open(f"static/previews/{title}.{img_type}",'wb') as f:
        f.write(image.content)
    return f"{title}.{img_type}"

def get_title(RAW_URL):
    soup = get_soup(RAW_URL)
    info = soup.find('ul', class_ ='manga-info-text')
    return clean(clean(info.contents)[0].contents)[0].contents[0]

def get_chapter_list(RAW_URL):
    soup = get_soup(RAW_URL)
    chapter_list = soup.find('div', class_ = "chapter-list")
    chapter_list = clean(chapter_list.contents)
    chapterList = []
    for chapter in chapter_list:
        a = clean(chapter.contents)[0].contents[0]
        chapter_name = a.contents[0]
        url = a.attrs['href']
        chapterList.append(chapter_name, url)
    return chapterList


#print(get_preview("https://mangakakalot.com/chapter/nc923742/chapter_237","Divine Hero’s Skyfall System"))
#print(get_chapter_list("https://mangakakalot.com/chapter/nc923742/chapter_237"))
