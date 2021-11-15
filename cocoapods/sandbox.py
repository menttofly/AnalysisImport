#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import os
from lazy import lazy_property
from dataclasses import dataclass
from parser.umbrella import Umbrella
from parser.xcconfig import Xcconfig

@dataclass
class Module:
    """
    模块信息
    """
    name: str 
    modulemap_name: str
    umbrella_imports: set[str]

class PodsSandbox:
    """
    提供 $PODS_ROOT 目录下 module、头文件等内容
    """
    def __init__(self, pods_root: str) -> None:
        self.__pods_root = os.path.expanduser(pods_root)
 
    @lazy_property
    def modules(self) -> list[Module]:   
        """
        提取所有 module，写入 name、umbrella headers、modulemap 等信息
        """
        modules = []

        for root, dir, files in os.walk(
            os.path.join(self.__pods_root, "Headers/Public")
        ):
            for file in files:
                if not file.endswith("-umbrella.h"):  continue
                    
                umbrella_imports = Umbrella(file).imports
                module = Module(
                    os.path.basename(root), 
                    os.path.basename(file).split("-")[0], 
                    umbrella_imports
                )

                modules.append(module)
                dir[:] = []

        return modules

    @lazy_property
    def pod_modulemaps(self) -> dict:
        """
        各组件 OTHER_C_FLAGS 已有的 modulemap
        """
        pod_modulemaps = {}

        for root, _, files in os.walk(
            os.path.join(self.__pods_root, "Target Support Files")
        ):
            for file in files:
                if not file.endswith("debug.xcconfig"): continue

                modulemaps = Xcconfig(file).modulemaps
                pod_modulemaps[os.path.basename(root)] = modulemaps
        
        return pod_modulemaps


    @lazy_property
    def private_headers(self) -> dict:
        """
        所有的 pod => {.h} 映射关系
        """
        private_root = os.path.join(self.__pods_root, "Headers/Private")
        res = {}

        for x in os.listdir(private_root):
            if x.startswith("."): continue
            
            # 提取 x 组件下的所有头文件
            headers = set()
            for root, _, files in os.walk(
                os.path.join(private_root, x)
            ):
                headers.update(set(files))

            res[x] = headers
        
        return res