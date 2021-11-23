#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import re

from .plugin import Plugin
from cocoapods.sandbox import PodsSandbox
from cocoapods.parser.dependency import Dependency

"""
修复依赖关系
"""
class DependencyPlugin(Plugin):
    """
    检测缺失依赖声明
    """
    def __init__(self, sanbox: PodsSandbox):
        self.sanbox = sanbox
        self.__dependencies = set()
        self.__file_dependencies = []

    def process(self, pod: str, input_file: str):

        with open(input_file, "r") as f:

            imports, dependencies = [], self.sanbox.dependency.dependencies(pod)
            lines = f.readlines()
            for i in range(len(lines)):
                import_syntax = re.match(r'#import\s["<](\w+\/\S+.[hp]+)[">]', lines[i])
                if not import_syntax:
                    continue

                target = self.sanbox.target_for_namespaced_headers.get(import_syntax[1])
                if not target or target == pod: continue

                # 在现有依赖声明中
                if dependencies and target in dependencies:
                    continue

                self.__dependencies.add(target)
                imports.append({
                    "line_no": (i + 1),
                    "detail": import_syntax.group()
                })
            
            if len(imports) == 0:
                return

            self.__file_dependencies.append({
                "file": input_file,
                "imports": imports
            })

    @property
    def name(self) -> str:
        return "depedencies"

    @property
    def ouput(self) -> any:
        if len(self.__dependencies) == 0:
            return None
        
        return {
            "missing_dependencies": list(self.__dependencies),
            "file_import_details": self.__file_dependencies
        }