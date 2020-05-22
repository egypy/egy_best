from .exceptions import TranslateNotFound
class Translator:
	""" simple translate class to convert a word from a lang to en """

	data = {
		'اللغة': 'language',
		'البلد': 'country',
		'التصنيف' : 'category',
		'النوع': 'type',
		'المدة': 'duration',
		'الجودة': 'quality',
		'الترجمة': 'traduction',
		'التقييم': 'rating',
		'المسلسل': 'serie',
		'تقييم المسلسل': 'serie_rating',
	}

	@classmethod
	def translate(cls, elem: str, *, type='offline') -> str:
		if type == 'offline':
			return cls.offline_translate(elem)

	@classmethod
	def offline_translate(cls, elem):
		if elem in cls.data:
			return cls.data[elem]
		raise TranslateNotFound

# TOOO: add online translate
