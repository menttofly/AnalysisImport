#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

from abc import ABC, abstractmethod
from cocoapods.sandbox import PodsSandbox

class Plugin(ABC):
    """
    Pipeline 处理文件
    """
    @abstractmethod
    def __init__(self, sanbox: PodsSandbox):
        pass

    @abstractmethod
    def process(self, pod: str, input_file: str):
        """
        执行 import、module 替换等操作
        """
        pass

    @property
    def name(self) -> str:
        "插件名"
        pass

    @property
    def ouput(self) -> any:
        """
        输出分析结果（如有）
        """
        pass
