from egy_best.lib.utils import Utils
from egy_best.lib.settings import Settings
from cached_properties import Property as property

class Page:
	""" a class to handle html pages on the site """
	def __init__(self, link, **kwargs):
		self.link = link
		self.page_type = Utils.page_type(link)
		self.access = Settings().AUTO_INIT

		if not self.access:
			if 'title' in kwargs:
				self.title, self.year = Utils.title_parser(kwargs['title'])
				if self.year is None:
					year_url =  Utils.url_to_name(link)[1]
					self.year = year_url if year_url.isnumeric() else None
			else:
				self.title, self.year = Utils.url_to_name(link)

			for name, value in kwargs.items():
				if name != 'title':
					setattr(self, name, value)

	@property
	def soup(self):
		return Utils.page_downloader(self.link)
