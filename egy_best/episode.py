import re
from egy_best.serie import Serie
from egy_best.season import Season
from egy_best.material import Material
from egy_best.lib.utils import Utils
from cached_properties import Property as property


class Episode(Material):
    def __init__(self, link, **kwargs):
        self.link = link
        super().__init__(link, **kwargs)

    def __repr__(self):
        return f'{self.title} Episode number : {self.episode_number}'

    def find_order(self, pram):
        return re.search(f'{pram}-(.*)/', self.link).group(1)

    def get_serie_from_episode(self):
        order = self.find_order('ep')
        r = self.link.replace(f'-ep-{order}', '').replace('episode', 'season')
        return r

    @property
    def season(self):
        return Season(link=self.get_serie_from_episode())

    @property
    def download_info(self):
        return self.get_download_info()

    @property
    def episode_number(self):
        return self.find_order('ep')

    @property
    def soup(self):
        return Utils.page_downloader(self.link)

    @property
    def year(self):
        return self.season.serie.year
