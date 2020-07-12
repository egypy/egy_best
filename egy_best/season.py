import re
from egy_best.serie import Serie
from egy_best.lib.utils import Utils
from cached_properties import Property as property


class Season(Serie):
    def __init__(self, link, **kwargs):
        super().__init__(link, **kwargs)
        self.season_number = self.find_order('season')

    def get_episodes(self):
        """ get all episodes of a Season """
        container = self.soup.find(class_='movies_small')
        return [Utils.pickup_class(
            link['href'],
            title=link.find(class_='title').text,
            thumbnail=link.img['src'],
        )
            for link in container.find_all('a')]

    def find_order(self, pram):
        return re.search(f'{pram}-(.*)/', self.link).group(1)

    def get_serie_from_season(self):
        elem = self.soup.find(class_='nowrap').find_parent().find_all('td')[1]
        return elem.a['href'], elem.a.text.strip()

    @property
    def serie(self):
        data = self.get_serie_from_season()
        return Serie(link=data[0], title=data[1])

    @property
    def episodes(self):
        return self.get_episodes()
