import time
import pickle
import requests
from egy_best.lib.utils import Utils
from egy_best.lib.settings import Settings
from threading import Thread
from selenium import webdriver
from cached_properties import Property as property
from webdriver_manager.chrome import ChromeDriverManager

para = Settings()


class AntiBot:
    def __init__(self, elem=None):
        self.elem = para.egybest if 'egy' in elem else para.vidstream

    def _bypass(self):
        self.browser.get(f'{self.elem["domain"]}{self.elem["bypass_path"]}')
        self.browser.find_element_by_class_name(
            self.elem['bypass_class']).click()
        time.sleep(3)

    @property
    def browser(self):
        return webdriver.Chrome(ChromeDriverManager().install(),
                                options=para.options)

    def get_cookies(self):
        self._bypass()
        token = {item['name']: item['value']
                 for item in self.browser.get_cookies()}
        para._update_token(
            'vidstream' if 'vidstream' in self.elem['domain'] else 'egybest',
            pickle.dumps(token).hex())
        self.browser.quit()
        para.load_settings()
        return token

    def get_token(self):
        old_token = self.elem['storage']
        if old_token:
            old_token = pickle.loads(bytes().fromhex(old_token))
            if self._test_token(old_token):
                return old_token
        return self.get_cookies()

    def _test_token(self, token):
        r = requests.get(self.test_path, headers=para.headers, cookies=token)
        if self.elem['test_subject'] == 'location':
            return self.elem['test_success'] in r.url
        elif self.elem['test_subject'] == 'http':
            return r.status_code == self.elem['test_success']
        elif self.elem['test_subject'] == 'content':
            return self.elem['test_success'] in r.text

    @property
    def test_path(self):
        page = '{}{}'.format(self.elem['domain'], self.elem['test_path'])
        if 'vidstream' in self.elem['domain']:
            return page
        link = Utils.page_downloader(page).find(
            class_='nop btn g dl _open_window')['data-url']
        return f'{self.elem["domain"]}{link}'

    @property(timeout=3600)
    def token(self):
        return self.get_token()
