from bs4 import BeautifulSoup
import requests
from crawlers.utils import clean

#MangaTx.com


def url_scheme():
    return "https://mangatx.com/manga/"

def get_chapter_list(RAW_URL):

    temp = RAW_URL.split("/")
    URL = "/".join(temp[:-2]) +"/"
    print (URL)

    r = requests.get(URL)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")

        name = clean(soup.find('ol', class_ = "breadcrumb").contents)
        title = clean(name[2].contents)[0].contents[0].strip()

        chapterList = soup.find_all("li", class_="wp-manga-chapter")
        chapter_list = []
        for li in chapterList:
            a = clean(li.contents)[0]
            url = a.attrs['href']
            chapter_name = a.contents[0].strip()
            #print(chapter_name, url)
            chapter_list.append((chapter_name, url))
        #print(title)
        return chapter_list[::-1]
