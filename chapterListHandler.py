from dataclasses import dataclass
from statistics import mean, median
from typing import List
from crawler_handler import call_crawler, get_chapters_crawler
from utils import clean_title, open_with_json
import time
import multiprocessing
import json
from mongo import update, update_serie, remove_serie, get_serie, get_series, get_database, add_serie, set_updated, get_updated

@dataclass
class Chapter:
    url: str
    name: str
    read: bool = False

    def __repr__(self):
        return f"Chapter({self.name})"
    
    def __eq__(self, other: object):
        if other is not None:
            return self.name == other.name
        else:
            return False


@dataclass
class Serie:
    title: str
    sites: List
    date: float
    state: bool
    chapters: list
    preview: str = ''

    def get_infos(self):
        last_chap = self.chapters[-1] if len(self.chapters) > 0 else None
        last_read = self.get_last_chapter_read()
        return {
            'title':self.title,
            'last_chapter':"None" if last_chap is None else [last_chap.name, last_chap.url, last_chap.read],
            'last_chapter_read':"None" if last_read is None else [last_read.name, last_read.url, last_read.read],
            'site':self.sites[0],
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

    def mongo(self):
        return {
            'title':self.title,
            'sites':self.sites,
            'chapters': self.chapters_json(),
            'preview': self.preview,
            'state': self.state,
            'date': self.date}

    def chapters_json(self):
        return [[chapter.name, chapter.url, chapter.read] for chapter in self.chapters]

    def __eq__(self, __o: object) -> bool:
        return self.title == __o.title


class Handler:
    series: List[Serie]
    lock: object
    def __init__(self) -> None:
        print("Getting data from the database...")
        #data = get_series()
        data = open_with_json("chapterList.json")
        print("Done !")
        self.series = [Serie(
            title = title,
            sites = serie['sites'], 
            date = float(serie['date']), 
            state = serie['state'], 
            preview = serie["preview"], 
            chapters = [Chapter(url = chapter[1], name = chapter[0], read = chapter[2]) for chapter in serie["chapters"]]
        ) for (title, serie) in data.items()]

        self.lock = multiprocessing.Lock()

    def reload(self) -> None:
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

    def update(self) -> None:
        current_time = time.time()
        log = get_updated()
        update_time = log['log']
        if current_time - update_time > 86000: #check if one day has passed (i.e 24h)
            for i,serie in enumerate(sorted(self.series, key=lambda x: x.date, reverse=True)):
                try:
                    chapters = get_chapters_crawler(*serie.sites)
                    unpacked = [chapter.name for chapter in serie.chapters]
                    count = 0
                    for chapter in chapters:
                        if chapter[0] not in unpacked:
                            count += 1
                            serie.chapters.append(Chapter(url = chapter[1], name = chapter[0]))
                    if count != 0: #new chapters have been found
                        update_serie(serie)
                        print(f"{i/len(self.series)*100} %", count, serie.title)
                    else:
                        print(f"{i/len(self.series)*100} %")
                except Exception as err:
                    print(err, serie.title, serie.sites)

            set_updated(time.time())
            self.save()

    def delete(self, title: str) -> None:
        serie = self.get_serie(title)
        if serie:
            self.series.remove(serie)
            remove_serie(serie)
            self.save()

    def drop(self, title: str) -> None:
        serie = self.get_serie(title)
        if serie:
            serie.state = "dropped"
            update_serie(serie)
            self.save()

    def read_until(self, title: str, chapterName: str) -> None:
        serie = self.get_serie(title)
        if serie:
            for chapter in serie.chapters:
                chapter.read = True
                if chapter.name == chapterName:
                    break
            update_serie(serie)
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
                    update_serie(serie)
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
        serie = Serie(title = title, sites = [site,url], date=time.time(), state="reading", chapters = [])
        self.log(f"add {title} {url}\n")

        chapters, preview = call_crawler(site, title, url)
        chapters = [Chapter(name = chapter[0], url = chapter[1]) for chapter in chapters]

        serie.chapters = chapters
        serie.preview = preview

        self.series.append(serie)
        add_serie(serie)
        self.save()

    def following(self, title: str, site: str) -> bool:
        serie = self.get_serie(title)
        return False if serie is None else site == serie.sites[0]

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
                series_list.sort(key=lambda x: x.sites[0])

        return [serie.get_infos() for serie in series_list]

    def save(self):
        data = {}
        for serie in self.series:
            data[serie.title] = {
                'sites':serie.sites,
                'chapters': serie.chapters_json(),
                'preview': serie.preview,
                'state': serie.state,
                'date': serie.date
            }

        with self.lock:
            with open("chapterList.json", 'w') as file:
                json.dump(data, file)

    def log(self, message):
        pass
    
def convert_to_float(number: str) -> float:
    if ':' in number:
        number = number.rstrip(':')
    if number.isdecimal() or '.' in number:
        return float(number)
    if '-' in number:
        if '-' == number[-1]:
            return float(number[:-1])
        number = number.replace('-','.')
        return float(number)
    if ',' in number:
        number = number.replace(',','.')
        return float(number)
    raise ValueError

def extract_chapter_number(name: str) -> float:
    name = name.lower()
    if any([x in name for x in ["extra", "bonus", "special", "hiatus"]]):
        return 0.0
    index = name.find("chapter")
    if index == -1:
        if name.find("ch.") == -1:
            if name.find("episode") == -1:
                raise ValueError
            else:
                index = name.find("episode")
                name = name[index:]
                a = name.lstrip("episode").split(' ')
        else:
            index = name.find("ch.")
            name = name[index:]
            a = name.lstrip("ch.").split(' ')
    else:        
        name = name[index:]
        a = name.lstrip("chapter ").split(' ')
    if len(a) > 1:
        return convert_to_float(a[0])
    else:
        return convert_to_float(a[0])

if __name__ == "__main__":
    handler = Handler()
    for serie in handler.series:
        last = serie.get_last_chapter_read()
        if last is None:
            print(serie.title)
        else:
            continue