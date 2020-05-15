import requests
from bs4 import BeautifulSoup
from settings import Settings

class Utils:
	""" class that hold some useful utils methods"""
	@classmethod
	def page_downloader(cls, link):
		""" download the page and return BeautifulSoup instance """
		while True:
			r = requests.get(link, headers=Settings.headers,
				proxies=Settings.proxy)
			if r.status_code == 200:
				return BeautifulSoup(r.text, 'lxml')
			cls.page_downloader(link)
