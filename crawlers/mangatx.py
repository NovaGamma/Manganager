from bs4 import BeautifulSoup
import requests
try:
    from crawlers.utils import clean
    from crawlers.utils import save_preview
except:
    from utils import clean
    from utils import save_preview

#MangaTx.com


def url_scheme():
    return "https://mangatx.com/manga/"

def type():
    return 'bs4'

def get_soup(RAW_URL):
    temp = RAW_URL.split("/")
    URL = "/".join(temp[:-2]) +"/"
    r = requests.get(URL)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        return soup

def get_preview(RAW_URL, title):
    soup = get_soup(RAW_URL)
    temp = soup.find("div", class_="summary_image")
    url = clean(clean(temp.contents)[0].contents)[0].attrs['data-src']

    return save_preview(title, url)

def get_title(RAW_URL):
    soup = get_soup(RAW_URL)
    name = clean(soup.find('ol', class_ = "breadcrumb").contents)
    temp = clean(name[-1].contents)
    temp1 = temp[0].contents
    title = temp1[0].strip()
    return title


def get_chapter_list(RAW_URL):
    soup = get_soup(RAW_URL)
    chapterList = soup.find_all("li", class_="wp-manga-chapter")
    chapter_list = []
    for li in chapterList:
        a = clean(li.contents)[0]
        url = a.attrs['href']
        chapter_name = a.contents[0].strip()
        chapter_list.append((chapter_name, url))
    return chapter_list[::-1]
