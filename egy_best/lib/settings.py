import os
import json
import requests
from egy_best.lib.exceptions import BotDetectedException
from selenium.webdriver.chrome.options import Options
from cached_properties import Property as property


class Settings:
    def __init__(self):
        fpath = os.path.realpath(__file__)
        self.path = '/'.join(fpath.split('\\' if os.name == "nt" else '/')[:-1])
        self.settings_path = f'{self.path}/database/settings.json'
        self.options = Options()
        self.load_settings()

    def load_settings(self):
        for item in self.data:
            if item != 'selenium_settings':
                for name, value in self.data[item].items():
                    if item == 'website_settings':
                        for sname, svalue in self.data[item].items():
                            if not self.data[item][sname]['domain']:
                                if sname == 'egybest':
                                    svalue['domain'] = self.domain
                            setattr(self, sname, svalue)
                    else:
                        setattr(self, name, value)
            else:  # item == 'selenium_settings':
                for setting in self.data[item]:
                    if setting != 'arguments':
                        self.options.add_experimental_option(
                            setting, self.data[item][setting])
                    else:
                        for arg in self.data[item][setting]:
                            self.options.add_argument(arg)

    def _update_token(self, site, value):
        self.data['website_settings'][site].update({'storage': value})
        with open(self.settings_path, 'w+') as fobj:
            return fobj.write(json.dumps(self.data))

    @property(hits=10)
    def data(self):
        with open(self.settings_path, 'r') as fobj:
            return json.loads(fobj.read())

    @property(timeout=3600)
    def domain(self) -> str:
        if not self.detect_netloc:
            return 'https://room.egybest.name'
        r = requests.get('https://egy.best', headers=self.headers,
                         proxies=self.proxy)
        if 'egy' in r.url:
            return r.url
        raise BotDetectedException
