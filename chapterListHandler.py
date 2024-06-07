from dataclasses import dataclass
from typing import List
from crawler_handler import call_crawler, get_chapters_crawler, crawler_search
from utils import clean_title, open_with_json, save_with_json
import time
import multiprocessing
import json
import functools
from logger import log


def save(func):
    @functools.wraps(func)
    def inner(self, *arg, **kw):
        func(self, *arg, **kw)
        self.saving()
    return inner

@dataclass
class Chapter:
    url: str
    name: str
    number: float = ''

    def __repr__(self):
        return f"Chapter({self.name})"
    
    def __eq__(self, other: object):
        if other is not None:
            return self.number == other.number
        else:
            return False

class ChaptersWrapper(dict):
    def __init__(self, chapters):
        super().__init__({
            float(number): Chapter(name=chapter[0], url=chapter[1], number=chapter[2])
            for number, chapter in chapters.items()
        })

    @property
    def last_chapter(self):
        return self[max(self, key=float)]

@dataclass
class Serie:
    title: str
    date: float
    state: bool
    chapters: dict
    read: list
    preview: str = ''
    last_chapter: float = 0
    last_chapter_read: float = 0

    def get_infos(self):
        return {
            'title': self.title,
            'last_chapter': self.last_chapter,
            'last_chapter_read': "None" if self.last_chapter_read == 0 else self.last_chapter_read,
            'sites': list(self.chapters.keys()),
            'date': self.date,
            'state': self.state,
            'read': self.read,
        }

    def read_chapter(self, data) -> None:
        chapter_number = data['chapter_number']
        if(not data['site'] in self.chapters.keys()):
            return
        
        self.date = time.time()
        self.read.append(chapter_number)
        self.read.sort()
        self.last_chapter_read = chapter_number if chapter_number > self.last_chapter_read else self.last_chapter_read

        if not chapter_number in self.chapters[data['site']].keys():
            self.chapters[data['site']][chapter_number] = Chapter(data['url'], data['chapterName'], chapter_number)

    def mongo(self):
        return {
            'title':self.title,
            'sites':self.sites,
            'chapters': self.chapters_json(),
            'preview': self.preview,
            'state': self.state,
            'date': self.date}

    def chapters_json(self):
        return {
            site: { 
                number: [chapter.name, chapter.url, chapter.number] for number, chapter in chapters.items()
            } for site, chapters in self.chapters.items()
        }

    def __eq__(self, __o: object) -> bool:
        return self.title == __o.title

class Handler:
    series: List[Serie]
    lock: object
    def __init__(self) -> None:
        print("Opening data file...")
        data = open_with_json("chapterList.json")
        print("Loading data from file...")
        self.load_data(data)
        print("Done !")
        self.lock = multiprocessing.Lock()

    def load_data(self, data):
        self.series = [Serie(
            title = title,
            date = float(serie['date']),
            state = serie['state'],
            preview = serie["preview"],
            last_chapter = serie["last_chapter"],
            last_chapter_read = serie["last_chapter_read"],
            read = [float(number) for number in serie["read"]],
            chapters = {
                site: ChaptersWrapper(chapters)
                for site, chapters in serie['chapters'].items()
            }
        ) for (title, serie) in data.items()]

    def reload(self) -> None:
        with open("chapterList.json",'r') as file:
            data = json.load(file)
        self.load_data(data)

    @save
    def update(self) -> None:
        current_time = time.time()
        log = open_with_json('log.json')
        update_time = log['update']
        if current_time - update_time > 86000: #check if one day has passed (i.e 24h)
            for i,serie in enumerate(sorted(self.series, key=lambda x: x.date, reverse=True)):
                #can be multithreaded
                for site in serie.chapters:
                    try:
                        chapters = get_chapters_crawler(site, serie.chapters[site].last_chapter.url, serie.title)
                        count = 0
                        for chapter in chapters:
                            chapter_number = extract_chapter_number(chapter[0])
                            if chapter_number not in serie.chapters[site]:
                                count += 1
                                serie.chapters[site][chapter_number] = Chapter(name = chapter[0], url = chapter[1], number = chapter_number)
                                if chapter_number > serie.last_chapter:
                                    serie.last_chapter = chapter_number
                            else:
                                if serie.chapters[site][chapter_number].url != chapter[1]:
                                    serie.chapters[site][chapter_number].url = chapter[1]
                        if count != 0: #new chapters have been found
                            print(f"{i/len(self.series)*100} %", count, serie.title)
                        else:
                            print(f"{i/len(self.series)*100} %")
                    except Exception as err:
                        print(err, serie.title, site, serie.chapters[site].last_chapter.url)
            import psutil
            processes = psutil.process_iter()
            for process in processes:
                if(process.name() == "firefox.exe"):
                    p = psutil.Process(process.pid)
                    p.kill()
                    print(f"Process ID: {process.pid}, Name: {process.name()}")
            print("killed remanant firefox processes")
            save_with_json({"update": time.time()}, 'log.json')

    @save
    def delete(self, title: str) -> None:
        serie = self.get_serie(title)
        if serie:
            self.series.remove(serie)

    @save
    def drop(self, title: str) -> None:
        serie = self.get_serie(title)
        if serie:
            serie.state = "dropped"

    @save
    def read_until(self, title: str, chapterNumber: float) -> None:
        serie = self.get_serie(title)
        if serie:
            for site in serie.chapters:
                chapters = [chapter_number for chapter_number, _ in serie.chapters[site].items() if float(chapter_number) <= float(chapterNumber)]
                for chapter in chapters:
                    if chapter not in serie.read:
                        serie.read.append(chapter)

            serie.read.sort()
            serie.last_chapter_read = serie.read[-1]
            #update_serie(serie)

    @save
    def read_chapter(self, data: dict) -> None:
        chapterName = data['chapterName']
        title = clean_title(data['title'])
        site = data['site']
        serie = self.get_serie(title)
        if serie:
            number = extract_chapter_number(chapterName)

            #means that the chapter isn't in the list
            if number not in serie.chapters[site]:
                try:
                    chapters = get_chapters_crawler(site, serie.chapters[site].last_chapter.url, serie.title)
                    for chapter in chapters:
                        chapter_number = extract_chapter_number(chapter[0])
                        if chapter_number not in serie.chapters[site]:
                            serie.chapters[site][chapter_number] = Chapter(name = chapter[0], url = chapter[1], number = chapter_number)
                            if chapter_number > serie.last_chapter:
                                serie.last_chapter = chapter_number
                        else:
                            if serie.chapters[site][chapter_number].url != chapter[1]:
                                serie.chapters[site][chapter_number].url = chapter[1]
                except Exception as err:
                    print(err, serie.title, site, serie.chapters[site].last_chapter.url)

            if number not in serie.read:
                #chapter has not been read on any site before
                data['chapter_number'] = number
                serie.read_chapter(data)
                
                print(f"read {title} {number} on {site}\n")
                    

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

    @save
    def add_site(self, title: str, site: str) -> None:
        serie = self.get_serie(title)
        if(site in serie.chapters.keys()):
            return
        #hardcoded for asurascans
        url = crawler_search(title, site)
        if(not url is None):
            print(url)
            chapters = get_chapters_crawler(site, url)

            serie.chapters[site] = {
                extract_chapter_number(chapter[0]): Chapter(name = chapter[0], url = chapter[1], number = extract_chapter_number(chapter[0]))
                for chapter in chapters
            }

            chapters_number = list(serie.chapters[site].keys())
            chapters_number.sort()

            if chapters_number[-1] > serie.last_chapter:
                serie.last_chapter = chapters_number[-1]

    @save
    def add_follow(self, title: str, site: str, url: str) -> None:
        serie = self.get_serie(title)
        add_serie = False
        if(not serie):
            add_serie = True
            serie = Serie(
                title = title,
                date=time.time(),
                chapters={},
                state="reading",
                read = [],
                last_chapter_read = 0.0
            )

        elif site in serie.chapters.keys():
            return
        
        print(f"add {title} {url}\n")

        chapters, preview = call_crawler(site, title, url)

        print(chapters)
        serie.chapters[site] = {
            extract_chapter_number(chapter[0]): Chapter(name = chapter[0], url = chapter[1], number = extract_chapter_number(chapter[0]))
            for chapter in chapters
        }

        last_chapter = list(serie.chapters[site].keys())
        last_chapter = last_chapter[-1]

        if(serie.last_chapter and last_chapter > serie.last_chapter):
            serie.last_chapter = last_chapter

        if add_serie:
            serie.preview = preview
            serie.last_chapter = last_chapter
            self.series.append(serie)

    def following(self, title: str, site: str) -> bool:
        serie = self.get_serie(title)
        return False if serie is None else site in serie.chapters.keys()

    def get_read_list(self, kwargs) -> list:
        series_list = [serie for serie in self.series if serie.state != "dropped"]
        if "finished" in kwargs and kwargs["finished"] == "true":
            series_list = [serie for serie in series_list if serie.last_chapter_read != serie.last_chapter]

        if "sort" in kwargs:
            if kwargs["sort"] == "date":
                series_list.sort(key=lambda x: x.date, reverse=True)

            elif kwargs["sort"] == "remaining":
                def ratio(serie: Serie) -> int:
                    last_chap_read = serie.last_chapter_read
                    if last_chap_read is None:
                        index = 0
                    else:
                        index = last_chap_read
                    return (index+1)/(serie.last_chapter+1)
                series_list.sort(key=ratio)
            
            elif kwargs["sort"] == "sites":
                series_list.sort(key=lambda x: x.sites[0])

        return [serie.get_infos() for serie in series_list]

    def saving(self):
        data = {}
        for serie in self.series:
            data[serie.title] = {
                'chapters': serie.chapters_json(),
                'preview': serie.preview,
                'state': serie.state,
                'date': serie.date,
                'last_chapter': serie.last_chapter,
                'last_chapter_read': serie.last_chapter_read,
                'read': serie.read
            }

        with self.lock:
            with open("chapterList.json", 'w') as file:
                json.dump(data, file)
    
def convert_to_float(number: str) -> float:
    if ':' in number:
        number = number[:number.index(':')]
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
    return 0.0

def extract_chapter_number(name: str) -> float:
    name = name.lower()
    if ' ' in name: #checking UTF-8 character <0xa0>
        name = name.replace(' ', ' ')
    if any([x in name for x in ["extra", "bonus", "special", "hiatus", "notice", "hitaus", "bounus"]]):
        return 0.0
    index = name.find("chapter")
    if index == -1:
        if name.find("ch.") == -1:
            if name.find("episode") == -1:
                try: #if name is only the number of the chapter
                   number = float(name) 
                   return number
                except:
                    return 0.0 #has not found any corespondance
            else:
                index = name.find("episode")
                name = name[index:]
                a = name.lstrip("episode ").split(' ')
        else:
            index = name.find("ch.")
            name = name[index:]
            a = name.lstrip("ch.").split(' ')
    else:        
        name = name[index:]
        a = name.lstrip("chapter ").split(' ')
    try:
        return convert_to_float(a[0])
    except:
        return 0.0

if __name__ == "__main__":
    handler = Handler()
    for serie in handler.series:
        last = serie.last_chapter_read
        if last is None:
            print(serie.title)
        else:
            continue