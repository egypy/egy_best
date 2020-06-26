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
	def page_downloader(cls, link, **kwargs):
		""" download the page and return BeautifulSoup instance """
		if not link.startswith('http'):
			link = f'{Settings.mainsite().strip("/")}{link}'
		while True:
			r = requests.get(link, headers=Settings.headers,
				proxies=Settings.proxy, **kwargs)
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
	def magic_import(cls, name, link, **kwargs):
		""" import classes to avoid circular import Exception """
		tampl = '{}("{}", **kwargs)'
		rel = cls.classes[name]
		return getattr(__import__(rel.lower()), rel)(link, **kwargs)

	@classmethod
	def pickup_class(cls, link, **kwargs):
		""" return a instance based on the link and config
		"""
		type = Utils.page_type(link)
		if type in cls.classes:
			return cls.magic_import(type, link, **kwargs)
		return cls.magic_import('page', link, **kwargs)

	@classmethod
	def make_link(cls, domain=Settings.mainsite(), link=None):
		""" fix errors on the link and append main netloc """
		tampl = '{domain}{path}?ref=home{q}'
		r = requests.utils.urlparse(link if link else '')
		return tampl.format(
			domain=domain,
			path=r.path.strip('/')
				if r.path.startswith('/') else r.path,
			q=r.query.replace('?', '&'),
			)

	@staticmethod
	def fix_actor_role(actor, role):
		if 'as' in role:
			role = role.replace(actor, '').strip()
		if 'المخرج' in role:
			role = 'Director'
		return role

	@staticmethod
	def url_to_name(link: str) -> tuple:
		""" return title and year from url """
		r = requests.utils.urlparse(link).path
		bad = r.split('/')[1]
		year = r.split('-')[-1].strip('/')
		title =''.join([ch if ch not in ['-', '/'] else ' '
			for ch in r.replace(year, '').replace(bad, '')]).strip()
		return title.title(), year

	@staticmethod
	def title_parser(title: str) -> tuple:
		try:
			year = title[title.index('(') + 1:title.index(')')]
			if not year.isnumeric():
				raise ValueError
		except ValueError:
			return title, None
		return title.replace(f'({year})', '').strip(), year
