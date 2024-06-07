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
                            driver = module.get_page(url, title)
                            chapter_list = module.get_chapter_list(driver)
                            preview = module.get_preview(driver, title)
                            driver.quit()
                        except:
                            print(url)
                            raise Exception
                    else:
                        print(url)
                        soup = module.get_page(url, title)
                        chapter_list = module.get_chapter_list(soup)
                        preview = module.get_preview(soup, title)
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
                        driver = module.get_page(url, title)
                        module.get_preview(driver, title)
                        driver.quit()
                    else:
                        module.get_preview(url, title)
                else:
                    raise Error('URL does not correspond to the url_scheme')

def get_chapters_crawler(site, url, title):
    for crawler in os.listdir("crawlers/"):
        if crawler.endswith('.py'):
            name = crawler.rstrip('.py')
            if name == site:
                old = url
                if name == "mangatx":
                    url = url.replace(".com", ".to")
                module = importlib.import_module('crawlers.'+name)
                #check if the url correspond to the right site
                if url.startswith(module.url_scheme()):
                    if module.type() == 'selenium':
                        try:
                            driver = module.get_page(url, title)
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
                        soup = module.get_page(url, title)
                        chapter_list = module.get_chapter_list(soup)
                    return chapter_list
                else:
                    if name == "asurascans":
                        url = module.search(title)
                        if url:
                            soup = module.get_page(url, title)
                            chapter_list = module.get_chapter_list(soup)
                            return chapter_list
                    raise Error(f'URL does not correspond to the url_scheme. Got: {url} expected: {module.url_scheme()}. Trace: {site} {url} note: could have been modified {old} original  {title}')

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
                    if module.type() == 'selenium':
                        try:
                            driver = module.get_page(url, '')
                            title = module.get_title(driver)
                            driver.quit()
                        except:
                            r = requests.get(url)
                            if(r.status_code == 404):
                                print(url)
                                return []
                            else:
                                raise Exception
                    else:
                        soup = module.get_page(url)
                        title = module.get_title(soup)
                    return title
                else:
                    raise Error('URL does not correspond to the url_scheme')
