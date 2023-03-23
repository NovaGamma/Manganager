from pymongo import MongoClient

def get_database():

    CON_URL = "mongodb+srv://manganager:sftN3kZofIEKo0pU@cluster0.lqaeztq.mongodb.net/test"

    client = MongoClient(CON_URL)

    return client['elvin']

def get_collection_series():
    db = get_database()
    return db['elvin']

def updated(id):
    db = get_database()
    collection = db["logs"]
    data = collection.find()
    for el in data:
        if "updater" in el.keys():
            collection.find_one_and_replace(el, {"updater":id})

def get_serie(serie):
    collection = get_collection_series()
    return collection.find_one({"title": serie.title})

def update_serie(serie) -> None:
    collection = get_collection_series()
    collection.replace_one(get_serie(serie), serie.mongo())

def add_serie(serie) -> None:
    collection = get_collection_series()
    collection.insert_one(serie.mongo())

def remove_serie(serie) -> None:
    collection = get_collection_series()
    collection.delete_one(serie.mongo())

def update(id):
    db = get_database()
    collection = db["logs"]
    for el in collection.find():
        if "updater" in el.keys():
            if collection.find_one(el) == id:
                return False
    return True

def set_updated(time):
    db = get_database()
    collection = db["logs"]
    for el in collection.find():
        if "log" in el.keys():
            collection.find_one_and_replace(el, {"log":time})

def get_updated():
    db = get_database()
    collection = db["logs"]
    for el in collection.find():
        if "log" in el.keys():
            return el

def get_series() -> dict:
    collection = get_collection_series()
    series = {}
    for serie in collection.find():
        serie.pop("_id")
        series[serie['title']] = {**serie}
    return series

if __name__ == "__main__":
    print(get_collection_series())