# from multiprocessing import Pool
from learn_to_pack.geometry.geofunc import GeoFunc


class PackingUtil(object):

    @staticmethod
    def getInnerFitRectangle(poly, x, y):
        left_index, bottom_index, right_index, top_index = GeoFunc.checkBound(poly)  # 获得边界
        new_poly = GeoFunc.getSlide(poly, -poly[left_index][0], -poly[bottom_index][1])  # 获得平移后的结果

        refer_pt = [new_poly[top_index][0], new_poly[top_index][1]]
        ifr_width = x - new_poly[right_index][0]
        ifr_height = y - new_poly[top_index][1]

        IFR = [refer_pt, [refer_pt[0] + ifr_width, refer_pt[1]], [refer_pt[0] + ifr_width, refer_pt[1] + ifr_height],
               [refer_pt[0], refer_pt[1] + ifr_height]]
        return IFR


