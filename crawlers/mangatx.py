from bs4 import BeautifulSoup
import requests
try:
    from crawlers.utils import clean
except:
    from utils import clean

#MangaTx.com


def url_scheme():
    return "https://mangatx.com/manga/"

def get_preview(RAW_URL, title):
    temp = RAW_URL.split("/")
    URL = "/".join(temp[:-2]) +"/"
    r = requests.get(URL)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")

        temp = soup.find("div", class_="summary_image")
        url = clean(clean(temp.contents)[0].contents)[0].attrs['data-src']

        img_type = url.split('.')[-1]
        image = requests.get(url)
        with open(f"static/previews/{title}.{img_type}",'wb') as f:
            f.write(image.content)
        return f"{title}.{img_type}"

def get_title(RAW_URL):
    temp = RAW_URL.split("/")
    URL = "/".join(temp[:-2]) +"/"

    r = requests.get(URL)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        name = clean(soup.find('ol', class_ = "breadcrumb").contents)
        temp = clean(name[-1].contents)
        temp1 = temp[0].contents
        title = temp1[0].strip()
        return title


def get_chapter_list(RAW_URL):
    temp = RAW_URL.split("/")
    URL = "/".join(temp[:-2]) +"/"

    r = requests.get(URL)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")

        chapterList = soup.find_all("li", class_="wp-manga-chapter")
        chapter_list = []
        for li in chapterList:
            a = clean(li.contents)[0]
            url = a.attrs['href']
            chapter_name = a.contents[0].strip()
            chapter_list.append((chapter_name, url))
        return chapter_list[::-1]
