from cached_properties import Property as property
from lib.utils import Utils
from lib.settings import Settings

class Actor:
	def __init__(self, link, **kwargs):
		self.link = link

		for name, value in kwargs.items():
			setattr(self, name, value)

	def __repr__(self):
		return self.name

	@property
	def soup(self):
		if not hasattr(self, '_soup'):
			self._soup = Utils.page_downloader(self.link).find(id='mainLoad')
		return self._soup


	def scrape_image(self):
		r = self.soup.find(class_='inline vam').a.img
		return dict(image=r['src'], name=r['alt'])

	def scrape_movies(self, max=1):
		content = dict(new=list(), top=list(), popular=list(), old=list())
		for categorie in content.keys():
			for id in range(1, max+1):
				soup = Utils.page_downloader(f'{self.link}{categorie}?page={id}')
				con = soup.find(class_='movies movies_small')
				content[categorie].extend([Utils.pickup_class(movie['href'])
								for movie in con.find_all(class_='movie')])
		return content

	@property
	def total_films(self):
		r = self.soup.find(text=self.name).find_parent().find_parent()
		return ''.join([elem for elem in r.text.replace(self.name, '').split()
						if elem.isdigit()])
	@property
	def movies(self):
		max = int(self.total_films[1]) if int(self.total_films) > 20 else 1
		return self.scrape_movies(max)

	@property
	def image(self):
		return self.scrape_image()['image']

	@property
	def name(self):
		if Settings.AUTO_INIT:
			return self.scrape_image()['name']
		return ' '.join(Utils.url_to_name(self.link)).title()
