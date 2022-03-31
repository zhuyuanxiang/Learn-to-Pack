# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Learn-to-Pack -> test_nfp.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-24 16:32
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
from datetime import datetime

import pytest


def test_a():
    print("test_a")
    assert 1


def test_b():
    print("test_b")
    assert 0


def main(name):
    print(f'Hi, {name}', datetime.now())
    pytest.main(["-s", "test_nfp.py"])
    pass


if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)
