#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

from pipeline import Pipeine

"""
修复依赖关系
"""
class RepairDependency(Pipeine):

    def process(self, file: str) -> str:
        return ""