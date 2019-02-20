import unittest  # 单元测试模块
from selenium import webdriver
from utils.config import Config, DATA_PATH, DRIVER_PATH # 引入配置
from test.page.baidu_result_page import BaiDuMainPage
from utils.file_reader import ExcelReader


class TestDemo(unittest.TestCase):
    URL = Config().get('api_url')
    excel = DATA_PATH + '/baidu.xlsx'

    def setUp(self):
        # 初始页面是main page，传入浏览器类型打开浏览器

        #self.driver = webdriver.Chrome(executable_path=DRIVER_PATH + '\chromedriver.exe')
        self.page = BaiDuMainPage(browser_type='chrome').get(self.URL, maximize_window=False)
        print(self.page)

    def tearDown(self):
        self.driver.quit()  # 清理退出
        print('demo')

    def test_search(self):

        self.tearDown()


if __name__ == '__main__':
    unittest.main()