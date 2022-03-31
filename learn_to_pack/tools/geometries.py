# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Learn-to-Pack -> geometries.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-26 15:11
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
from datetime import datetime

from learn_to_pack.shapes.nfp import NFP


def getNFP(poly1, poly2):  # 这个函数必须放在class外面否则多进程报错
    nfp = NFP(poly1, poly2).nfp
    return nfp

def main(name):
    print(f'Hi, {name}', datetime.now())
    pass


if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)