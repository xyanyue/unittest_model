#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from config import config
from pubTest import request as RequestMethod
from pubTest import selenium
import types
import unittest
from HTMLTestRunner import HTMLTestRunner
import importlib
import os
import re
import random
import time

TestCasePath = 'testCase'
TestCaseRule = config.g('Main', 'test_case_rule')

# 存储所有testCase配置对象
TestCase = {}
# 存储各个case流程中间结果
TestCaseResult = {}

Selenium_obj = selenium.selenium_chrome()


def getscreen(key):
    r = random.randint(1, 9)
    timeStr = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime())
    return str(key)+str(timeStr)+str(r)+'.png'


def append(case_dict, r_key):
    def add(self):
        self.check(case_dict.keys())
        TestCaseResult[r_key] = {}
        for case_key, case_val in case_dict.items():
            eval("self._"+case_key.replace("-", ""))(r_key, case_val)
    return add


def readTestCase():
    dirs = os.listdir(TestCasePath)
    for d in dirs:
        matchObj = re.match(TestCaseRule, d, re.M | re.I)
        if matchObj:

            key = matchObj.group(1) if matchObj.group(1) else d
            TestCase[key] = {}
            tc = importlib.import_module(TestCasePath+'.'+d.replace('.py', ''))
            # print(tc.__dict__)
            for x in dir(tc):
                if x[0:2] == '__':
                    pass
                else:
                    TestCase[key][x] = eval('tc.'+x)


def addMethodToTest():
    for case_file, test_case in TestCase.items():
        for test_case_name, case_dict in test_case.items():
            r_key = case_file+'_'+test_case_name
            # print(r_key)
            # print(append(case_dict))
            setattr(TestMain, "test_"+r_key, append(case_dict, r_key))
            # test = test_generator(t[1], t[2])
            # setattr(TestSequense, test_name, test)


class TestMain(unittest.TestCase):
    """docstring for TestMain"""
    @classmethod
    def setUpClass(self):
        self.Type = 0
        self.HttpCode = 1
        self.HttpSuccessCode = config.g('Test', 'success_http_code')
        self.Safe = 0

    def default_err(self, msg):
        self.assertEqual(0, 1, msg=msg)

    # 全局修改
    def _type(self, r_key, value):
        self.Type = value

    # 全局修改
    def _safe(self, r_key, value):
        self.Safe = value

    def _get(self, r_key, data):
        url = data['url']
        if self.Type == 0:
            params = data['params'] if 'params' in data.keys() else None
            header = data['header'] if 'header' in data.keys() else None
            cookie = data['cookie'] if 'cookie' in data.keys() else None
            TestCaseResult[r_key]['request'] = RequestMethod.get(
                url, params, header, cookie)
        else:
            TestCaseResult[r_key]['request'] = Selenium_obj.open_page(url)
            Selenium_obj.screenshot(getscreen(r_key+'_load'))

    def _post(self, r_key, data):
        url = data['url']
        if self.Type == 0:
            params = data['params'] if 'params' in data.keys() else None
            header = data['header'] if 'header' in data.keys() else None
            cookie = data['cookie'] if 'cookie' in data.keys() else None
            TestCaseResult[r_key]['request'] = RequestMethod.get(
                url, params, header, cookie)
        else:
            TestCaseResult[r_key]['request'] = Selenium_obj.open_page(url)
            Selenium_obj.screenshot(getscreen(r_key+'_load'))

    def _interaction(self, r_key, data):
        for element in data:
            for k, v in element.items():
                eval("self._"+k)(r_key, v)

    def _element(self, r_key, ele):
        e = Selenium_obj.find(ele)
        if e:
            TestCaseResult[r_key]['element'] = e
        else:
            self.default_err("{0}:没有找到元素:{1}".format(r_key, ele))

    def _action(self, r_key, data):
        for k, v in data.items():
            eval("self._"+k)(r_key, v)

    def _write(self, r_key, v):
        try:
            ele = TestCaseResult[r_key]['element']
            Selenium_obj.base_val(ele, v)
        except Exception as e:
            self.default_err(
                "{0}:_write没有找到元素或者无法完成动作:{1}:{2}".format(r_key, ele, v))
        finally:
            Selenium_obj.screenshot(getscreen(r_key+'_write'))

    def _clear(self, r_key,v=None):
        try:
            ele = TestCaseResult[r_key]['element']
            Selenium_obj.base_clear(ele)
        except Exception as e:
            self.default_err("{0}:_clear没有找到元素或者无法完成动作:{1}".format(r_key, ele))
        finally:
            Selenium_obj.screenshot(getscreen(r_key+'_clear'))

    def _click(self, r_key,v=None):
        try:
            ele = TestCaseResult[r_key]['element']
            Selenium_obj.base_click(ele)
        except Exception as e:
            self.default_err("{0}:_click没有找到元素或者无法完成动作:{1}".format(r_key, ele))
        finally:
            Selenium_obj.screenshot(getscreen(r_key+'_click'))

    def _execute(self, r_key, v):
        try:
            # ele = TestCaseResult[r_key]['element']
            Selenium_obj.execute_script(v)
        except Exception as e:
            self.default_err("{0}:_execute错误:{1}".format(r_key, v))
        finally:
            Selenium_obj.screenshot(getscreen(r_key+'_execute'))

    def _success(self, r_key, data):
        Selenium_obj.screenshot(getscreen(r_key+'_success'))
        for k, v in data.items():
            eval("self._"+k)(r_key, v)

    def _httpCode(self, r_key, value=None):
        if value is None:
            value = self.HttpSuccessCode
        if 'request' in TestCaseResult[r_key]:
            http_code = TestCaseResult[r_key]['request'][0]
            self.assertEqual(int(http_code), int(value), msg="httpCode error:" +
                             str(http_code)+"Url:"+TestCaseResult[r_key]['request'][1])
        else:
            self.assertEqual(0, 1, msg="没有找到任何请求结果")

    def _text(self, r_key, value):
        # print(self.TestCaseResult[r_key]['request'])

        if 'request' in TestCaseResult[r_key]:
            http_text = TestCaseResult[r_key]['request'][2]
            self.assertIn(value, http_text, msg="httpRequest Text error:" +
                          str(value)+"Url:"+TestCaseResult[r_key]['request'][1])
        else:
            self.assertEqual(0, 1, msg="没有找到任何请求结果")

    def check(self, case_dict):
        if 'type' not in case_dict:
            raise Exception('请配置`type`值！！')
        if ('get' not in case_dict) and ('post' not in case_dict):
            raise Exception('请配置`get&post`！！')

    @classmethod
    def init(self):
        return self.__dict__

    def test_b(self):
        self.assertEqual(0, 1, msg="Test-b 失败")

if __name__ == '__main__':

    # print(HTMLTestRunner.__dict__)

    readTestCase()
    addMethodToTest()
    report_title = 'Example用例执行报告'
    desc = '用于展示修改样式后的HTMLTestRunner'
    report_file = 'report/Report.html'

    test_suite = unittest.TestSuite()  # 创建一个测试集合
    for x in TestMain.init():
        if x[0:4] == 'test':
            test_suite.addTest(TestMain(x))

    with open(report_file, 'wb') as report:
        runner = HTMLTestRunner.HTMLTestRunner(stream=report, title=report_title, description=desc)
        runner.run(test_suite)
        Selenium_obj.close()
    




    # with open(report_file, 'wb') as report:
        # unittest.main(testRunner=HTMLTestRunner(stream=report, title=report_title, description=desc))
    # Selenium_obj.close()
    # Selenium_obj.open_page("http://www.baidu.com")
    # Selenium_obj.close()
