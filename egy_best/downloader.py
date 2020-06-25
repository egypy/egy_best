import requests as reeeeeee # reeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
from antibot import AntiBot
from lib.settings import Settings
from lib.utils import Utils
from cached_properties import Property as property

class Downloader:
	def __init__(self, link):
		self.link = link
		self.api = Settings.mainsite()

	def get_mp4_link(self):
		link = f'{self.api.rstrip("/")}{self.link}'
		vid_link = reeeeeee.get(link,
			headers=Settings.headers, cookies=self.egy_token).url
		page = Utils.page_downloader(vid_link, cookies=self.vid_stream)
		return page.find(class_='bigbutton').attrs['href']

	@staticmethod
	def download_file(cls, source, max=512):
		r = requests.get(source, headers=Settings.headers, stream=True)
		content = bytes()
		while True:
			if r:
				yield r.raw.read(max)
			break

	@property(timeout=3600)
	def egy_token(self):
		AntiBot('egy_best', True).get_token()

	@property(timeout=3600)
	def vid_stream(self):
		AntiBot('vid_stream', True).get_token()
