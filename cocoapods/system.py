#!/usr/bin/python3
# -*-coding:utf-8-*-

import os, re, subprocess
from sys import stdout

class iOSSystem:
    """
    获取 iOS 系统库
    """
    def __init__(self):
        self.list_all_frameworks(self.fetch_sdk_path())

        
    def fetch_sdk_path(self) -> str:
        """
        获取模拟器的 sdk 路径
        """
        res = subprocess.run(
            "xcrun --sdk iphonesimulator --show-sdk-path", 
            stdout=subprocess.PIPE,
            shell=True, 
            check=True
        )

        if res.returncode != 0: 
            raise Exception("未找到 iOS 系统库")

        path = res.stdout.decode(stdout.encoding)
        return os.path.join(
            path.strip(), 
            "System/Library/Frameworks"
        )

    def list_all_frameworks(self, path: str):
        """
        找出所有的系统库
        """
        if not os.path.exists(path):
            raise Exception("系统 sdk 目录不存在")

        sdks = set()
        for x in os.listdir(path):
            rex = re.match(r"(\w+).framework", x)
            if rex: 
                sdks.add(rex.group(1))
        
        self.sdks = sdks