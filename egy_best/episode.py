import re
from serie import Serie
from season import Season
from material import Material
from lib.utils import Utils
class Episode(Material):
	def __init__(self, link, **kwargs):
		self.link = link
		super().__init__(link, **kwargs)
		if self.access:
			for name, value in self.season.serie.__dict__.items():
				setattr(self, name, value)
			self.soup = Utils.page_downloader(link)


	def find_order(self, pram):
		return  re.search(f'{pram}-(.*)/', self.link).group(1)

	def get_serie_from_episode(self):
		order = self.find_order('ep')
		r = self.link.replace(f'-ep-{order}', '').replace('episode', 'season')
		return r

	@property
	def season(self):
		if not hasattr(self, '_season'):
			self._season = Season(link=self.get_serie_from_episode())
		return self._season

	@property
	def download_info(self):
		if not hasattr(self, '_download_info'):
			setattr(self, '_download_info', self.get_download_info())
		return self._download_info

	@property
	def episode_number(self):
		if not hasattr(self, '_episode_number'):
			setattr(self, '_episode_number', self.find_order('ep'))
		return self._episode_number
