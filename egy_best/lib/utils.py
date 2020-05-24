import requests
from bs4 import BeautifulSoup
from .settings import Settings
# i had to sell my soul to devil due relative imports
class Utils:
	""" class that hold some useful utils methods"""
	classes = dict(
			movie='Movie',
			actor='Actor',
			series='Serie',
			season='Season',
			episode='Episode',
		)
	@classmethod
	def page_downloader(cls, link):
		""" download the page and return BeautifulSoup instance """
		while True:
			r = requests.get(link, headers=Settings.headers,
				proxies=Settings.proxy)
			if r.status_code == 200:
				return BeautifulSoup(r.text, 'lxml')
			cls.page_downloader(link)

	@classmethod
	def page_type(cls, link):
		""" detect page type based on the link """
		r = requests.utils.urlparse(link)
		if r.path.count('/') and not r.path == '/':
			return r.path.split('/')[1]
		return 'home'

	@classmethod
	def magic_import(cls, name, link):
		tampl = '{}("{}")'
		rel = cls.classes[name]
		code = f'from {rel.lower()} import {rel}'
		exec(code)
		return eval(tampl.format(rel, link))

	@classmethod
	def pickup_class(cls, link):
		""" return a instance based on the link and config
		"""
		holy_marry = ['actor', 'season']
		type = Utils.page_type(link)
		if Settings.AUTO_INIT:
			if type in cls.classes:
				return cls.magic_import(type, link)
			return cls.magic_import('page', link)
		return link
