from bs4 import BeautifulSoup
import requests
try:
    from crawlers.utils import clean
    from crawlers.utils import save_preview
except:
    from utils import clean
    from utils import save_preview

def url_scheme():
    return "https://lhtranslation.net/manga/"

def type():
    return 'bs4'

def get_soup(RAW_URL: str) -> BeautifulSoup:
    temp = RAW_URL.split("/")
    URL = "/".join(temp[:-2]) +"/"
    r = requests.get(URL)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        return soup

def get_preview(RAW_URL: str, title: str):
    soup = get_soup(RAW_URL)
    temp = soup.find("div", class_="summary_image")
    url = clean(clean(temp.contents)[0].contents)[0].attrs['data-src']
    
    return save_preview(title, url)

def get_title(RAW_URL: str) -> str:
    soup = get_soup(RAW_URL)
    name = clean(soup.find('div', class_ = "post-title").contents)
    temp = clean(name[0].contents)
    title = temp[0].strip()
    return title


def get_chapter_list(RAW_URL: str) -> list:
    temp = RAW_URL.split("/")
    URL = "/".join(temp[:-2]) +"/ajax/chapters/"
    soup = BeautifulSoup(requests.post(URL).text, "html.parser")
    chapterList = soup.find_all("li", class_="wp-manga-chapter")
    chapter_list = []
    for li in chapterList:
        a = clean(li.contents)[0]
        url = a.attrs['href']
        chapter_name = a.contents[0].strip()
        chapter_list.append((chapter_name, url))
    return chapter_list[::-1]

if __name__ == "__main__":
    print(get_chapter_list("https://lhtranslation.net/manga/isekai-cheat-magic-swordsman/chapter-19-2/"))
