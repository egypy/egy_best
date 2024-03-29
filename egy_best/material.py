from egy_best.page import Page
from egy_best.actor import Actor
from egy_best.downloader import Downloader
from egy_best.lib.translator import Translator
from egy_best.lib.utils import Utils
from cached_properties import Property as property


class Material(Page):
    """ class to handle movies, series and other Materiales """

    def __init__(self, link, **kwargs):
        super().__init__(link, **kwargs)
        if self.access:
            for name, value in self.get_table_info().items():
                if name not in ['serie']:
                    setattr(self, name, value)

    def __repr__(self):
        return f'{self.__class__.__name__} at : {self.link}'

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
                content.update({Translator.translate(tag.text.strip()): [text.strip()
                                                                         for text in child_text]})
            else:
                content.update({Translator.translate(tag.strip()): child.strip()
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
        container = self.soup.find(class_='rs_scroll pdt pdr')
        content = list()
        for actor in container.find_all(class_='cast_item'):
            name = actor.find_all(class_='td vam')[1].a.text
            content.append(Actor(
                actor.find_all(class_='td vam')[1].a['href'],
                role=Utils.fix_actor_role(
                    name,
                    actor.find_all(class_='td vam')[1].span.text),
                _name=name,
                _image=actor.find_all(class_='td vam')[0].img['src']
            ))
        return content

    def get_download_info(self):
        """ get download informations: qualities availables and a lot of info
        """
        if Translator.translate('404') in self.soup.text:
            return 'No download has found'
        container = self.soup.find(class_='dls_table btns full mgb')
        parents = [Translator.translate(w.text)
                   for w in container.thead.tr.find_all('th')]
        childs = container.tbody.find_all('tr')
        return {i: {parent: elem.a['data-url']
                    if elem.a else elem.text
                    for parent, elem in zip(
            parents,
            child.find_all('td'))
        }
            for i, child in zip(range(len(childs)), childs)}

    def get_source_link(self, quality=None):
        """ get the mp4 download link """
        if str(quality).isnumeric():
            self.download_info[quality]['download'] = self.downloader_handler.get_mp4_link(quality)
            return self.download_info[quality]
        for quality in self.download_info:
            if '/api' in self.download_info[quality]['download']:
                self.download_info[quality]['download'] = self.downloader_handler.get_mp4_link(
                    quality)
        return self.download_info

    def get_thriller(self):
        """ scrape youtube thriller from the website """
        api = self.soup.find(class_='play p api')
        return api['url'] if api else 'Not Found'

    @property
    def thumbnail(self):
        self.get_thumbnail_info()['thumbnail']

    @property
    def rating_percent(self):
        if self.soup.find(class_='cpnt'):
            return self.soup.find(class_='cpnt').text
        return 'Not rated'

    @property
    def downloader_handler(self):
        return Downloader(self.download_info)
