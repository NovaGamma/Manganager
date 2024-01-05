import os, requests
import importlib

class Error(Exception):

    def __init__(self, error_message = ''):
        self.error_message = error_message
        super().__init__(self.error_message)

def call_crawler(site, title, url):
    for crawler in os.listdir("crawlers/"):
        if crawler.endswith('.py'):
            name = crawler.rstrip('.py')
            if name == site:
                module = importlib.import_module('crawlers.'+name)
                #check if the url correspond to the right site
                if url.startswith(module.url_scheme()):
                    if module.type() == 'selenium':
                        try:
                            driver = module.get_page(url)
                            chapter_list = module.get_chapter_list(driver)
                            preview = module.get_preview(driver, title)
                            driver.quit()
                        except:
                            print(url)
                            raise Exception
                    else:
                        chapter_list = module.get_chapter_list(url)
                        preview = module.get_preview(url, title)
                    return [chapter_list, preview]
                else:
                    raise Error('URL does not correspond to the url_scheme')

def get_preview_crawler(site, title, url):
    for crawler in os.listdir("crawlers/"):
        if crawler.endswith('.py'):
            name = crawler.rstrip('.py')
            if name == site:
                module = importlib.import_module('crawlers.'+name)
                #check if the url correspond to the right site
                if url.startswith(module.url_scheme()):
                    if module.type() == 'selenium':
                        driver = module.get_page(url)
                        preview = module.get_preview(driver, title)
                        driver.quit()
                    else:
                        preview = module.get_preview(url, title)
                else:
                    raise Error('URL does not correspond to the url_scheme')

def get_chapters_crawler(site, url):
    for crawler in os.listdir("crawlers/"):
        if crawler.endswith('.py'):
            name = crawler.rstrip('.py')
            if name == site:
                module = importlib.import_module('crawlers.'+name)
                #check if the url correspond to the right site
                if url.startswith(module.url_scheme()):
                    if module.type() == 'selenium':
                        try:
                            driver = module.get_page(url)
                            chapter_list = module.get_chapter_list(driver)
                            driver.quit()
                        except:
                            r = requests.get(url)
                            if(r.status_code == 404):
                                print(url)
                                return []
                            else:
                                raise Exception
                    else:
                        chapter_list = module.get_chapter_list(url)
                    return chapter_list
                else:
                    raise Error('URL does not correspond to the url_scheme')

def crawler_search(title, site):
    for crawler in os.listdir("crawlers/"):
        if crawler.endswith('.py'):
            name = crawler.rstrip('.py')
            if name == site:
                module = importlib.import_module('crawlers.'+name)
                url = module.search(title)
                return url


def get_title_crawler(site, url):
    for crawler in os.listdir("crawlers/"):
        if crawler.endswith('.py'):
            name = crawler.rstrip('.py')
            if name == site:
                module = importlib.import_module('crawlers.'+name)
                #check if the url correspond to the right site
                if url.startswith(module.url_scheme()):
                    title = module.get_title(url)
                    return title
                else:
                    raise Error('URL does not correspond to the url_scheme')
