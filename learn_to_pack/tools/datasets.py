# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Learn-to-Pack -> datasets.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-26 11:13
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
import json
import pprint
import random
from datetime import datetime

import pandas as pd

from learn_to_pack.config import datasets_name
from learn_to_pack.config import scale
from learn_to_pack.geometry.geofunc import GeoFunc
from learn_to_pack.tools.files import getProjectPath


def get_data(index=5):
    print("开始处理", datasets_name[index], "数据集")
    # 暂时没有考虑宽度，全部缩放来表示
    print("缩放", scale[index], "倍")
    df = pd.read_csv(getProjectPath() + "\\data\\" + datasets_name[index] + ".csv")
    polygons = []
    for i in range(0, df.shape[0]):
        # for i in range(0,4):
        for j in range(0, df['num'][i]):
            poly = json.loads(df['polygon'][i])
            GeoFunc.normData(poly, scale[index])
            polygons.append(poly)
    return polygons


def get_convex(**kw):
    df = pd.read_csv(getProjectPath() + "\\record\\convex.csv")
    polygons = []
    poly_index = []
    if 'num' in kw:
        for i in range(kw["num"]):
            poly_index.append(random.randint(0, 7000))
    elif 'certain' in kw:
        poly_index = [1000, 2000, 3000, 4000, 5000, 6000, 7000]
    else:
        poly_index = [1000, 2000, 3000, 4000, 5000, 6000, 7000]
    # poly_index=[5579, 2745, 80, 6098, 3073, 8897, 4871, 4266, 3477, 3266, 8016, 4563, 1028, 10842, 1410, 7254,
    # 5953, 82, 1715, 300]
    for i in poly_index:
        poly = json.loads(df['polygon'][i])
        polygons.append(poly)
    if 'with_index' in kw:
        return poly_index, polygons
    return polygons


def main(name):
    print(f'Hi, {name}', datetime.now())
    polygons = get_data()
    pprint.pprint(polygons)
    pass


if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)
