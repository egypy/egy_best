import os
import pickle
import requests
from egy_best.lib.exceptions import BotDetectedException
from selenium.webdriver.chrome.options import Options

# todo make this better a sat
class Settings:

	def __init__(self):
		fpath = os.path.realpath(__file__)
		self.path = '/'.join(fpath.split('\\' if os.name == "nt" else '/')[:-1])
		self.settings_path = f'{self.path}/database/settings.data'
		self.load_settings()

	def _read_settings(self):
		with open(self.settings_path, 'r') as fobj:
			return pickle.loads(bytes().fromhex(fobj.read()))

	def _save_settings(self, data):
		with open(self.settings_path, 'w+') as fobj:
			fobj.write(pickle.dumps(data).hex())

	def load_settings(self):
		for name, value in self._read_settings().items():
			setattr(self, name, value)
		options = Options()
		options.add_experimental_option('prefs', self.prefs)
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		options.add_argument("disable-infobars")
		options.add_argument("--disable-extensions")
		options.add_argument("--headless")
		options.add_argument('log-level=3')
		self.options = options

	def edit_settings(self, item, value):
		old = self._read_settings()
		old[item] = value
		self._save_settings(old)

	def mainsite(self) -> str:
		""" return a website that can be used to browser movies,
		or raise Exception if the bot detcted or due the geolocation
		restriction
		"""
		if not self.DETECT_MAINSITE:
			return 'https://room.egybest.name/'
		r = requests.get(self.site, headers=self.headers, proxies=self.proxy)
		if 'egy' in r.url:
			return r.url
		raise BotDetectedException
