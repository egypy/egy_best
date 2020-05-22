from page import Page
from lib.translator import Translator
class Material(Page):
	""" class to handle movies, series and other Materiales """
	def __init__(self, link):
		super().__init__(link)
		self.thumbnail = self.get_thumbnail_info()['thumbnail']
		self.rating_percent = self.soup.find(class_='cpnt').text
		for name, value in self.get_table_info().items():
			setattr(self, name, value)

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
				content.update({Translator.translate(tag.text.strip()):[text.strip()
					for text in child_text]})
			else:
				content.update({Translator.translate(tag.strip()):child.strip()
					for tag, child in zip(tag_text, child_text)})
		return content

	def get_story(self):
		"""find story, only for movie and serie classes """
		r = self.soup.find(
			text=Translator.translate('story', reverse=True)
			).findNext('div')
		return r.text.replace(r.strong.text, '') if r.strong else r.text

	def get_actors(self):
		""" get actors and thire info from a material page """
		content = dict()
		container = self.soup.find(class_='rs_scroll pdt pdr')
		i = int()
		for actor in container.find_all(class_='cast_item'):
			i += 1
			for elem in actor.find_all(class_='td vam'):
				if elem.a.img:
					content.update({
					i:dict(
						name=elem.img['alt'],
						image=elem.img['src'],
						)
					})
				else:
					role = elem.span
					content[i].update(dict(
						role=role.text.replace('...', ''),
						appearance=role['title'].split('  ')[-1]
							if self.page_type in ['series', 'season'] else None
						)
					)
		return content

	def get_download_info(self):
		""" get download informations: qualities availables and a lot of info
		"""
		container = self.soup.find(class_='dls_table btns full mgb')
		parents = [Translator.translate(w.text)
			for w in container.thead.tr.find_all('th')]
		childs = container.tbody.find_all('tr')
		return {i:{parent: elem.a['data-url']
		if elem.a else elem.text
			for parent, elem in zip(
				parents,
				child.find_all('td'))
				}
			for i , child in zip(range(len(childs)), childs)}

	def get_thriller(self):
		""" scrape youtube thriller from the website """
		return self.soup.find(class_='play p api')['url']
