# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Learn-to-Pack -> times.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-26 17:16
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
import functools
import time
from datetime import datetime


def run_time(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kw):
        start = time.time()
        res = fn(*args, **kw)
        print('%s 运行了 %f 秒' % (fn.__name__, time.time() - start))
        return res
    return wrapper


# 测试
@run_time
def test_time(n):
    time.sleep(n)
    print("运行结束了")


def main(name):
    print(f'Hi, {name}', datetime.now())
    test_time(3)
    pass


if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)
