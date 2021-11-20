#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import os, heapq
from .build import Build, stage, stages
from .file_build import File
from lazy import lazy_property
from functools import reduce
from dataclasses import dataclass, fields

@dataclass
class Target(Build):
    """
    统计 target 下所有文件 build 数据
    """
    @classmethod
    def from_build(self, target_dir: str) -> Build:
        """
        提取 target 目录所有 json
        """
        dependencies: list[Build] = []
        for root, _, files in os.walk(target_dir):
            for file in files:
                
                if not file.endswith(".json"): continue
                leaf = File.from_build(os.path.join(root, file))
                dependencies.append(leaf)

        def fuction(acc: dict, x: Build) -> dict:
            return {
                field.name: (acc.get(field.name, 0.0) + getattr(x, field.name)) 
                for field in fields(Target) if field.name in stages
            }

        kwargs = reduce(fuction, dependencies, {})
        kwargs = {k: round(v / 1000.0, 3) for k, v in kwargs.items()}

        kwargs["context"] = os.path.basename(target_dir).split(".")[0]
        kwargs["dependencies"] = dependencies

        return Target(**kwargs)

    @lazy_property
    def top_10_builds(self) -> list[Build]:
        """
        耗时前 10 的源文件
        """
        return heapq.nlargest(
            10, self.dependencies, 
            key=lambda x: x.total_execute_compiler
        )

    @lazy_property
    def json_object(self) -> dict:

        trace_events = {
            stages[field.name]: getattr(self, field.name) 
            for field in fields(Build) if field.name in stages
        }
        return {
            "build_target": self.context,
            "trace_events": trace_events,
            "top_10_builds": [
                x.json_object for x in self.top_10_builds
            ],
        }    