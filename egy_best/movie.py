from material import Material
from lib.translator import Translator
from lib.utils import Utils

class Movie(Material):
	""" a movie class to handle movies """
	def __init__(self, link, **kwargs):
		super().__init__(link, **kwargs)
		if self.access:
			self.title = ' '.join(self.get_thumbnail_info()['title'].split()[0:-1:])
			self.year = self.get_thumbnail_info()['title'].split()[-1]
			self.story = self.get_story()
			self.thriller = self.get_thriller()

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
		if not hasattr(self, '_download_info'):
			setattr(self, '_download_info', self.get_download_info())
		return getattr(self, '_download_info')

	@download_info.setter
	def download_info(self, val):
		if val:
			setattr(self, '_download_info', val)

	@property
	def story(self):
		return self.get_story()
