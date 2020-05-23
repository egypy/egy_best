from lib.utils import Utils
from movie import Movie


class Actor:
    def __init__(self, link):
        self.link = link
        self.soup = Utils.page_downloader(link).find(id='mainLoad')
        for name, value in self.scrape_image().items():
            setattr(self, name, value)
        self.total_films = self._total_films()
        max = int(self.total_films[1]) if int(self.total_films) > 20 else 1
        self.movies = self.scrape_movies(max)

    def scrape_image(self):
        r = self.soup.find(class_='inline vam').a.img
        return dict(image=r['src'], name=r['alt'])

    def _total_films(self):
        r = self.soup.find(text=self.name).find_parent().find_parent()
        return ''.join([elem for elem in r.text.replace(self.name, '').split()
                        if elem.isdigit()])

    def scrape_movies(self, max=1):
        content = dict(new=list(), top=list(), popular=list(), old=list())
        for categorie in content.keys():
            for id in range(1, max+1):
                soup = Utils.page_downloader(f'{self.link}{categorie}?page={id}')
                con = soup.find(class_='movies movies_small')
                content[categorie].extend([Movie(movie['href'])
                                           for movie in con.find_all(class_='movie')])
        return content
