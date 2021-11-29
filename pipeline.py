#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import os, json
from cocoapods.sandbox import PodsSandbox
from cocoapods.parser.dependency import Dependency
from plugins.import_plugin import ImportPlugin
from plugins.module_plugin import ModulePlugin
from plugins.dependency_plugin import DependencyPlugin
from plugins.plugin import Plugin

class Pipeline:
    """
    串联 Plugin，执行主流程
    """
    def __init__(self, plugins: list[Plugin], module: str) -> None:
        self.__plugins = plugins
        self.__module = module

    def run(self, files: list[str]):
        """
        按组件 module 处理其中 .{h,m}
        """
        for file in files:
            for plugin in self.__plugins:
                plugin.process(self.__module, file)

    def gather_reports(self):
        """
        报告收集
        """
        for plugin in self.__plugins:
            if not plugin.name or not plugin.ouput:
                continue

            report_dir = os.path.join(os.path.dirname(__file__), "reports")
            if not os.path.exists(report_dir):
                os.makedirs(report_dir)

            json_object = plugin.ouput
            with open(os.path.join(report_dir, f"{self.__module}_{plugin.name}.json"), "w+") as f:
                try:
                    json_str = json.dumps(json_object, indent=4)
                    f.write(json_str)
                except Exception as e:
                    print(f"生成json数据异常：<{str(e)}>")

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

    # 分析当前依赖
    
    dependencies = Dependency("/Users/menttofly/Desktop/Gaoding-iOS/apps/fc_ios/FireCat/Podfile.lock")
    dependencies.analyze()
    sanbox = PodsSandbox("/Users/menttofly/Desktop/Gaoding-iOS/apps/fc_ios/FireCat/Pods", dependencies)

    modules_dir = "/Users/menttofly/Desktop/Gaoding-iOS/modules"
    for x in os.listdir(modules_dir):
        presets = {
            "FireCat": "FireCatApp",
            "FocoDesign": "FocoDesignApp",
            "FocoVideo": "FocoVideoApp",
        }

        target_name = x
        if x in presets.keys():
            target_name = presets[x]

        if target_name not in dependencies.pods: 
            continue

        # 创建 pipeline，引入插件
        pipeline = Pipeline([ImportPlugin(sanbox), DependencyPlugin(sanbox)], target_name) #  ModulePlugin(sanbox),

        source_files = list_all_files(os.path.join(modules_dir, x))
        pipeline.run(source_files)
        pipeline.gather_reports()

    print("Done!!!")