#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

from plugins.plugin import Plugin

class Pipeline:
    """
    串联 Plugin，执行主流程
    """
    def __init__(self, plugins: list[Plugin]) -> None:
        self.__plugins = plugins

    def run(self, pod: str, source_files: list[str]):
        """
        以 pod 为单位，处理源文件
        """
        for file in source_files:
            for plugin in self.__plugins:
                plugin.process(pod, file)