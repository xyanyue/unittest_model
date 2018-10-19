#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests

def get(url, params={}, cookie={}, header={}):
    """
    定义get方法请求
    :return:
    """
    try:
        r = requests.get(url=url, params=params,
                         cookies=cookie, headers=header, timeout=60)
        return [r.status_code, url, r.text]
    except TimeoutError:
        return [600, url, "get request timeout 60s!"]

def post(url, params={}, cookie={}, header={}):
    """
    定义post方法请求
    :return:
    """
    try:
        r = requests.post(url=url, data=params,
                          cookies=cookie, headers=header, timeout=60)

        return [r.status_code, url, r.text]
    except TimeoutError:
        return [600, url, "get request timeout 60s!"]
