from bs4 import BeautifulSoup
import requests
from utils import clean

#Isekaiscanmanga.com

def url_scheme():
    return "https://isekaiscanmanga.com/manga/"

RAW_URL = "https://isekaiscanmanga.com/manga/a-bad-person/chapter-80/"
temp = RAW_URL.split("/")
URL = "/".join(temp[:-2]) +"/"
print (URL)


r = requests.get(URL)
if r.status_code == 200:
    soup = BeautifulSoup(r.text, "html.parser")
    chapterList = soup.find_all("li", class_="wp-manga-chapter")
    for li in chapterList:
        a = clean(li.contents)[0]
        url = a.attrs['href']
        chapter_name = a.contents[0].strip()
        print(chapter_name, url)
    name = soup.find('ol', class_ = "breadcrumb").contents
    title = clean(name[3].contents)[0].contents[0].strip()
