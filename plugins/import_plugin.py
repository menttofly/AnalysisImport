#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import re

from cocoapods.sandbox import PodsSandbox
from .plugin import Plugin

class ImportPlugin(Plugin):

    def __init__(self, sanbox: PodsSandbox):
        self.sanbox = sanbox

    def process(self, pod: str, input_file: str):
        """
        un-namespced #import => namespced #import
        """
        headers = self.sanbox.module_headers[pod]

        def namespaced(imported: re.Match) -> str:
            if imported[1] in headers: 
                return imported.group()
             
            # un-namspced 替换为 namespaced
            if namespaced := self.sanbox.namespaced_headers.get(imported[1]):
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