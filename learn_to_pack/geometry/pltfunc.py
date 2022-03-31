# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Learn-to-Pack -> pltfunc.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-24 16:49
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
from datetime import datetime

from matplotlib import pyplot as plt


def main(name):
    print(f'Hi, {name}', datetime.now())
    pass


if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)


class PltFunc(object):
    @staticmethod
    def addPolygon(poly):
        for i in range(0, len(poly)):
            if i == len(poly) - 1:
                PltFunc.addLine([poly[i], poly[0]])
            else:
                PltFunc.addLine([poly[i], poly[i + 1]])

    @staticmethod
    def addPolygonColor(poly):
        for i in range(0, len(poly)):
            if i == len(poly) - 1:
                PltFunc.addLine([poly[i], poly[0]], color="blue")
            else:
                PltFunc.addLine([poly[i], poly[i + 1]], color="blue")

    @staticmethod
    def addLine(line, **kw):
        if len(kw) == 0:
            plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color="black", linewidth=0.5)
        else:
            plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color=kw["color"], linewidth=0.5)

    @staticmethod
    def showPlt(**kw):
        if len(kw) > 0:
            if "minus" in kw:
                plt.axhline(y=0, c="blue")
                plt.axvline(x=0, c="blue")
                plt.axis([-kw["minus"], kw["width"], -kw["minus"], kw["height"]])

            else:
                plt.axis([0, kw["width"], 0, kw["height"]])
        else:
            plt.axis([0, 3000, 0, 3000])
            # plt.axis([-1000,2000,-979400.4498015114,20000])
            # plt.axis([-500,1000,0,1500])
        plt.show()
        plt.clf()

    def showPolys(polys):
        for poly in polys:
            PltFunc.addPolygon(poly)
        PltFunc.showPlt(width=2000, height=2000)

    def saveFig(name):
        plt.savefig('figs\\' + name + '.png')
        plt.cla()
