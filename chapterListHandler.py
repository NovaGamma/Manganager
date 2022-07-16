from dataclasses import dataclass
from crawler_handler import call_crawler
from utils import clean_title
import time
import multiprocessing
import json

@dataclass
class Chapter:
    url: str
    name: str
    read: bool = False

    def __repr__(self):
        return f"Chapter({self.name})"

@dataclass
class Serie:
    title: str
    sites: dict
    date: float
    state: bool
    chapters: list
    preview: str = ''

    def get_infos(self):
        last_chap = self.chapters[-1]
        last_read = self.get_last_chapter_read()
        return {
            'title':self.title,
            'last_chapter':[last_chap.name, last_chap.url, last_chap.read],
            'last_chapter_read':"None" if last_read is None else [last_read.name, last_read.url, last_read.read],
            'site':list(self.sites.keys())[0],
            'date':self.date,
            'state':self.state
        }

    def get_last_chapter_read(self) -> Chapter:
        for chapter in reversed(self.chapters):
            if chapter.read:
                return chapter
        return None

    def get_chapter(self, chapterName) -> Chapter:
        for chapter in self.chapters:
            if chapter.name == chapterName:
                return chapter
        return None            

    def chapters_json(self):
        return [[chapter.name, chapter.url, chapter.read] for chapter in self.chapters]

    def __eq__(self, __o: object) -> bool:
        return self.title == __o.title


class Handler:
    series: list
    lock: object
    def __init__(self) -> None:
        with open("chapterList.json",'r') as file:
            data = json.load(file)
        self.series = [Serie(
            title = title,
            sites = serie['sites'], 
            date = float(serie['date']), 
            state = serie['state'], 
            preview = serie["preview"], 
            chapters = [Chapter(url = chapter[1], name = chapter[0], read = chapter[2]) for chapter in serie["chapters"]]
        ) for (title, serie) in data.items()]

        self.lock = multiprocessing.Lock()


    def delete(self, title):
        serie = self.get_serie(title)
        if serie:
            self.series.remove(serie)
            self.save()

    def drop(self, title):
        serie = self.get_serie(title)
        if serie:
            serie.state = "dropped"
            self.save()

    def read_until(self, title, chapterName):
        serie = self.get_serie(title)
        if serie:
            for chapter in serie.chapters:
                if chapter.name == chapterName:
                    chapter.read = True
                    break
                else:
                    chapter.read = True
            self.save()

    def read_chapter(self, data: dict) -> None:
        chapterName = data['chapterName']
        url = data['url']
        title = clean_title(data['title'])
        site = data['site']
        serie = self.get_serie(title)
        if serie:
            if site in serie.sites:
                serie.date = time.time()
                chapter = serie.get_chapter(chapterName)
                if not chapter.read:
                    chapter.read = True
                    print(data)
                    self.log(f"read {title}\n")
                    self.save()
                    

    def get_preview(self, title: str) -> str:
        serie = self.get_serie(title)
        if serie:
            return serie.preview
        return None

    def get_serie(self, title: str, lower: bool = False) -> Serie:
        for serie in self.series:
            if lower:
                if serie.title.lower() == title:
                    return serie
            else:
                if serie.title == title:
                    return serie
        else: return None

    def add_follow(self, title: str, site: str, url: str) -> None:
        if self.get_serie(title):
            return
        serie = Serie(title = title, sites = {site:url}, date=time.time(), state="reading", chapters = [])
        self.log(f"add {title} {url}\n")

        chapters, preview = call_crawler(site, title, url)
        chapters = [Chapter(name = chapter[0], url = chapter[1]) for chapter in chapters]

        serie.chapters = chapters
        serie.preview = preview

        self.series.append(serie)
        print(serie)
        print(self.series[0])
        self.save()

    def following(self, title: str, site: str) -> bool:
        serie = self.get_serie(title)
        return False if serie is None else site in serie.sites

    def get_read_list(self, kwargs) -> list:
        series_list = [serie for serie in self.series if serie.state != "dropped"]
        if "finished" in kwargs and kwargs["finished"] == "true":
            series_list = [serie for serie in series_list if serie.get_last_chapter_read() != serie.chapters[-1]]

        if "sort" in kwargs:
            if kwargs["sort"] == "date":
                series_list.sort(key=lambda x: x.date, reverse=True)

            elif kwargs["sort"] == "remaining":
                def ratio(serie: Serie) -> int:
                    last_chap_read = serie.get_last_chapter_read()
                    if last_chap_read is None:
                        index = 0
                    else:
                        index = serie.chapters.index(last_chap_read)
                    return (index+1)/len(serie.chapters)
                series_list.sort(key=ratio)
            
            elif kwargs["sort"] == "sites":
                series_list.sort(key=lambda x: x.sites.keys()[0])

        return [serie.get_infos() for serie in series_list]

    def save(self):
        process = multiprocessing.Process(target=save_function, args=(self.lock, self.series))
        process.start()

    def log(self, message):
        pass

def save_function(lock, series):
    data = {}
    for serie in series:
        data[serie.title] = {
            'sites':serie.sites,
            'chapters': serie.chapters_json(),
            'preview': serie.preview,
            'state': serie.state,
            'date': serie.date
        }

    print(data)
    with lock:
        with open("chapterList.json", 'w') as file:
            json.dump(data, file)

if __name__ == "__main__":
    handler = Handler()
    handler.save()
