# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Learn-to-Pack -> nfp.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-24 16:04
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
import copy
import json
import random
from datetime import datetime

import pandas as pd
from shapely.geometry import LineString
from shapely.geometry import mapping
from shapely.geometry import Point
from shapely.geometry import Polygon

from learn_to_pack.geometry.geofunc import GeoFunc
from learn_to_pack.geometry.pltfunc import PltFunc


class NFP(object):
    def __init__(self, poly1, poly2, **kw):
        self.stationary = copy.deepcopy(poly1)
        self.sliding = copy.deepcopy(poly2)
        start_point_index = GeoFunc.checkBottom(self.stationary)
        self.start_point = [poly1[start_point_index][0], poly1[start_point_index][1]]
        self.locus_index = GeoFunc.checkTop(self.sliding)
        # 如果不加 list 则 original_top 是指针
        self.original_top = list(self.sliding[self.locus_index])
        GeoFunc.slideToPoint(self.sliding, self.sliding[self.locus_index], self.start_point)
        self.start = True  # 判断是否初始
        self.nfp = []
        self.rectangle = False
        if 'rectangle' in kw:
            if kw["rectangle"]:
                self.rectangle = True
        self.error = 1
        self.main()
        if 'show' in kw:
            if kw["show"]:
                self.showResult()

    def main(self):
        i = 0
        if self.rectangle:  # 若矩形则直接快速运算 点的index为左下角开始逆时针旋转
            width = self.sliding[1][0] - self.sliding[0][0]
            height = self.sliding[3][1] - self.sliding[0][1]
            self.nfp.append([self.stationary[0][0], self.stationary[0][1]])
            self.nfp.append([self.stationary[1][0] + width, self.stationary[1][1]])
            self.nfp.append([self.stationary[2][0] + width, self.stationary[2][1] + height])
            self.nfp.append([self.stationary[3][0], self.stationary[3][1] + height])
        else:
            while not self.judgeEnd() and i < 75:  # 大于等于75会自动退出的，一般情况是计算出错
                # while i<7:
                # print("########第",i,"轮##########")
                touching_edges = self.detectTouching()
                all_vectors = self.potentialVector(touching_edges)
                if len(all_vectors) == 0:
                    print("没有可行向量")
                    self.error = -2  # 没有可行向量
                    break

                vector = self.feasibleVector(all_vectors, touching_edges)
                if not vector:
                    print("没有计算出可行向量")
                    self.error = -5  # 没有计算出可行向量
                    break

                self.trimVector(vector)
                if vector == [0, 0]:
                    print("未进行移动")
                    self.error = -3  # 未进行移动
                    break

                GeoFunc.slidePoly(self.sliding, vector[0], vector[1])
                self.nfp.append([self.sliding[self.locus_index][0], self.sliding[self.locus_index][1]])
                i = i + 1
                inter = Polygon(self.sliding).intersection(Polygon(self.stationary))
                if GeoFunc.computeInterArea(inter) > 1:
                    print("出现相交区域")
                    self.error = -4  # 出现相交区域
                    break

        if i == 75:
            print("超出计算次数")
            self.error = -1  # 超出计算次数

    # 检测相互的连接情况
    def detectTouching(self):
        touch_edges = []
        stationary_edges, sliding_edges = self.getAllEdges()
        # print(stationary_edges)
        # print(sliding_edges)
        for edge1 in stationary_edges:
            for edge2 in sliding_edges:
                inter = GeoFunc.intersection(edge1, edge2)
                if inter:
                    # print("edge1:",edge1)
                    # print("edge2:",edge2)
                    # print("inter:",inter)
                    # print("")
                    pt = [inter[0], inter[1]]  # 交叉点
                    edge1_bound = (GeoFunc.almostEqual(edge1[0], pt) or GeoFunc.almostEqual(edge1[1], pt))  # 是否为边界
                    edge2_bound = (GeoFunc.almostEqual(edge2[0], pt) or GeoFunc.almostEqual(edge2[1], pt))  # 是否为边界
                    stationary_start = GeoFunc.almostEqual(edge1[0], pt)  # 是否开始
                    orbiting_start = GeoFunc.almostEqual(edge2[0], pt)  # 是否开始
                    touch_edges.append({
                            "edge1"           : edge1,
                            "edge2"           : edge2,
                            "vector1"         : self.edgeToVector(edge1),
                            "vector2"         : self.edgeToVector(edge2),
                            "edge1_bound"     : edge1_bound,
                            "edge2_bound"     : edge2_bound,
                            "stationary_start": stationary_start,
                            "orbiting_start"  : orbiting_start,
                            "pt"              : [inter[0], inter[1]],
                            "type"            : 0
                    })
        return touch_edges

        # 获得潜在的可转移向量

    def potentialVector(self, touching_edges):
        all_vectors = []
        for touching in touching_edges:
            # print("touching:",touching)
            aim_edge = []
            # 情况1
            if touching["edge1_bound"] and touching["edge2_bound"]:
                right, left, parallel = GeoFunc.judgePosition(touching["edge1"], touching["edge2"])
                # print("right,left,parallel:",right,left,parallel)
                if touching["stationary_start"] and touching["orbiting_start"]:
                    touching["type"] = 0
                    if left:
                        aim_edge = [touching["edge2"][1], touching["edge2"][0]]  # 反方向
                    if right:
                        aim_edge = touching["edge1"]
                if touching["stationary_start"] and not touching["orbiting_start"]:
                    touching["type"] = 1
                    if left:
                        aim_edge = touching["edge1"]
                if not touching["stationary_start"] and touching["orbiting_start"]:
                    touching["type"] = 2
                    if right:
                        aim_edge = [touching["edge2"][1], touching["edge2"][0]]  # 反方向
                if not (touching["stationary_start"] or touching["orbiting_start"]):
                    touching["type"] = 3

            # 情况2
            if touching["edge1_bound"] == False and touching["edge2_bound"] == True:
                aim_edge = [touching["pt"], touching["edge1"][1]]
                touching["type"] = 4

            # 情况3
            if touching["edge1_bound"] and not touching["edge2_bound"]:
                aim_edge = [touching["edge2"][1], touching["pt"]]
                touching["type"] = 5

            if aim_edge:
                vector = self.edgeToVector(aim_edge)
                if not self.detectExisting(all_vectors, vector):  # 删除重复的向量降低计算复杂度
                    all_vectors.append(vector)
        return all_vectors

    def detectExisting(self, vectors, judge_vector):
        for vector in vectors:
            if GeoFunc.almostEqual(vector, judge_vector):
                return True
        return False

    def edgeToVector(self, edge):
        return [edge[1][0] - edge[0][0], edge[1][1] - edge[0][1]]

    # 选择可行向量
    def feasibleVector(self, all_vectors, touching_edges):
        """
        ToDo:该段代码需要重构，过于复杂
        """
        res_vector = []
        # print("\n all_vectors:",all_vectors)
        for vector in all_vectors:
            feasible = True
            # print("\n vector:",vector,"\n")
            for touching in touching_edges:
                vector1, vector2 = [], []
                # 判断方向并进行转向
                if touching["stationary_start"]:
                    vector1 = touching["vector1"]
                else:
                    vector1 = [-touching["vector1"][0], -touching["vector1"][1]]
                if touching["orbiting_start"]:
                    vector2 = touching["vector2"]
                else:
                    vector2 = [-touching["vector2"][0], -touching["vector2"][1]]
                vector12_product = GeoFunc.crossProduct(vector1, vector2)  # 叉积，大于0在左侧，小于0在右侧，等于0平行
                vector_vector1_product = GeoFunc.crossProduct(vector1, vector)  # 叉积，大于0在左侧，小于0在右侧，等于0平行
                vector_vector2_product = GeoFunc.crossProduct(vector2, vector)  # 叉积，大于0在左侧，小于0在右侧，等于0平行
                # print("vector:",vector)
                # print("type:",touching["type"])
                # print("vector12_product:",vector12_product)
                # print("vector1:",vector1)
                # print("vector2:",vector2)
                # print("vector_vector1_product:",vector_vector1_product)
                # print("vector_vector2_product:",vector_vector2_product)
                # 最后两种情况
                if touching["type"] == 4 and (vector_vector1_product * vector12_product) < 0:
                    feasible = False
                if touching["type"] == 5 and (vector_vector2_product * (-vector12_product)) > 0:
                    feasible = False
                # 正常的情况处理
                if vector12_product > 0:
                    if vector_vector1_product < 0 and vector_vector2_product < 0:
                        feasible = False
                if vector12_product < 0:
                    if vector_vector1_product > 0 and vector_vector2_product > 0:
                        feasible = False
                # 平行情况，需要用原值逐一判断
                if vector12_product == 0:
                    inter = GeoFunc.newLineInter(touching["edge1"], touching["edge2"])
                    # print("inter['geom_type']:",inter["geom_type"])
                    # print(inter)
                    if inter["geom_type"] == "LineString":
                        if inter["length"] > 0.01:
                            # 如果有相交，则需要在左侧
                            if (touching["orbiting_start"] and vector_vector2_product < 0) or (
                                    not touching["orbiting_start"] and vector_vector2_product > 0):
                                feasible = False
                    else:
                        # 如果方向相同，且转化直线也平行，则其不能够取a的方向
                        if touching["orbiting_start"] == True != touching[
                            "stationary_start"] == False and vector_vector1_product == 0:
                            if touching["vector1"][0] * vector[0] > 0:  # 即方向相同
                                feasible = False
            #     if feasible==False:
            #         print("feasible:",False)
            #     print("")
            # print("feasible:",feasible)
            # print("")
            if feasible:
                res_vector = vector
                break
        return res_vector

    # 削减过长的向量
    def trimVector(self, vector):
        stationary_edges, sliding_edges = self.getAllEdges()
        new_vectors = []
        for pt in self.sliding:
            for edge in stationary_edges:
                line_vector = LineString([pt, [pt[0] + vector[0], pt[1] + vector[1]]])
                end_pt = [pt[0] + vector[0], pt[1] + vector[1]]
                line_polygon = LineString(edge)
                inter = line_vector.intersection(line_polygon)
                if inter.geom_type == "Point":
                    inter_mapping = mapping(inter)
                    inter_coordinate = inter_mapping["coordinates"]
                    # if (end_pt[0]!=inter_coordinate[0] or end_pt[1]!=inter_coordinate[1]) and (pt[
                    # 0]!=inter_coordinate[0] or pt[
                    # 1]!=inter_coordinate[1]):
                    if (abs(end_pt[0] - inter_coordinate[0]) > 0.01 or abs(
                            end_pt[1] - inter_coordinate[1]) > 0.01) and (
                            abs(pt[0] - inter_coordinate[0]) > 0.01 or abs(pt[1] - inter_coordinate[1]) > 0.01):
                        # print("start:",pt)
                        # print("end:",end_pt)
                        # print("inter:",inter)
                        # print("")
                        new_vectors.append([inter_coordinate[0] - pt[0], inter_coordinate[1] - pt[1]])

        for pt in self.stationary:
            for edge in sliding_edges:
                line_vector = LineString([pt, [pt[0] - vector[0], pt[1] - vector[1]]])
                end_pt = [pt[0] - vector[0], pt[1] - vector[1]]
                line_polygon = LineString(edge)
                inter = line_vector.intersection(line_polygon)
                if inter.geom_type == "Point":
                    inter_mapping = mapping(inter)
                    inter_coordinate = inter_mapping["coordinates"]
                    # if (end_pt[0]!=inter_coordinate[0] or end_pt[1]!=inter_coordinate[1]) and (pt[
                    # 0]!=inter_coordinate[0] or pt[
                    # 1]!=inter_coordinate[1]):
                    if (abs(end_pt[0] - inter_coordinate[0]) > 0.01 or abs(
                            end_pt[1] - inter_coordinate[1]) > 0.01) and (
                            abs(pt[0] - inter_coordinate[0]) > 0.01 or abs(pt[1] - inter_coordinate[1]) > 0.01):
                        # print("start:",pt)
                        # print("end:",end_pt)
                        # print("inter:",inter)
                        # print("")
                        new_vectors.append([pt[0] - inter_coordinate[0], pt[1] - inter_coordinate[1]])

        # print(new_vectors)
        for vec in new_vectors:
            if abs(vec[0]) < abs(vector[0]) or abs(vec[1]) < abs(vector[1]):
                # print(vec)
                vector[0] = vec[0]
                vector[1] = vec[1]

    # 获得两个多边形全部边
    def getAllEdges(self):
        return GeoFunc.getPolyEdges(self.stationary), GeoFunc.getPolyEdges(self.sliding)

    # 判断是否结束
    def judgeEnd(self):
        sliding_locus = self.sliding[self.locus_index]
        main_bt = self.start_point
        if abs(sliding_locus[0] - main_bt[0]) < 0.1 and abs(sliding_locus[1] - main_bt[1]) < 0.1:
            if self.start:
                self.start = False
                # print("判断是否结束：否")
                return False
            else:
                # print("判断是否结束：是")
                return True
        else:
            # print("判断是否结束：否")
            return False

    # 显示最终结果
    def showResult(self):
        PltFunc.addPolygon(self.sliding)
        print("self.sliding=", self.sliding)
        PltFunc.addPolygon(self.stationary)
        print("self.stationary=", self.stationary)
        PltFunc.addPolygonColor(self.nfp)
        PltFunc.showPlt()

    # 计算渗透深度
    # ToDo: 未被使用？
    def getDepth(self):
        """
        计算poly2的checkTop到NFP的距离
        Source: https://stackoverflow.com/questions/36972537/distance-from-point-to-polygon-when-inside
        """
        d1 = Polygon(self.nfp).distance(Point(self.original_top))
        # if point in inside polygon, d1=0
        # d2: distance from the point to nearest boundary
        if d1 == 0:
            d2 = Polygon(self.nfp).boundary.distance(Point(self.original_top))
            # print('d2:',d2)
            return d2
        else:
            return 0


def tryNFP():
    """计算NFP然后寻找最合适位置"""
    test_two_polygons()

    # test_two_rects()
    # test_bfp()
    pass


def test_two_polygons():
    # df = pd.read_csv("data/blaz.csv")
    df = pd.read_csv("../../data/train_test/blaz_train_test.csv")
    # df = pd.read_csv("/Users/sean/Documents/Projects/Data/Shapes/now_fail.csv") # 没有这个数据集
    i = random.randint(0, 91)
    print("--->poly1<---")
    poly1 = json.loads(df['poly1'][i])
    print("original poly1=", poly1)
    GeoFunc.normData(poly1, 50)
    print("normal poly1=", poly1)
    print("--->poly2<---")
    poly2 = json.loads(df['poly2'][i])
    print("original poly2=", poly2)
    GeoFunc.normData(poly2, 50)
    print("normal poly2=", poly2)
    print("--->nfp(poly1,poly2)<---")
    poly1 = json.loads(df['poly1'][i])
    poly2 = json.loads(df['poly2'][i])
    GeoFunc.slidePoly(poly1, 1000, 1000)
    print("move poly1=", poly1)
    nfp = NFP(poly1, poly2, show=True, rectangle=False)
    print("nfp(poly1,poly2)=", nfp.nfp)
    pass


def test_bfp():
    # bfp = bestFitPosition(nfp, True)  # bestFitPosition 类没有写完整，不能使用
    # print("Final fitness:", bfp.fitness)
    pass


def test_two_rects():
    print("--->nfp(rect1,rect2)<---")
    rect1 = [[100, 100], [150, 100], [150, 150], [100, 150]]
    rect2 = [[100, 100], [120, 100], [120, 160], [100, 160]]
    nfp = NFP(rect1, rect2, show=True, rectangle=True)
    print("original rect1=", rect1)
    print("original rect2=", rect2)
    print("nfp(rect1,rect2)=", nfp.nfp)


def main(name):
    print(f'Hi, {name}', datetime.now())
    tryNFP()
    pass


if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)
