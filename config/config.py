#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import configparser

# 获取文件的当前路径（绝对路径）
cur_path = os.path.dirname(os.path.realpath(__file__))


# 获取config.ini的路径
config_path = os.path.join(cur_path, 'config.ini')


conf = configparser.ConfigParser()
conf.read(config_path)
# sections = conf.sections()


def g(s, o=None):
    
        if s in conf:
            if o is None :
                return conf.items(s)
            else:
                try:
                    return conf.get(s,o)
                except Exception as e:
                    return None
        else:
            raise Exception("config sections error:%s is undefine", s)
    
def all():
    ConfVar = {}
    for s in conf.sections():
        ConfVar[s] = {}
        for o in conf.items(s):
            ConfVar[s][o[0]] = o[1]
    return ConfVar
