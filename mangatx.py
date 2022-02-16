from bs4 import BeautifulSoup
import requests
from utils import clean

#MangaTx.com

def url_scheme():
    return "https://mangatx.com/manga/"

RAW_URL = "https://mangatx.com/manga/above-all-gods/chapter-300/"
temp = RAW_URL.split("/")
print (temp[:-2])
URL = "/".join(temp[:-2]) +"/"
print (URL)

r = requests.get(URL)
if r.status_code == 200:
    soup = BeautifulSoup(r.text, "html.parser")
    chapterList = soup.find_all("li", class_="wp-manga-chapter")
    print (chapterList[0])
    lastChapter = clean(chapterList[0].contents)[0]
    print(lastChapter)
    '''
    linkLastChapter = lastChapter.attrs["href"]
    print (linkLastChapter)
    chapterName = lastChapter.contents[0].strip()
    print (chapterName)
    chapterNumber = float(chapterName.lstrip("Chapter "))
    print (type(chapterNumber) is float)'''
