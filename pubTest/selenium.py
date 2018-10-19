#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from config import config
import time
import json


class selenium_chrome(object):
    """docstring for selenium_chrome"""

    def __init__(self):
        # super(selenium_chrome, self).__init__()
        print("-------start-------")
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
        chrome_options.add_argument("--verbose")
        chrome_options.add_argument("--log-path="+config.g('Main', 'log_path'))
        chrome_options.add_argument('lang=zh_CN.UTF-8')
        # chrome_options.add_argument("binary_location=/usr/bin/google-chrome")
        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = {'performance': 'ALL'}
        chrome_options.binary_location = "/usr/bin/google-chrome"
        chromedriver = config.g('Main', 'driver_path')
        # os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(
            chrome_options=chrome_options,
            executable_path=chromedriver,
            desired_capabilities=d
        )

        self._screenshot = config.g('Main', 'screenshot_path')
        self._element_wait = int(config.g('Main', 'element_wait'))
        self._element_wait_interval = float(config.g('Main', 'element_wait_interval'))
        self._page_wait = int(config.g('Main', 'page_wait'))
        # print('#####################')
        # find ele 标记
        self._Element_flag = {
            # "#": "id",
            # ".": "class name",
            "!": "xpath",
            "@": "link text",
            "$": "name",
            "%": "tag name"
        }
    # 打开网页,并且返回源码

    def getHttpStatus(self):
        for responseReceived in self.driver.get_log('performance'):

            try:

                response = json.loads(responseReceived[u'message'])[
                    u'message'][u'params'][u'response']

                if response[u'url'] == self.driver.current_url:
                    return (response[u'status'], response[u'statusText'])
            except:
                pass
        return None

    def open_page(self, url):
        # http_status = 600
        self.driver.get(url)
        self.driver.implicitly_wait(self._page_wait)
        http_status = self.getHttpStatus()
        if http_status:
            return [http_status[0], self.driver.current_url, self.driver.page_source]
        else:
            return [600, self.driver.current_url, self.driver.page_source]

    def driver(self):
        return self.driver

    # 保存截图
    def screenshot(self, file_name, path=''):
        path = path.lstrip("/")
        if path and (not os.path.exists(self._screenshot+path)):
            os.makedirs(self._screenshot+path)
        self.driver.save_screenshot(self._screenshot+path+file_name)

    # id 使用 # class使用. xpath 使用// 原生页面元素不带任何东西
    # by_id= "id"
    # by_xpath = "xpath"
    # by_link_text = "link text"
    # by_partial_text = "partial link text"
    # by_name = "name"
    # by_tag_name = "tag name"
    # by_class_name = "class name"
    # by_css_selector = "css selector"
    def find(self, f, by=None):
        try:
            f = f.strip()
            if f[0:1] in self._Element_flag.keys():
                return WebDriverWait(self.driver, self._element_wait, self._element_wait_interval, ignored_exceptions=True).until(EC.presence_of_all_elements_located((self._Element_flag[f[0:1]], f[1:])))

            return WebDriverWait(self.driver, self._element_wait, self._element_wait_interval, ignored_exceptions=True).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, f)))
        except Exception as e:
            return None

    def base_val(self, element, value):
        if isinstance(element,list):
            for ele in element:   
                ele.send_keys(value)
        else:
            element.send_keys(value)

    def base_click(self, element):
        if isinstance(element,list):
            for ele in element:   
                ele.click()
        else:
            element.click()
    def base_clear(self, element):
        if isinstance(element,list):
            for ele in element:   
                ele.clear()
        else:
            element.clear()

    def val(self, find_element, value):
        # print(find_element,value)
        element = self.find(find_element)
        # print(element)
        if element:
            for ele in element:
                self.base_val(ele, value)
            return True
        else:
            False

    def clear(self, find_element):
        # self.base_clear(self.find(find_element))
        element = self.find(find_element)
        if element:
            for ele in element:
                self.base_clear(ele, value)
            return True
        else:
            False

    def click(self, find_element):
        element = self.find(find_element)
        if element:
            for ele in element:
                self.base_click(ele, value)
            return True
        else:
            False

    def alert(self, accept=1):
        t = WebDriverWait(self.driver, self._element_wait,
                          self._element_wait_interval).until(EC.alert_is_present())
        if accept:
            t.accept()
        else:
            t.dismiss()

    def execute_script(self, script):
        self.driver.execute_script(script)

    # 关闭浏览器
    def close(self):
        self.driver.close()
        self.driver.quit()


if __name__ == '__main__':
    a = selenium_chrome()
    a.open_page("http://www.baidu.com")
