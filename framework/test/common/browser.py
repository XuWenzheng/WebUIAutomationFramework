import time
import os
import platform
from selenium import webdriver
from utils.config import DRIVER_PATH, REPORT_PATH
from utils.config import Config, DRIVER_PATH, DATA_PATH, REPORT_PATH  # 引入配置


# 根据传入的参数选择浏览器的driver去打开对应的浏览器

# 可根据需要自行扩展
CHROMEDRIVER_PATH = os.path.join(DRIVER_PATH , 'chromedriver.exe')
IEDRIVER_PATH = os.path.join(DRIVER_PATH , 'IEDriverServer.exe')
PHANTOMJSDRIVER_PATH = os.path.join(DRIVER_PATH + 'phantomjs.exe')
EDGEDRIVER_PATH = os.path.join(DRIVER_PATH + 'edgedriver.exe')

TYPES = {'firefox': webdriver.Firefox, 'chrome': webdriver.Chrome, 'ie': webdriver.Ie, 'phantomjs': webdriver.PhantomJS, 'headless': webdriver.Chrome, 'edge': webdriver.Edge}
EXECUTABLE_PATH = {'firefox': 'wires', 'chrome': CHROMEDRIVER_PATH, 'ie': IEDRIVER_PATH, 'phantomjs': PHANTOMJSDRIVER_PATH, 'edge':EDGEDRIVER_PATH}


class UnSupportBrowserTypeError(Exception):
    pass


class Browser(object):
    def __init__(self):
        self._type = Config().get('browser').lower()
        if self._type in TYPES:
            self.browser = TYPES[self._type]
        else:
            raise UnSupportBrowserTypeError('仅支持%s!' % ', '.join(TYPES.keys()))
        self.driver = None

    def get(self, url, maximize_window=True, implicitly_wait=30):
        if self._type == 'headless':
            option = webdriver.ChromeOptions()
            option.add_argument('--headless')
            option.add_argument('--disable-gpu')
            self.driver = self.browser(options=option)
        if self._type == 'edge':
            osVersion = platform.version()
            if int(osVersion.split('.')[-1]) >= 18362:
            # 从RS5（EdgeHTML 18.18362）开始，Edge 的webdriver 已内置，可以通过命令或手动在系统中启用。
                self.driver = self.browser()
        else:
            self.driver = self.browser(executable_path=EXECUTABLE_PATH[self._type])
        self.driver.get(url)
        if maximize_window:
            self.driver.maximize_window()
        self.driver.implicitly_wait(implicitly_wait)
        return self

    def save_screen_shot(self, name='screen_shot'):
        day = time.strftime('%Y%m%d', time.localtime(time.time()))
        screenshot_path = REPORT_PATH + r'\screenshot_%s' % day
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)

        tm = time.strftime('%H%M%S', time.localtime(time.time()))
        screenshot = self.driver.save_screenshot(screenshot_path + '\\%s_%s.png' % (name, tm))
        return screenshot

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()
