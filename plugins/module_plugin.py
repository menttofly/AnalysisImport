#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import os, re
from .plugin import Plugin
from cocoapods.sandbox import PodsSandbox

class ModulePlugin(Plugin):
    """
    自动替换 #import => @import
    """
    def __init__(self, sanbox: PodsSandbox):
        self.sanbox = sanbox

    def process(self, pod: str, input_file: str):
        if input_file.endswith(".mm"): 
            return

        modulemaps = self.sanbox.pod_modulemaps.get(pod, set())
        
        def function(imported: re.Match) -> str:

            for importe in [f"{imported[1]}/{imported[2]}", imported[2]]:
                if not self.sanbox.headers_to_module.get(importe):
                    continue
                
                module, pod_name = self.sanbox.headers_to_module.get(importe)
                if pod_name == pod:
                    return imported.group()
                
                if pod_name and pod_name in modulemaps:
                    return f"@import {module};"

            return imported.group()

        with open(input_file, "r+") as f:
            contents = f.read()
            contents = re.sub(
                r'#import\s["<](\w+)\/(\S+.[hp]+)[">]', function, contents
            )
            
            f.seek(0)
            f.truncate()
            f.write(contents)
    
    def ouput(self) -> str:
        pass