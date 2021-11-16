#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import fileinput, sys, re

from cocoapods.sandbox import PodsSandbox
from .plugin import Plugin

class ImportPlugin(Plugin):

    def __init__(self, sanbox: PodsSandbox):
        self.sanbox = sanbox

    def process(self, pod: str, input_file: str):
        """
        替换未带命名空间 #import
        """
        pod_headers = self.sanbox.module_headers[pod]
        

        def namespaced(imported: re.Match) -> str:
            if imported[1] in pod_headers: 
                return imported.group()
             
            # un-namspced 替换为 namespaced
            if namespaced := self.sanbox.namespaced_headers.get(imported[1]):
                return f"#import <{namespaced}>"
            else:
                return imported.group()

        with open(input_file, "r+") as file:
            content = file.read()
            content = re.sub(
                r'#import\s"([^\/\s\n]+\.h)"', namespaced, content
            )
            
            file.seek(0)
            file.truncate()
            file.write(content)

        # for line in fileinput.input(input_file, inplace=True):
        #     imported = re.match(r'#import\s"([^\/\s\n]+\.h)"', line)
            
        #     if not imported: continue
        #     if imported[1] in self_headers: continue

        #     # un-namspced 替换为 namespaced
        #     if namespaced := self.sanbox.namespaced_headers.get(imported[1]):
        #         sys.stdout.write(f"# import <{namespaced}>")

        print("")

    def ouput(self) -> str:
        pass