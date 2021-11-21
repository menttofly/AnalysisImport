#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import json, os
from .build import Build, stages, stages_reversed
from lazy import lazy_property
from dataclasses import dataclass, fields
from functools import reduce

@dataclass
class File(Build):
    """
    解析单个文件 build 数据
    """
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
            kwargs = reduce(
                fuction, json.load(f).get("traceEvents", []), {}
            )
            kwargs["context"] = os.path.splitext(
                os.path.basename(json_file)
            )[0] + ".o"

            return File(**kwargs)

    @lazy_property
    def top_10_builds(self) -> list[Build]:
        pass

    @lazy_property
    def json_object(self) -> dict:

        trace_events = {
            stages[field.name]: round(getattr(self, field.name) / 1000.0, 3) 
            for field in fields(Build) if field.name in stages
        }
        return {
            "build_file": self.context,
            "trace_events": trace_events
        }
