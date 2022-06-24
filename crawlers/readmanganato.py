from bs4 import BeautifulSoup
import requests
try:
    from crawlers.utils import clean
    from crawlers.utils import save_preview
except:
    from utils import clean
    from utils import save_preview

def url_scheme():
    return "https://readmanganato.com/manga-"

def type():
    return "bs4"

def get_preview(RAW_URL, title):
    temp = RAW_URL.split("/")
    URL = "/".join(temp[:-1]) +"/"

    r = requests.get(URL)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        temp = soup.find("span", class_="info-image")
        url = clean(temp.contents)[0].attrs['src']

        return save_preview(title, url)


def get_chapter_list(RAW_URL):
    temp = RAW_URL.split("/")
    URL = "/".join(temp[:-1]) +"/"

    r = requests.get(URL)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        chapterList = soup.find_all("li", class_="a-h")
        chapList = []
        for li in chapterList:
            a = clean(li.contents)[0]
            url = a.attrs['href']
            chapter_name = a.contents[0]
            chapList.append((chapter_name, url))
        return chapList[::-1]


def get_title(RAW_URL):
    temp = RAW_URL.split("/")
    URL = "/".join(temp[:-1]) +"/"

    r = requests.get(URL)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        name = clean(soup.find('div', class_ = "panel-breadcrumb").contents)
        title = name[2].attrs['title']
        return title
