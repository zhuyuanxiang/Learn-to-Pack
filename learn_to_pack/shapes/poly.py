# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Learn-to-Pack -> poly.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-24 15:45
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
from datetime import datetime


class Poly(object):
    """
    用于后续的Poly对象
    """

    def __init__(self, num, poly, allowed_rotation):
        self.num = num
        self.poly = poly
        self.cur_poly = poly
        self.allowed_rotation = [0, 180]


def main(name):
    print(f'Hi, {name}', datetime.now())
    pass


if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)
