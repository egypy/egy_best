from egy_best.material import Material
from egy_best.lib.translator import Translator
from egy_best.lib.utils import Utils
from cached_properties import Property as property

class Movie(Material):
	""" a movie class to handle movies """
	def __init__(self, link, **kwargs):
		super().__init__(link, **kwargs)
		if self.access:
			self.title = ' '.join(self.get_thumbnail_info()['title'].split()[0:-1:])
			self.year = self.get_thumbnail_info()['title'].split()[-1]

	def __str__(self):
		return f'{self.title} ({self.year})'

	def __repr__(self):
		return str(self)

	def get_similar(self):
		""" get similar movies """
		container = self.soup.find(class_='contents movies_small')

		return [Utils.pickup_class(
				link['href'],
				title=link.find(class_='title').text
			)
			for link in container.find_all('a')]

	@property
	def actors(self):
		return self.get_actors()

	@property
	def download_info(self):
		return self.get_download_info()

	@property
	def story(self):
		""" get story """
		return self.get_story()

	@property
	def thriller(self):
		""" get youtube thriller link if any """
		return self.get_thriller()
