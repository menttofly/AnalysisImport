#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import json, os
from .build import Build, stages, stages_reversed
from lazy import lazy_property
from dataclasses import dataclass, field, fields
from functools import reduce

@dataclass(frozen=True)
class File(Build):
    """
    解析单个文件 build 数据
    """
    context: str = ""
    
    total_execute_compiler: float = 0
    total_frontend:         float = 0
    total_source:           float = 0
    total_module_load:      float = 0
    total_module_compile:   float = 0
    total_backend:          float = 0

    @classmethod
    def from_build(self, json_file: str) -> Build:
        """
        从 json 文件初始化
        """
        def fuction(acc: dict, x: dict) -> dict:
            if x["name"] in stages_reversed:
                acc[stages_reversed[x["name"]]] = round(x["dur"] / 1000.0, 3)

            return acc

        with open(json_file) as f:
            object = reduce(
                fuction, json.load(f).get("traceEvents", []), {}
            )
            object["context"] = os.path.splitext(
                os.path.basename(json_file)
            )[0] + ".o"

            return File(**object)

    @property
    def top_10_builds(self) -> list:
        pass

    @lazy_property
    def json_object(self) -> dict[str: float]:

        trace_events = {
            stages[field.name]: getattr(self, field.name) for field in fields(File) if field.name in stages
        }
        return {
            "build_file": self.context,
            "trace_events": trace_events
        }