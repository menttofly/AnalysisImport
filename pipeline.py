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

    def run(self, module: str, files: list[str]):
        """
        按组件 module 处理其中 .{h,m}
        """
        for file in files:
            for plugin in self.__plugins:
                plugin.process(module, file)