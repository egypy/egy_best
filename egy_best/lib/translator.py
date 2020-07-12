"""module that handles translation.

Modules
-------
    Translator
"""
from egy_best.lib.exceptions import TranslateNotFound


class Translator:
    """Simple translate class to convert a word from ar lang to en.

    ...

    Attributes
    ----------
    data: dict
        hold local data

    Methods
    -------
    translate('', method='offline', reverse=False):
        choose the right method based of method parameter and call it with the
        string and reverse argements

    offline_translate('', reverse=False):
        return a match from the local data dict
    """

    data = {
        'اللغة': 'language',
        'البلد': 'country',
        'التصنيف': 'category',
        'النوع': 'type',
        'المدة': 'duration',
        'الجودة': 'quality',
        'الترجمة': 'traduction',
        'التقييم': 'rating',
        'المسلسل': 'serie',
        'تقييم المسلسل': 'serie_rating',
        'القصة': 'story',
        'الدقة': 'accuracy',
        'الحجم': 'size',
        'التحميل': 'download',
        '404': 'هذا الفيلم غير متاح حالياً',
        'الأفلام الأكثر مشاهدة': 'most_viewd',
        'أفلام جديدة': 'new_movies',
        'مسلسلات جديدة': 'new_series',
        'أفلام جديدة BluRay': 'new_blueray_movies',
        'أحدث الاضافات': 'recently_added',
        'أفلام كوميدية': 'comedies_movies',
        'أفلام شبابية': 'teen_movies',
        'أفلام سوبر هيرو': 'super_hero_movies',
        'أفلام انمي و كرتون': 'anime',
        'أفلام رومانسية': 'romantic_movies',
        'أفلام دراما': 'darama_movies',
        'أفلام رعب': 'heror_movies',
        'أفلام وثائقية': 'documentaries',
        'أفلام عن نهاية العالم': 'movies_about_the_end',
        'أفلام عربية': 'arabic_movies',

    }

    @classmethod
    def translate(cls, string: str, *, method: str = 'offline',
                  reverse: bool = False) -> str:
        """Translate a word from ar to en or reverse.

        Parameters
        ----------
        string: str
            string that will be translated

        Optional arguments
        ------------------
        method: str
            method that will be used offline/online (default 'offline')
        reverse: bool:
            reverse translation en to ar (default False)

        """
        if method == 'offline':
            return cls.offline_translate(string, reverse)

    @classmethod
    def offline_translate(cls, string: str, reverse: bool) -> str:
        """Return translation based on a local dict.

        Parameters
        ----------
        string: str
            string that will be translated
        reverse: bool
            reverse translation en to ar (default False)
        Returns
        -------
            data [string]: value of key string
        """
        if reverse:
            for name, value in cls.data.items():
                if value == string:
                    return name
        if string in cls.data:
            return cls.data[string]
        raise TranslateNotFound

# TOOO: add online translate
