import os
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
                    chapter_list = module.get_chapter_list(url)
                    return chapter_list
                else:
                    raise Error('URL does not correspond to the url_scheme')
