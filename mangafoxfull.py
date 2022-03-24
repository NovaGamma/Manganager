from bs4 import BeautifulSoup
import requests
from utils import clean

# Mangafoxfull.com


def url_scheme():
    return "https://mangafoxfull.com/manga/"


RAW_URL = "https://mangafoxfull.com/manga/sousei-no-onmyouji/chapter-104/"
temp = RAW_URL.split("/")
URL = "/".join(temp[:-2]) + "/"
print(URL)

r = requests.get(URL)
if r.status_code == 200:
    soup = BeautifulSoup(r.text, "html.parser")
    chapterList = soup.find_all("li", class_="wp-manga-chapter")
    print(soup)
    for li in chapterList:
        a = clean(li.contents)[0]
        url = a.attrs['href']
        chapter_name = a.contents[0].strip()
        print(chapter_name, url)
    name = clean(soup.find('ol', class_="breadcrumb").contents)
    title = clean(name[3].contents)[0].contents[0].strip()
    print(title)
