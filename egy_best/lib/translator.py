from egy_best.lib.exceptions import TranslateNotFound

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
	def translate(cls, elem: str, *, type='offline', reverse=False) -> str:
		""" translate a word from ar to en or reverse """
		if type == 'offline':
			return cls.offline_translate(elem, reverse)

	@classmethod
	def offline_translate(cls, elem, reverse):
		""" return translation based on a local dict """
		if reverse:
			for name, value in cls.data.items():
				if value == elem:
					return name
		if elem in cls.data:
			return cls.data[elem]
		raise TranslateNotFound

# TOOO: add online translate
