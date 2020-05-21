from lib.utils import Utils
class Page:
	""" a class to handle html pages on the site """
	def __init__(self, link):
		self.link = link
		self.soup = Utils.page_downloader(link)
		self.page_type = Utils.page_type(link)
