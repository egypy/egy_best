import requests as reeeeeee # reeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
from egy_best.antibot import AntiBot
from egy_best.lib.settings import Settings
from egy_best.lib.utils import Utils
from cached_properties import Property as property
parameters = Settings()

class Downloader:
	def __init__(self, items):
		self.api = parameters.mainsite()
		self.items = items

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

	@property(timeout=3600)
	def egy_token(self):
		return AntiBot('egy_best', True).get_token()

	@property(timeout=3600)
	def vid_stream(self):
		return AntiBot('vid_stream', True).get_token()
