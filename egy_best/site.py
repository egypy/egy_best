import requests
from actor import Actor
from movie import Movie
from serie import Serie
from season import Season
from episode import Episode
from page import Page
from lib.settings import Settings
from lib.utils import Utils
class Site:
	""" a class that hold site functionality : search, login ..."""
	classes = dict(
			movie=Movie,
			actor=Actor,
			series=Serie,
			season=Season,
			episode=Episode,
		)
	my_site = Settings.mainsite()
	search_api = f'{my_site}autoComplete.php'

	@classmethod
	def search(cls, query: str, **kwargs):
		""" a class to search inside the site : movies, series ...
		return instance of class's that blong the the type of result
		"""

		pram = (
		('q', query),
		)
		r = requests.get(cls.search_api, params=pram, **kwargs).json()
		return [f'{cls.my_site}{movie["u"]}' for elem in r
			for movie in r[elem]]
		# todo replace the link by instance generator based on type

	@classmethod
	def pickup_class(cls, link):
		""" return a instance based on the link and config
		"""
		if Settings.AUTO_INIT:
			type = Utils.page_type(link)
			if type in cls.classes:
				return cls.classes[type](link)
			return Page(link)
		return link
