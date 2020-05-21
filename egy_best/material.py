from page import Page
class Material(Page):
	""" class to handle movies, series and other Materiales """
	def __init__(self, link):
		super().__init__(link)
		self.thumbnail = self.thumbnail_scrape()['thumbnail']
		self.language = None
		self.classing = None
		self.type = None
		self.rating = None
		self.rating_percent = None

	def get_thumbnail_info(self) -> dict:
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

	def get_table_info(self):
		""" scrape movie table for useful informations """
		childs = self.soup.find(class_='movieTable full').find_all('td')
		content = dict()
		for tag, child in zip(childs[1::2], childs[2::2]):
			tag_text = tag.text.split('•')
			child_text = child.text.split('•')
			if len(tag_text) != len(child_text):
				content.update({tag.text.strip():[text.strip()
					for text in child_text]})
			else:
				content.update({tag.strip():child.strip()
					for tag, child in zip(tag_text, child_text)})
		return content
