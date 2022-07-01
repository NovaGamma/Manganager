import requests

def clean(list):
    return [item for item in list if item not in ["\n","",' ']]

def save_preview(title, url):
    img_type = url.split('.')[-1]
    image = requests.get(url)
    with open(f"static/previews/{title}.{img_type}",'wb') as f:
        f.write(image.content)
    return f"{title}.{img_type}"