#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import os
from cocoapods.sandbox import PodsSandbox
from cocoapods.parser.dependency import Dependency
from plugins.import_plugin import ImportPlugin
from plugins.module_plugin import ModulePlugin
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

def list_all_files(directory: str) -> list[str]:
    """
    返回指定目录下的所有 .{.h,m} 文件
    """
    res = []
    for root, dir, files in os.walk(directory):
        if root.startswith("."): 
            continue
        if os.path.basename(root) == "Example": 
            dir[:] = [] # 忽略当前目录下的子目录
            continue

        for file in files:
            if file.startswith("."): continue
            if file.endswith('.h') or file.endswith('.m') or file.endswith('.mm'):
                res.append(os.path.join(root, file))

    return res

if __name__ == "__main__":

    # 创建 pipeline，引入插件
    sanbox = PodsSandbox("/Users/menttofly/Desktop/Gaoding-iOS/apps/fc_ios/FireCat/Pods")
    pipeline = Pipeline([ImportPlugin(sanbox), ModulePlugin(sanbox)])

    # 分析当前依赖
    dependencies = Dependency("/Users/menttofly/Desktop/Gaoding-iOS/apps/fc_ios/FireCat/Podfile.lock")
    dependencies.analyze()

    modules_dir = "/Users/menttofly/Desktop/Gaoding-iOS/modules"
    for x in os.listdir(modules_dir):
        presets = {
            "FireCat": "FireCatApp",
            "FocoDesign": "FocoDesignApp",
            "FocoVideo": "FocoVideoApp",
        }

        if x in presets.keys():
            x = presets[x]

        if x not in dependencies.pods: 
            continue

        source_files = list_all_files(os.path.join(modules_dir, x))
        pipeline.run(x, source_files)

    print("Done!!!")