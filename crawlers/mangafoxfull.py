from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from utils import clean
import time

def url_scheme():
    return "https://mangafoxfull.com/manga/"

chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works
driver = webdriver.Chrome(options=chrome_options)

RAW_URL = "https://mangafoxfull.com/manga/return-of-immortal-emperor/chapter-1/"
temp = RAW_URL.split("/")
URL = "/".join(temp[:-2]) +"/"
print(URL)

driver.get(URL)
#allc = driver.find_element(By.CLASS_NAME, 'allc')
#title = allc.text.lstrip('All chapters are in')
#new_link = allc.find_element(By.TAG_NAME, 'a').get_attribute('href')
#print(new_link)
#driver.get(new_link)

time.sleep(5)
list_chapters = driver.find_elements(By.CLASS_NAME, 'wp-manga-chapter')
title = driver.find_element( By.CLASS_NAME, "post-title").find_element(By.TAG_NAME, 'h1').get_attribute('innerHTML')
print(title)

for chapter in list_chapters:
    a = chapter.find_element(By.TAG_NAME, 'a')
    url = a.get_attribute('href')
    chapter_title = a.get_attribute('innerHTML').strip()
    print(chapter_title, url)

driver.quit()
