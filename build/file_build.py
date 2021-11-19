#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import json, os
from .build import Build, stage, stages
from lazy import lazy_property
from dataclasses import dataclass

# @dataclass
class FileBuild(Build):
    """
    解析单个文件 build 数据
    """
    def __init__(self, json_file: str):
        
        with open(json_file) as f:
            data, raw_trace = json.load(f), {}

            for item in data.get("traceEvents", []):
                if "dur" not in item.keys(): continue
                raw_trace[item["name"]] = round(item["dur"] / 1000.0, 3)

            self.__raw_trace = raw_trace
            self.__file_name = os.path.splitext(os.path.basename(json_file))[0] + ".o"

    @property
    def total_execute_compiler(self) -> float:
        return self.__raw_trace.get(stage.TOTAL_EXECUTE_COMPILER.value, 0.0)

    @property
    def total_frontend(self) -> float:
        return self.__raw_trace.get(stage.TOTAL_FRONTEND.value, 0.0)

    @property
    def total_source(self) -> float:
        return self.__raw_trace.get(stage.TOTAL_SOURCE.value, 0.0)

    @property
    def total_module_load(self) -> float:
        return self.__raw_trace.get(stage.TOTAL_MODULE_LOAD.value, 0.0)

    @property
    def total_module_compile(self) -> float:
        return self.__raw_trace.get(stage.TOTAL_MODULE_COMPILE.value, 0.0)

    @property
    def total_backend(self) -> float:
        return self.__raw_trace.get(stage.TOTAL_BACKEND.value, 0.0)

    @property
    def top_10_builds(self) -> list:
        pass

    @lazy_property
    def json_object(self) -> dict[str: float]:

        trace_events = { 
            k: v for k, v in self.__raw_trace.items() if k in stages
        }
        return {
            "build_file": self.__file_name,
            "trace_events": trace_events
        }