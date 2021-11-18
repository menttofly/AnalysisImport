#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import os, json
from build.pods_build import PodsBuild

if __name__ == "__main__":

    workspace = "ModuleTest"
    
    builder = PodsBuild(workspace)
    build_info = builder.json_object

    build_json_name = f"{workspace}-build-time-trace.json"
    print(f"生成 {build_json_name}..")
    with open(os.path.join(os.path.dirname(__file__), build_json_name), "w+") as file:
        try:
            json_str = json.dumps(build_info, indent=4)
            file.write(json_str)
        except Exception as e:
            print(f"生成json数据异常：<{str(e)}>")
        else:
            pass
    
    print("Done!!!")