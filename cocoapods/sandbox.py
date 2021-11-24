#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import os, json, subprocess
from functools import reduce, cached_property
from dataclasses import dataclass
from cocoapods.parser.umbrella import Umbrella
from cocoapods.parser.xcconfig import Xcconfig
from cocoapods.parser.dependency import Dependency

@dataclass
class Module(object):
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
    def __init__(self, pods_root: str, dependency: Dependency) -> None:
        self.__pods_root = os.path.expanduser(pods_root)
        self.__dependency = dependency
 
    @cached_property
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

    @cached_property
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

    @cached_property
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

    @cached_property
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

    @cached_property
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

    @cached_property
    def target_for_namespaced_headers(self) -> dict:
        """
        从 hmap 中提取 header 所属的 target 信息
        """
        hmap_file = os.path.join(self.__pods_root, "Headers/Pods-all-target-headers.hmap")
        json_file = os.path.splitext(hmap_file)[0] + ".json"
        
        retcode = subprocess.run(f"hmap convert {hmap_file} {json_file}", shell=True, check=True)
        if retcode.returncode != 0:
            raise Exception(f"请确认 {hmap_file} 是否存在!")

        mapping, private_headers = {}, os.path.join(self.__pods_root, "Headers/Private")
        with open(json_file, "r") as f:

            raw_data = json.load(f)
            
            def function(acc: dict, key: str) -> dict:
                relpath = os.path.relpath(raw_data[key]["prefix"], private_headers)
                acc[key] = relpath.split("/")[0]
                return acc

            mapping = reduce(function, raw_data, {})

        return mapping

    @property
    def dependency(self) -> Dependency:
        return self.__dependency