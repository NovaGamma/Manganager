from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from utils import clean

def url_scheme():
    return "https://www.asurascans.com/"

chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works
driver = webdriver.Chrome(options=chrome_options)
start_url = "https://www.asurascans.com/talent-swallowing-magician-chapter-19/"
driver.get(start_url)
search_div = driver.find_element(By.ID, 'chapter').text
title = driver.find_element(By.CLASS_NAME, 'allc').text.lstrip('All chapters are in')
print(title)
print(clean([chapter.strip() for chapter in search_div.split('\n')][1:]))


driver.quit()
