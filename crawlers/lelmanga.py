from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from utils import clean

def url_scheme():
    return "https://www.lelmanga.com/"

chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works
driver = webdriver.Chrome(options=chrome_options)
start_url = "https://www.lelmanga.com/martial-peak-759/"
driver.get(start_url)
allc = driver.find_element(By.CLASS_NAME, 'allc')
title = allc.text.lstrip('All chapters are in')
new_link = allc.find_element(By.TAG_NAME, 'a').get_attribute('href')
print(new_link)
driver.get(new_link)

list_chapters = driver.find_elements(By.CLASS_NAME, 'eph-num')
print(title)
for chapter in list_chapters:
    a = chapter.find_element(By.TAG_NAME, 'a')
    url = a.get_attribute('href')
    chapter_title = a.find_element(By.CLASS_NAME, 'chapternum').get_attribute('innerHTML')
    print(chapter_title, url)

driver.quit()
