from parsel import Selector
import requests
try:
    from crawlers.utils import clean
    from crawlers.utils import save_preview
except:
    from utils import clean
    from utils import save_preview

#MangaTx.com


def url_scheme():
    return "https://mangatx.to/"

def type():
    return 'parsel'

def get_page(url, title, recursive = False):
    #test validity of url
    r = requests.get(url)
    if r.status_code != 200 and not recursive:
        if "/manga/" in url:
            soup = get_page(url.replace("/manga/", "/manhua/"), True)
            return soup
    temp = url.split("/")
    URL = "/".join(temp[:-2]) +"/"
    r = requests.get(URL)
    if r.status_code == 200:
        soup = Selector(text=r.text)
        return soup
            

def get_preview(soup, title):
    soup.css(".summary_image img::attr(src)").get()
    return save_preview(title, url)

def get_title(soup):
    title = soup.css(".breadcrumb")[-1].css('a::text').get().strip()
    return title

def get_chapter_list(soup):
    chapterList = soup.css(".wp-manga-chapter")
    chapter_list = []
    for chapter in chapterList:
        url = chapter.css("a::attr(href)").get()
        chapter_name = chapter.css("a::text").get().strip()
        chapter_list.append((chapter_name, url))
    return chapter_list[::-1]

if __name__ == '__main__':
    url = "https://mangatx.to/manga/reincarnation-of-the-hero-party-archmage/chapter-0/"
    soup = get_page(url)
    title = get_title(soup)
    chapter_list = get_chapter_list(soup)
    print(chapter_list)