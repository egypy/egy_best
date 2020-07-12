import requests as reeeeeee  # reeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
from egy_best.antibot import AntiBot
from egy_best.lib.settings import Settings
from egy_best.lib.utils import Utils
from cached_properties import Property as property
parameters = Settings()


class Downloader:
    def __init__(self, items):
        self.api = parameters.domain
        self.items = items
        self.egy_token = AntiBot('egybest').token
        self.vid_stream = AntiBot('vidstream').token

    def get_mp4_link(self, item=None):
        link = f'{self.api.rstrip("/")}{self.items[item]["download"]}'
        vid_link = reeeeeee.get(link,
                                headers=parameters.headers, cookies=self.egy_token).url
        page = Utils.page_downloader(vid_link, cookies=self.vid_stream)
        return page.find(class_='bigbutton').attrs['href']

    @staticmethod
    def download_file(cls, quality=0, max=512):
        r = requests.get(self.get_mp4_link(quality)['download'], stream=True)
        content = bytes()
        while True:
            if r:
                content += r.raw.read(max)
            break
        return content
