from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
try:
    from crawlers.utils import clean
    from crawlers.utils import save_preview
except:
    from utils import clean
    from utils import save_preview

def url_scheme():
    return "https://www.asurascans.com/"

def type():
    return "selenium"

def get_page(url):
    firefox_options = Options()
    firefox_options.add_argument("--disable-gpu")
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(options=firefox_options)

    start_url = url
    driver.get(start_url)
    allc = driver.find_element(By.CLASS_NAME, 'allc')
    new_link = allc.find_element(By.TAG_NAME, 'a').get_attribute('href')
    driver.get(new_link)
    return driver

def get_chapter_list(driver):
    list_chapters = driver.find_elements(By.CLASS_NAME, 'eph-num')
    chapterList = []
    for chapter in list_chapters:
        a = chapter.find_element(By.TAG_NAME, 'a')
        url = a.get_attribute('href')
        chapter_title = a.find_element(By.CLASS_NAME, 'chapternum').get_attribute('innerHTML')
        chapterList.append((chapter_title, url))
    return chapterList[::-1]

def get_preview(driver, title):
    div = driver.find_element(By.CLASS_NAME, 'thumb')
    img = div.find_element(By.CSS_SELECTOR, '*')
    url = img.get_attribute('src')
    return save_preview(title, url)

def get_title(RAW_URL):
    driver = get_page(RAW_URL)
    title = driver.find_element(By.CLASS_NAME, 'entry-title')
    driver.quit()
    return title