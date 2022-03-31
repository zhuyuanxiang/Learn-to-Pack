# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Learn-to-Pack -> bottom_left_fill.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-24 16:00
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
import copy
import random
from datetime import datetime

from shapely.geometry import Polygon

from learn_to_pack.geometry.geofunc import GeoFunc
from learn_to_pack.geometry.pltfunc import PltFunc
from learn_to_pack.shapes import NFPAssistant1
from learn_to_pack.shapes.nfp import NFP
from learn_to_pack.shapes.poly import Poly
from learn_to_pack.shapes.RotationPolygons import RotationPoly
from learn_to_pack.tools.datasets import get_data
from tools import packing as packing


class BottomLeftFill(object):
    def __init__(self, width, original_polygons, **kw):
        self.choose_nfp = False
        self.width = width
        self.length = 150000  # 代表长度
        self.contain_length = 3000
        self.polygons = original_polygons
        self.place_first_poly()
        self.NFPAssistant = None
        if 'NFPAssistant' in kw:
            self.NFPAssistant = kw["NFPAssistant"]
        # else:
        #     # 若未指定外部NFP_assistant则内部使用NFP_assistant开多进程
        #     self.NFPAssistant=packing.NFPAssistant(self.polygons,fast=True)
        self.vertical = False
        if 'vertical' in kw:
            self.vertical = kw['vertical']
        if 'rectangle' in kw:
            self.rectangle = True
        else:
            self.rectangle = False
        # for i in range(1,3):
        for i in range(1, len(self.polygons)):
            # print("##############################放置第",i+1,"个形状#################################")
            self.place_poly(i)

        self.get_length()
        # self.show_all()

    def place_first_poly(self):
        poly = self.polygons[0]
        left_index, bottom_index, right_index, top_index = GeoFunc.checkBound(poly)  # 获得边界
        GeoFunc.slidePoly(poly, -poly[left_index][0], -poly[bottom_index][1])  # 平移到左下角

    def place_poly(self, index):
        adjoin = self.polygons[index]
        # 是否垂直
        if self.vertical:
            ifr = packing.PackingUtil.getInnerFitRectangle(self.polygons[index], self.width, self.length)
        else:
            ifr = packing.PackingUtil.getInnerFitRectangle(self.polygons[index], self.length, self.width)
        differ_region = Polygon(ifr)

        for main_index in range(0, index):
            main_poly = self.polygons[main_index]
            if self.NFPAssistant is None:
                nfp = NFP(main_poly, adjoin, rectangle=self.rectangle).nfp
            else:
                nfp = self.NFPAssistant.getDirectNFP(main_poly, adjoin)
            nfp_poly = Polygon(nfp)
            try:
                differ_region = differ_region.difference(nfp_poly)
            except:  # ToDo: 捕捉合适的异常
                print('NFP failure, polys and nfp are:')
                print([main_poly, adjoin])
                print(nfp)
                self.show_all()
                self.show_polys([main_poly] + [adjoin] + [nfp])
                print('NFP loaded from: ', self.NFPAssistant.history_path)

        differ = GeoFunc.polyToArr(differ_region)
        differ_index = self.get_bottom_left(differ)
        refer_pt_index = GeoFunc.checkTop(adjoin)
        GeoFunc.slideToPoint(self.polygons[index], adjoin[refer_pt_index], differ[differ_index])

    def get_bottom_left(self, poly):
        """
        获得左底部点，优先左侧，有多个左侧选择下方
        """
        bl = []  # bottom left的全部点
        _min = 999999
        # 选择最左侧的点
        for i, pt in enumerate(poly):
            pt_object = {
                    "index": i,
                    "x"    : pt[0],
                    "y"    : pt[1]
            }
            if self.vertical:
                target = pt[1]
            else:
                target = pt[0]
            if target < _min:
                _min = target
                bl = [pt_object]
            elif target == _min:
                bl.append(pt_object)
        if len(bl) == 1:
            return bl[0]["index"]
        else:
            if self.vertical:
                target = "x"
            else:
                target = "y"
            _min = bl[0][target]
            one_pt = bl[0]
            for pt_index in range(1, len(bl)):
                if bl[pt_index][target] < _min:
                    one_pt = bl[pt_index]
                    _min = one_pt["y"]
            return one_pt["index"]

    def show_all(self):
        # for i in range(0,2):
        for i in range(0, len(self.polygons)):
            PltFunc.addPolygon(self.polygons[i])
        length = max(self.width, self.contain_length)
        # PltFunc.addLine([[self.width,0],[self.width,self.contain_height]],color="blue")
        PltFunc.showPlt(width=max(length, self.width), height=max(length, self.width), minus=100)

    def show_polys(self, polys):
        for i in range(0, len(polys) - 1):
            PltFunc.addPolygon(polys[i])
        PltFunc.addPolygonColor(polys[len(polys) - 1])
        length = max(self.width, self.contain_length)
        PltFunc.showPlt(width=max(length, self.width), height=max(length, self.width), minus=200)

    def get_length(self):
        _max = 0
        for i in range(0, len(self.polygons)):
            if self.vertical:
                extreme_index = GeoFunc.checkTop(self.polygons[i])
                extreme = self.polygons[i][extreme_index][1]
            else:
                extreme_index = GeoFunc.checkRight(self.polygons[i])
                extreme = self.polygons[i][extreme_index][0]
            if extreme > _max:
                _max = extreme
        self.contain_length = _max
        # PltFunc.addLine([[0,self.contain_length],[self.width,self.contain_length]],color="blue")
        return _max


class PolyListProcessor(object):
    @staticmethod
    def getPolyObjectList(polys, allowed_rotation):
        """
        将Polys和允许旋转的角度转化为poly_lists
        """
        poly_list = []
        for i, poly in enumerate(polys):
            poly_list.append(Poly(i, poly, allowed_rotation))
        return poly_list

    @staticmethod
    def getPolysVertices(_list):
        """排序结束后会影响"""
        polys = []
        for i in range(len(_list)):
            polys.append(_list[i].poly)
        return polys

    @staticmethod
    def getPolysVerticesCopy(_list):
        """不影响list内的形状"""
        polys = []
        for i in range(len(_list)):
            polys.append(copy.deepcopy(_list[i].poly))
        return polys

    @staticmethod
    def getPolyListIndex(poly_list):
        index_list = []
        for i in range(len(poly_list)):
            index_list.append(poly_list[i].num)
        return index_list

    @staticmethod
    def getIndex(item, _list):
        for i in range(len(_list)):
            if item == _list[i]:
                return i
        return -1

    @staticmethod
    def getIndexMulti(item, _list):
        index_list = []
        for i in range(len(_list)):
            if item == _list[i]:
                index_list.append(i)
        return index_list

    @staticmethod
    def packingLength(poly_list, history_index_list, history_length_list, width, **kw):
        polys = PolyListProcessor.getPolysVertices(poly_list)
        index_list = PolyListProcessor.getPolyListIndex(poly_list)
        length = 0
        check_index = PolyListProcessor.getIndex(index_list, history_index_list)
        if check_index >= 0:
            length = history_length_list[check_index]
        else:
            try:
                if 'NFPAssistant' in kw:
                    length = BottomLeftFill(width, polys, NFPAssistant=kw['NFPAssistant']).contain_length
                else:
                    length = BottomLeftFill(width, polys).contain_length
            except:
                print('出现Self-intersection')
                length = 99999
            history_index_list.append(index_list)
            history_length_list.append(length)
        return length

    @staticmethod
    def randomSwap(poly_list, target_id):
        new_poly_list = copy.deepcopy(poly_list)

        swap_with = int(random.random() * len(new_poly_list))

        item1 = new_poly_list[target_id]
        item2 = new_poly_list[swap_with]

        new_poly_list[target_id] = item2
        new_poly_list[swap_with] = item1
        return new_poly_list

    @staticmethod
    def random_rotate(poly_list, min_angle, target_id):
        new_poly_list = copy.deepcopy(poly_list)

        index = random.randint(0, len(new_poly_list) - 1)
        RotationPoly(min_angle).rotation(new_poly_list[index].poly)
        return new_poly_list

    @staticmethod
    def show_poly_list(width, poly_list):
        blf = BottomLeftFill(width, PolyListProcessor.getPolysVertices(poly_list))
        blf.show_all()

    @staticmethod
    def deleteRedundancy(_arr):
        new_arr = []
        for item in _arr:
            if not item in new_arr:
                new_arr.append(item)
        return new_arr

    @staticmethod
    def getPolysByIndex(index_list, poly_list):
        choosed_poly_list = []
        for i in index_list:
            choosed_poly_list.append(poly_list[i])
        return choosed_poly_list


def main(name):
    print(f'Hi, {name}', datetime.now())
    start_time = datetime.now()
    polygons = get_data(index=0)  # 只处理 dental 数据
    nfp_ass = NFPAssistant1.NFPAssistant(polygons, store_nfp=False, get_all_nfp=True, load_history=True)
    blf = BottomLeftFill(1500, polygons, vertical=False, NFPAssistant=nfp_ass)
    print("总共耗时：", datetime.now() - start_time)
    blf.show_all()


if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)
