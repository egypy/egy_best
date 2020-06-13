import requests
from lib.settings import Settings
from lib.utils import Utils

class Site:
	""" a class that hold site functionality : search, login ..."""
	my_site = Settings.mainsite()
	search_api = f'{my_site}autoComplete.php'

	@classmethod
	def search(cls, query: str, **kwargs):
		""" a class to search inside the site : movies, series ...
		return instance of class's that blong the the type of result
		"""
		tamplate = f'{cls.my_site}' + '{}'
		pram = (
			('q', query),
		)
		r = requests.get(cls.search_api, params=pram, **kwargs).json()
		return [Utils.pickup_class(tamplate.format(movie["u"]), True)
			for elem in r
				for movie in r[elem]]
