import re
from serie import Serie
from lib.utils import Utils

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
					thumbnail_image=link.img['src'],
				)
		 	for link in container.find_all('a')]

	def find_order(self, pram):
		return  re.search(f'{pram}-(.*)/', self.link).group(1)

	def get_serie_from_season(self):
		elem = self.soup.find(class_='nowrap').find_parent().find_all('td')[1]
		return elem.a['href'], elem.a.text.strip()

	@property
	def serie(self):
		if not hasattr(self, '_serie'):
			data = self.get_serie_from_season()
			setattr(self, '_serie', Serie(
					link=data[0],
					title=data[1]
					),
				)
		return self._serie

	@property
	def episodes(self):
		return self.get_episodes()
