#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import os
from lazy import lazy_property
from functools import reduce
from dataclasses import dataclass
from cocoapods.parser.umbrella import Umbrella
from cocoapods.parser.xcconfig import Xcconfig

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
                    
                umbrella_imports = Umbrella(os.path.join(root, file)).imports
                module = Module(
                    os.path.basename(root), 
                    os.path.basename(file).split("-")[0], 
                    umbrella_imports
                )

                modules.append(module)
                dir[:] = []

        return modules

    @lazy_property
    def headers_to_module(self) -> dict[str: tuple]:
        """
        umbrella.h 中的头文件 => (所属的 module, pod_name)
        """
        def function(acc: dict, module: Module) -> dict:
            for header in module.umbrella_imports:
                if not acc.get(header):
                    acc[header] = (module.name, module.modulemap_name)
            return acc

        return reduce(function, self.modules, {})

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

                modulemaps = Xcconfig(os.path.join(root, file)).modulemaps
                pod_modulemaps[os.path.basename(root)] = modulemaps
        
        return pod_modulemaps

    @lazy_property
    def pod_headers(self) -> dict:
        """
        所有的 pod => {.h} 映射关系，头文件保留基于 pod 目录相对路径
        """
        private_root = os.path.join(self.__pods_root, "Headers/Private")
        pod_headers = {}

        for x in os.listdir(private_root):
            if x.startswith("."): continue
            
            # 提取 x 组件下的所有头文件
            x, headers = os.path.join(private_root, x), set()
            for root, _, files in os.walk(x):

                for file in files:
                    if not file.endswith(".h"): continue
                    if root != x:
                        file = os.path.join(
                            os.path.relpath(root, x), file
                        )
                    headers.update({file})

            pod_headers[os.path.basename(x)] = headers
        
        return pod_headers

    @lazy_property
    def pod_namespaced_headers(self) -> dict:
        """
        un-namspaced => namespaced 
        """
        merged = {}
        for module, headers in self.pod_headers.items():
            mapping = {
                os.path.basename(x): 
                os.path.join(module, x) for x in headers
            }
            
            for k, v in mapping.items():
                if not merged.get(k):
                    merged[k] = v
                else:
                    print(f"重名头文件: {k}")
        
        return merged