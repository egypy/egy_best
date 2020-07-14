from fastapi import FastAPI
from typing import Optional
from b64 import Tag64
from base64 import b64encode
from egy_best import (
    Site,
    Actor,
    Home,
    Serie,
    Movie,
    Season,
    Episode
)

app = FastAPI()
session = Site()


@app.get("/")
def read_root():
    return {"error": "NO!"}


@app.get("/search")
def search(q: str):
    resutls = session.search(q)
    content = dict()
    for i, r in enumerate(resutls):
        info = r.get_thumbnail_info()
        # info['thumbnail'] = Tag64(f"https:{info['thumbnail']}", 'img').html_tag
        info['type'] = r.page_type
        info['url'] = r.link
        if r.page_type == 'series':
            info['seasons'] = f'/seasons?url={r.link}'
        else:
            info['downloadinfo'] = f'/downloadinfo?url={r.link}'
        content.update({i: info})
    return content


@app.get("/filter/{material}")
def filter(material, q):
    # return session.supported
    if material in session.supported:
        rs = session.filter(material, q.split('-'))
        if rs:
            content = dict()
            for i, r in enumerate(rs):
                info = r.get_thumbnail_info()
                info['type'] = r.page_type
                info['url'] = r.link
                if r.page_type == 'series':
                    info['seasons'] = f'/seasons?url={r.link}'
                else:
                    info['downloadinfo'] = f'/downloadinfo?url={r.link}'
                content.update({i: info})
            return content
    return {'error': 'Nothing Has Been Found'}


@app.get("/seasons")
def seasons(url: str):
    return {n:
            {'title': s.title, 'url': s.link, 'episodes': f'/episodes?url={s.link}', 'thumbnail': s.thumbnail}
            for n, s in enumerate(Serie(url).seasons)}


@app.get("/episodes")
def episodes(url: str):
    return {n:
            {
                'url': s.link,
                'title': s.title,
                'thumbnail': s.thumbnail,
                'downloadinfo': f'/downloadinfo?url={s.link}'
            } for n, s in enumerate(Season(url).episodes)}


@app.get('/downloadinfo')
def download(url: str):
    if 'episode' in url:
        c = Episode
    elif 'movie' in url:
        c = Movie
    ob = c(url)
    rr = ob.get_source_link()
    if rr:
        return rr
    return {'error': 'Bad Usage'}
