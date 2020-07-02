import requests
from egy_best.lib.settings import Settings
from egy_best.lib.utils import Utils
from bs4 import BeautifulSoup

class Site:
	""" a class that hold site functionality : search, login ..."""
	my_site = Settings().mainsite()
	search_api = f'{my_site}autoComplete.php'
	filter_api = '%s{material}/{options}?output_format=json&page={page}' % my_site

	@classmethod
	def search(cls, query: str, access=True, **kwargs) -> list or None:
		""" a class to search inside the site : movies, series ...
		return instance of class's that blong the the type of result
		"""
		tamplate = '%s{}' % cls.my_site
		pram = (
			('q', query),
		)
		r = requests.get(cls.search_api, params=pram, **kwargs).json()
		if r:
			return [Utils.pickup_class(
						link=tamplate.format(movie['u']),
						title=movie['t'],
						)
				for elem in r
					for movie in r[elem]]
		return None

	@classmethod
	def filter(cls, material: str, options: list, max: int = 5) -> list:
		""" filter movies based on options
		options supported values:
		filter : latest, top, popular
		year : year if under 2000 add 's' example -> 2012, 1950s
			bad usage ->  2012s, 1951
		language: language example -> arabic, english
		country : iso code of the country example -> us, ma
		type: type -> example -> action, documentary
		content rating : example -> [PG-13] +13 , unrated,
		quality: example -> bluray, hdrip
		precision : example -> 1080p, 720p
		example of filtering - > Site.filter('tv', ['top', 'us', '1080p'])
		1) order doesn't matter
		2) pass options as a list
		3) options are optinal you don't have to pass all of them
		"""
		material = material.lower()
		supported = ['tv', 'movies', 'masrahiyat']
		if material not in supported:
			print(f'Supported filters are {", ".join(supported)}')
			return None
		text = ''
		for page in range(1, max+1):
			query = cls.filter_api.format(
					material=material,
					options='-'.join(options),
					page=page)
			r = requests.get(query).json()
			text += r['html']

		soup = BeautifulSoup(text, 'lxml')
		return [
			Utils.pickup_class(link['href'],
			title=link.find(class_='title').text)
				for link in soup.find_all(class_='movie')
			]
