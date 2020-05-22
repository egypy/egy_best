import requests
from bs4 import BeautifulSoup
from .settings import Settings
# i had to sell my soul to devil due relative imports
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

	@classmethod
	def page_type(cls, link):
		""" detect page type based on the link """
		r = requests.utils.urlparse(link)
		if r.path.count('/') and not r.path == '/':
			return r.path.split('/')[1]
		return 'home'
