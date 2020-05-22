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

m = Movie('https://room.egybest.name/movie/the-dark-knight-2008/')
r = m.get_thriller()
print(r)
