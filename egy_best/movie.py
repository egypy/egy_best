from material import Material
from lib.translator import Translator

class Movie(Material):
	""" a movie class to handle movies """
	def __init__(self, link):
		super().__init__(link)
		self.name = ' '.join(self.get_thumbnail_info()['title'].split()[0:-1:])
		self.year = self.get_thumbnail_info()['title'].split()[-1]
		self.story = self.get_story()
		self.actors = self.get_actors()
		self.thriller = self.get_thriller()
		self.download_info = self.get_download_info()

	def __str__(self):
		return f'{self.name} ({self.year})'

	def __repr__(self):
		return str(self)

	def get_similar(self):
		""" get similar movies """
		container = self.soup.find(class_='contents movies_small')
		return [Movie(link['href']) for link in container.find_all('a')]
