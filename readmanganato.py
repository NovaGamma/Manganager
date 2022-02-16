from bs4 import BeautifulSoup
import requests
from utils import clean

#MangaTx.com


def url_scheme():
    return "https://readmanganato.com/manga-"

RAW_URL = "https://readmanganato.com/manga-mh989642/chapter-136"
temp = RAW_URL.split("/")
URL = "/".join(temp[:-1]) +"/"
print (URL)

r = requests.get(URL)
if r.status_code == 200:
    soup = BeautifulSoup(r.text, "html.parser")
    chapterList = soup.find_all("li", class_="a-h")
    for li in chapterList:
        a = clean(li.contents)[0]
        url = a.attrs['href']
        chapter_name = a.contents[0]
        print(chapter_name, url)
    name = clean(soup.find('div', class_ = "panel-breadcrumb").contents)
    title = name[2].attrs['title']
    print(title)
