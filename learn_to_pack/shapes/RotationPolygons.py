# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Learn-to-Pack -> RotationPolygons.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-26 15:17
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
import random
from datetime import datetime

import numpy as np
from shapely import affinity
from shapely.geometry import mapping
from shapely.geometry import Polygon


class RotationPoly():
    def __init__(self, angle):
        self.angle = angle
        self._max = 360 / angle

    def rotation(self, poly):
        if self._max > 1:
            # print("旋转图形")
            rotation_res = random.randint(1, self._max - 1)
            Poly = Polygon(poly)
            new_Poly = affinity.rotate(Poly, rotation_res * self.angle)
            mapping_res = mapping(new_Poly)
            new_poly = mapping_res["coordinates"][0]
            for index in range(0, len(poly)):
                poly[index] = [new_poly[index][0], new_poly[index][1]]
        else:
            pass
            # print("不允许旋转")

    def rotation_specific(self, poly, angle=-1):
        '''
        旋转特定角度
        '''
        Poly = Polygon(poly)
        if angle == -1:
            angle = self.angle
        elif len(angle) > 0:
            angle = np.random.choice(angle)
            # print('旋转{}°'.format(angle))
        new_Poly = affinity.rotate(Poly, angle)
        mapping_res = mapping(new_Poly)
        new_poly = mapping_res["coordinates"][0]
        for index in range(0, len(poly)):
            poly[index] = [new_poly[index][0], new_poly[index][1]]


def main(name):
    print(f'Hi, {name}', datetime.now())
    pass


if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)
