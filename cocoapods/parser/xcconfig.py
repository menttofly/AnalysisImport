#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import os, re
from cocoapods.lazy import lazy_property

class Xcconfig:
    """
    解析 xcconfig 文件
    """
    def __init__(self, path: str) -> None:
        self.__config_file = os.path.expanduser(path)

    @lazy_property
    def modulemaps(self) -> set[str]:
        """
        支持用 @import 引用已声明 module
        """
        other_c_flags = self.raw_configs["OTHER_CFLAGS"]
        if not other_c_flags: return None
            
        map_files = re.findall(r'-fmodule-map-file="(\S+)"', other_c_flags)
        return [
            os.path.basename(x[1]).splitext[0] for x in map_files
        ]

    @lazy_property
    def raw_configs(self) -> dict[str: str]:
        """
        提取所有的 raw 配置，并以字典形式存储
        """
        raw_configs = {}
        with open(self.__config_file) as file:
            for line in file.readlines():
                res = re.match(r"(\w+)\s=\s([^\n]+)", line)
                
                if not res: continue
                self.raw_configs[res[1]] = res[2]  

        return raw_configs     