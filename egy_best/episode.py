import re
from serie import Serie
from season import Season
from material import Material
from lib.utils import Utils

class Episode(Material):
	def __init__(self, link):
		self.link = link
		self.soup = Utils.page_downloader(link)
		self.season = Season(self.get_serie_from_episode())
		self.download_info = self.get_download_info()
		self.episode_number = self.find_order('ep')

		for name, value in self.season.serie.__dict__.items():
			if name != 'soup':
				setattr(self, name, value)

	def find_order(self, pram):
		return  re.search(f'{pram}-(.*)/', self.link).group(1)

	def get_serie_from_episode(self):
		order = self.find_order('ep')
		return self.link.replace(f'-ep-{order}', '').replace('episode', 'season')
