from egy_best.material import Material
from egy_best.lib.utils import Utils
from cached_properties import Property as property


class Serie(Material):
    """ class for Series on egy best """

    def __init__(self, link, **kwargs):
        super().__init__(link, **kwargs)
        if self.access:
            self.title = ' '.join(self.get_thumbnail_info()['title'].split()[0:-1:])
            self.year = self.get_thumbnail_info()['title'].split()[-1]

    def __repr__(self):
        return f'{self.title} ({self.year})'

    def get_seasons(self):
        """ return all seasons of a serie """
        container = self.soup.find(class_='contents movies_small')
        return [Utils.pickup_class(
            link=link['href'],
            title=link.find(class_='title').text,
            thumbnail=link.img['src']
        )
            for link in container.find_all('a')]

    @property
    def actors(self) -> list:
        """ return actors in the series """
        return self.get_actors()

    @property
    def seasons(self) -> list:
        """ return seasons that are in the serie """
        return self.get_seasons()

    @property
    def thriller(self):
        """ get youtube thriller link if any """
        return self.get_thriller()

    @property
    def story(self):
        """ get story """
        return self.get_story()
