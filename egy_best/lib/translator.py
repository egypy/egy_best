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
		'القصة': 'story',
	}

	@classmethod
	def translate(cls, elem: str, *, type='offline', reverse=False) -> str:
		if type == 'offline':
			return cls.offline_translate(elem, reverse)

	@classmethod
	def offline_translate(cls, elem, reverse):
		if reverse:
			for name, value in cls.data.items():
				if value == elem:
					return name
		if elem in cls.data:
			return cls.data[elem]
		raise TranslateNotFound

# TOOO: add online translate
