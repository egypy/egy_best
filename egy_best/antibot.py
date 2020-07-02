import time
import pickle
import requests
from egy_best.lib.utils import Utils
from egy_best.lib.settings import Settings
from threading import Thread
from selenium import webdriver
from cached_properties import Property as property
# todo clean up the code
# better class and tests

parameters = Settings()
class AntiBot:
	database = f'{parameters.path}/database/'
	egy_site = parameters.mainsite()

	data = {
		'egy_best': {
			'site': egy_site,
			'filename': f'{database}egy_best.data',
			'bypass': {
					'name': 'class name',
					'value':'logo.vam',
				},
		},
		'vid_stream': {
			'site': 'https://vidstream.online/f/mgnA4lAq7g/',
			'filename': f'{database}vid_stream.data',
			'bypass':{
				'name': 'class name',
				'value': 'bigbutton._reload'
			},
		}
	}


	def __init__(self, elem, thread=False):
		self.content = self.data[elem]
		if thread:
			t1 = Thread(target=self._auto_update)
			t1.setDaemon(True)
			t1.start()

	def init_browser(self):
		return webdriver.Chrome(f'{parameters.path}/chromedriver.exe',
			options=parameters.options)

	def bypass(self):
		elem = self.content['bypass']
		self.browser.get(self.content['site'])
		self.browser.find_element(elem['name'], elem['value']).click()
		time.sleep(3)

	def get_token(self, is_threaded=False):
		old_token = self.load_data(self.content['filename'])
		if old_token:
			if self.test_token(old_token):
				return old_token
		while True:
			if is_threaded:
				self.init_browser()
			else:
				t = Thread(target=self.init_browser)
				t.setDaemon(True)
				t.start()
				while True:
					if not t.is_alive():
						break
			self.bypass()
			token = self.make_cookie(self.browser)
			if self.test_token(token):
				self.save_data(self.content['filename'], token)
				break
		self.browser.quit()
		return token

	def save_data(self, filename, data):
		with open(filename, 'wb') as fobj:
			fobj.write(pickle.dumps(data))

	def load_data(self, filename):
		try:
			with open(filename, 'rb') as fobj:
				data = fobj.read()
				if data:
					return pickle.loads(data)
				return False
		except FileNotFoundError:
			return False

	def _auto_update(self):
		while True:
			time.sleep(120)
			token = self.get_token(is_threaded=True)

	@staticmethod
	def make_cookie(browser):
		return {item['name']:item['value'] for item in browser.get_cookies()}

	@staticmethod
	def _get_test(vid=False):
		if vid:
			return 'https://vidstream.online/f/mgnA4lAq7g/'

		netloc = parameters.mainsite()
		r = Utils.page_downloader(f'{netloc}movie/pink-floyd-the-wall-1982/')
		link = r.find(class_='nop btn g dl _open_window')['data-url']
		return f"{netloc.strip('/')}{link}"

	def test_token(self, cookies):
		if 'egybest' in self.content['site']:
			test = self._get_test()
			r = requests.get(test, headers=parameters.headers, cookies=cookies)
			if 'vidstream' in r.url:
				return r.url
			return False
		test = self._get_test(True)
		r = requests.get(test, headers=parameters.headers, cookies=cookies)
		if '.mp4" class="bigbutton"' in r.text:
			return True
		return False

	@property
	def browser(self):
		return self.init_browser()
