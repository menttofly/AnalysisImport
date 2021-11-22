#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import re

from .plugin import Plugin
from cocoapods.sandbox import PodsSandbox

class ImportPlugin(Plugin):
    """
    修复未带命名空间的 import
    """
    def __init__(self, sanbox: PodsSandbox):
        self.sanbox = sanbox

    def process(self, pod: str, input_file: str):
        """
        un-namespced #import => namespced #import
        """
        headers = self.sanbox.pod_headers[pod]

        def namespaced(imported: re.Match) -> str:
            if imported[1] in headers: 
                return imported.group()
             
            # un-namspced 替换为 namespaced
            if namespaced := self.sanbox.pod_namespaced_headers.get(imported[1]):
                return f"#import <{namespaced}>"
            else:
                return imported.group()

        with open(input_file, "r+") as f:
            contents = f.read()
            contents = re.sub(
                r'#import\s"([^\/\s\n]+\.h)"', namespaced, contents
            )
            
            f.seek(0)
            f.truncate()
            f.write(contents)

    def ouput(self) -> str:
        pass