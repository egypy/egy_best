from material import Material
from lib.utils import Utils

class Serie(Material):
	""" class for Series on egy best """
	def __init__(self, link, **kwargs):
		super().__init__(link, **kwargs)
		if self.access:
			self.title = ' '.join(self.get_thumbnail_info()['title'].split()[0:-1:])
			self.year = self.get_thumbnail_info()['title'].split()[-1]
			self.story = self.get_story()
			self.thriller = self.get_thriller()

	def __repr__(self):
		return f'{self.title} ({self.year})'

	def get_seasons(self):
		""" return all seasons of a serie """
		container = self.soup.find(class_='contents movies_small')
		return [Utils.pickup_class(
				link=link['href'],
				title=link.find(class_='title').text,
				thumbnail_image=link.img['src']
			)
			for link in container.find_all('a')]

	@property
	def actors(self) -> list:
		""" return actors in the series """
		return self.get_actors()

	@property
	def seasons(self) -> list:
		""" return seasons that are in the serie """
		return self.get_seasons()
