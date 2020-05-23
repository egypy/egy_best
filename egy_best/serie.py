from material import Material
class Serie(Material):
	""" class for Series on egy best """
	def __init__(self, link):
		super().__init__(link)
		self.name = ' '.join(self.get_thumbnail_info()['title'].split()[0:-1:])
		self.year = self.get_thumbnail_info()['title'].split()[-1]
		self.story = self.get_story()
		self.thriller = self.get_thriller()
		self.actors = self.get_actors()
		self.seasons = self.get_seasons()

	def get_seasons(self):
		""" return all seasons of a serie """
		container = self.soup.find(class_='contents movies_small')
		return [link['href']for link in container.find_all('a')]
