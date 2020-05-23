import re
from serie import Serie

class Season(Serie):
	def __init__(self, link):
		super().__init__(link)
		self.episodes = self.get_episodes()
		self.season_number = self.find_order('season')
		self.serie = Serie(self.get_serie_from_season())

	def get_episodes(self):
		""" get all episodes of a Season """
		container = self.soup.find(class_='movies_small')
		return [link['href'] for link in container.find_all('a')]

	def find_order(self, pram):
		return  re.search(f'{pram}-(.*)/', self.link).group(1)

	def get_serie_from_season(self):
		return self.soup.find(text=self.serie).find_parent()['href']
