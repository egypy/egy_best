from lib.utils import Utils
class Material:
	""" class to handle movies, series and other Materiales """
	def __init__(self, link):
		self.link = link
		self.soup = Utils.page_downloader(link)
		self.thumbnail = self.thumbnail_scrape()['thumbnail']
		self.language = None
		self.classing = None
		self.type = None
		self.rating = None
		self.rating_percent = None

	def thumbnail_scrape(self) -> dict:
		""" scrape thumbnail for useful informations """
		content = dict()
		r = self.soup.find(class_='movie_img')
		if r.span:
			content.update(dict(
				quality_type=r.span.text,
				)
			)

		img = r.find('a').find('img')
		content.update(
			dict(thumbnail=img.attrs['src'],
				title=img.attrs['alt'],
			)
		)
		return content
