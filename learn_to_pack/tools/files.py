# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Learn-to-Pack -> files.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-26 11:29
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
import os
from datetime import datetime

from learn_to_pack.config import Project_Name


def getProjectPath():
    file_path = os.getcwd()
    project_path = file_path[:file_path.index(Project_Name)] + Project_Name
    return project_path


def main(name):
    print(f'Hi, {name}', datetime.now())
    print(getProjectPath())
    pass


if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)
