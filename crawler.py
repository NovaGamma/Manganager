import os
import importlib

for crawler in os.listdir("crawlers/"):
    if crawler.endswith('.py'):
        name = crawler.rstrip('.py')
        module = importlib.import_module('crawlers.'+name)
        print(module.url_scheme())
