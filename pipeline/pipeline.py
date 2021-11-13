#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

from abc import ABC, abstractmethod

class Pipeine(ABC):

    @abstractmethod
    def process(self, file: str) -> str:
        """
        接收一个文件，产出 json 字符串
        """
        pass

