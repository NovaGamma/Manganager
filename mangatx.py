from bs4 import BeautifulSoup
import requests
from utils import clean

#MangaTx.com


def url_scheme():
    return "https://mangatx.com/manga/"

RAW_URL = "https://mangatx.com/manga/above-all-gods/chapter-300/"
temp = RAW_URL.split("/")
URL = "/".join(temp[:-2]) +"/"
print (URL)

r = requests.get(URL)
if r.status_code == 200:
    soup = BeautifulSoup(r.text, "html.parser")
    chapterList = soup.find_all("li", class_="wp-manga-chapter")
    for li in chapterList:
        cleaned = clean(li.contents)[0].contents[0].strip()
        print(cleaned)
    name = clean(soup.find('ol', class_ = "breadcrumb").contents)
    title = clean(name[2].contents)[0].contents[0].strip()
    print(title)
