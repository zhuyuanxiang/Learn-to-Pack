# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Learn-to-Pack -> config.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-24 17:03
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
from datetime import datetime

"""
报错数据集有（空心）：han,jakobs1,jakobs2
形状过多暂时未处理：shapes、shirt、swim、trousers
"""
# datasets_name = ["ga", "albano", "blaz1", "blaz2", "dighe1", "dighe2", "fu", "han", "jakobs1", "jakobs2", "mao",
#                  "marques", "shapes", "shirts", "swim", "trousers", "convex", "simple", "ali2", "ali3"]
# scale = [100, 0.5, 100, 100, 20, 20, 20, 10, 20, 20, 0.5, 20, 50, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1]
datasets_name = ["dental", "ga", "albano", "blaz", "dighe1", "dighe2",
                 "fu", "han", "mao",
                 "marques", "shapes0", "shapes1", "shirts", "swim",
                 "trousers", "convex", "simple"]
scale = [5, 100, 0.5, 100, 20, 20,
         20, 10, 0.5,
         20, 50, 50, 1, 1, 1,
         1, 1, 3, 1, 1, 1, 1, 1]


def main(name):
    print(f'Hi, {name}', datetime.now())
    pass


if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)
bias = 0.000001
Project_Name = "Learn-to-Pack"
