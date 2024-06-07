from parsel import Selector
import requests
try:
    from crawlers.utils import clean
    from crawlers.utils import save_preview
except:
    from utils import clean
    from utils import save_preview

def url_scheme():
    return "https://chapmanganato.to/manga-"

def type():
    return "parsel"

def get_page(url, title):
    temp = url.split("/")
    URL = "/".join(temp[:-1]) +"/"

    r = requests.get(URL)
    return Selector(text=r.text)

def get_preview(soup, title):
    url = soup.css(".info-image > img::attr(src)").get()
    return save_preview(title, url)


def get_chapter_list(soup):
    chapterList = soup.css("li.a-h > a")
    chapList = []
    for chapter in chapterList:
        url = chapter.css("::attr(href)").get()
        chapter_name = chapter.css("::text").get().strip()
        chapList.append((chapter_name, url))
    return chapList[::-1]


def get_title(soup):
    title = soup.css(".panel-breadcrumb > a")[-1].css("::text").get()
    return title

if __name__ == '__main__':
    url = "https://chapmanganato.to/manga-om991495/chapter-61"
    soup = get_page(url)
    title = get_title(soup)
    chapter_list = get_chapter_list(soup)
    print(chapter_list)