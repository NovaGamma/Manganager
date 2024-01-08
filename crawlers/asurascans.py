from difflib import SequenceMatcher
from bs4 import BeautifulSoup
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
    return "bs4"

def get_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    allc = soup.find('div', class_='allc')
    new_url = allc.contents[1].attrs['href']
    new_r = requests.get(new_url)
    new_soup = BeautifulSoup(new_r.text, "html.parser")
    return new_soup

def get_chapter_list(soup):
    list_chapters = soup.find_all('div', class_="eph-num")
    chapterList = []
    for chapter in list_chapters:
        a = clean(chapter.contents)[0]
        url = a.attrs['href']
        chapter_title = clean(clean(a.contents)[0].contents)[0]
        chapterList.append((chapter_title, url))
    return chapterList[::-1]

def get_preview(soup, title):
    div = soup.find('div', class_="thumb")
    img = clean(div.contents)[0]
    url = img.attrs['src']
    return save_preview(title, url)

def get_title(RAW_URL):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    allc = soup.find('div', class_='allc')
    title = allc.contents[1].contents[0]
    return title

def search(title):
    base_url = "https://asuratoon.com/?s="
    url = base_url + title
    url = url.replace(' ', '%20')
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all('div', class_='bsx')
    if(len(results) > 0):
        a = clean(results[0].contents)[0]
        search_title = a.attrs['title']
        seq = SequenceMatcher(None, title.lower().strip(), search_title.lower().strip())
        if seq.ratio() > 0.9:
            return a.attrs['href']
        elif len(results) > 1:
            for result in results[1:]:
                a = clean(result.contents)[0]
                search_title = a.attrs['title']
                seq = SequenceMatcher(None, title.lower().strip(), search_title.lower().strip())
                if seq.ratio() > 0.9:
                    return a.attrs['href']


if __name__ == '__main__':
    url = "https://asuratoon.com/0873280421-star-embracing-swordmaster-chapter-1/"
    soup = get_page(url)
    title = get_title(url)
    chapter_list = get_chapter_list(soup)
    print(chapter_list)
    #print(title, chapter_list)
    #print(search('The Dark Mage s Return to Enlistment'))
    #preview = get_preview(driver, title)
    #print(chapter_list)
    #driver.quit()