import requests
from .exceptions import BotDetectedException
from selenium.webdriver.chrome.options import Options

# todo make this better a sat
class Settings:
	""" main settings stored in this class """
	site = 'https://egy.best'
	AUTO_INIT = False # better false for speed
	DETECT_MAINSITE = False # speed u can set it to true if you want
	headers =  {
	    'dnt': '1',
	    'upgrade-insecure-requests': '1',
    	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	    'sec-fetch-site': 'none',
	    'sec-fetch-mode': 'navigate',
		'sec-fetch-user': '?1',
	    'sec-fetch-dest': 'document',
	    'accept-language': 'en-US,en;q=0.9',
	}
	options = Options()
	prefs = {'profile.default_content_setting_values': {'images': 2,
                            'plugins': 2, 'popups': 2, 'geolocation': 2,
                            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2,
                            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2,
                            'durable_storage': 2}}
	options.add_experimental_option('prefs', prefs)
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	options.add_argument("disable-infobars")
	options.add_argument("--disable-extensions")
	options.add_argument("--headless")
	options.add_argument('log-level=3')

	proxy = None
	classes = dict(
			movie='Movie',
			actor='Actor',
			series='Serie',
			season='Season',
			episode='Episode',
		)
	@classmethod
	def mainsite(cls) -> str:
		""" return a website that can be used to browser movies,
		or raise Exception if the bot detcted or due the geolocation
		restriction
		"""
		if not cls.DETECT_MAINSITE:
			return 'https://room.egybest.name/'
		r = requests.get(cls.site, headers=cls.headers, proxies=cls.proxy)
		if 'egy' in r.url:
			return r.url
		raise BotDetectedException
