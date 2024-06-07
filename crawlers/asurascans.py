from difflib import SequenceMatcher
from parsel import Selector
import requests
try:
    from crawlers.utils import clean
    from crawlers.utils import save_preview
except:
    from utils import clean
    from utils import save_preview

def url_scheme():
    return "https://asuratoon.com/"

def type():
    return "parsel"

def get_page(url, title):
    r = requests.get(url)
    if r.status_code == 404:
        new_url = search(title)
        r = requests.get(new_url)
        soup = Selector(text=r.text)
        return soup
    soup = Selector(text=r.text)
    new_url = soup.css(".allc > a::attr(href)").get()
    new_r = requests.get(new_url)
    new_soup = Selector(text=new_r.text)
    return new_soup

def get_chapter_list(soup):
    list_chapters = soup.css(".eph-num")
    chapterList = []
    for chapter in list_chapters:
        url = chapter.css("a::attr(href)").get()
        chapter_title = chapter.css(".chapternum::text").get()
        chapterList.append((chapter_title, url))
    return chapterList[::-1]

def get_preview(soup, title):
    url = soup.css(".thumb > img::attr(src)")
    return save_preview(title, url)

def get_title(soup):
    title = soup.css(".entry-title::text").get()
    return title

def search(title):
    base_url = f"{url_scheme()}/?s="
    url = base_url + title
    url = url.replace(' ', '%20')
    r = requests.get(url)
    soup = Selector(text=r.text)
    results = soup.css(".bsx")
    if(len(results) > 0):
        url = results[0].css("a::attr(href)").get()
        search_title = results[0].css("a::attr(title)").get()
        seq = SequenceMatcher(None, title.lower().strip(), search_title.lower().strip())
        if seq.ratio() > 0.9:
            return url
        elif len(results) > 1:
            for result in results[1:]:
                url = result.css("a::attr(href)").get()
                search_title = result.css("a::attr(title)").get()
                seq = SequenceMatcher(None, title.lower().strip(), search_title.lower().strip())
                if seq.ratio() > 0.9:
                    return url

if __name__ == '__main__':
    url = "https://asuratoon.com/3955407132-sleeping-ranker-chapter-100/"
    title = "Sleeping Ranker"
    soup = get_page(url, title)
    title = get_title(soup)
    chapter_list = get_chapter_list(soup)
    print(chapter_list)
    #print(title, chapter_list)
    #print(search('The Dark Mage s Return to Enlistment'))
    #preview = get_preview(driver, title)
    #print(chapter_list)
    #driver.quit()