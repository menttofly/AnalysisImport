#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import os
from .build import Build, stages
from .target_build import Target
from lazy import lazy_property
from functools import reduce
from dataclasses import dataclass, fields

@dataclass
class Pods(Build):
    """
    汇总 Pods 目录下所有 target
    """
    @classmethod
    def from_build(self, project: str):
        """
        获取 project 下所有构建数据
        """
        derived_data_path = os.path.expanduser("~/Library/Developer/Xcode/DerivedData")
        projects = [x for x in os.listdir(derived_data_path) if x.startswith(f"{project}-")]

        if len(projects) != 1:
            raise Exception("没有符合条件的构建!")

        project_dir = os.path.join(derived_data_path, f"{projects[0]}/Build/Intermediates.noindex")
        dependencies: list[Build] = []

        for path in os.listdir(project_dir):
            if not path.endswith(".build") or path.startswith("Pods."):
                continue

            target = Target.from_build(os.path.join(project_dir, path))
            dependencies.append(target)  

        def fuction(acc: dict, x: Build) -> dict:
            """
            reduce 迭代器
            """
            return {
                field.name: (acc.get(field.name, 0.0) + getattr(x, field.name)) 
                for field in fields(Target) if field.name in stages
            }

        kwargs = reduce(fuction, dependencies, {})
        kwargs = {k: round(v, 3) for k, v in kwargs.items()}
        kwargs["dependencies"] = dependencies
        
        return Pods(**kwargs)

    @lazy_property
    def top_10_builds(self) -> list[Build]:
        """
        耗时前 10 的 target
        """
        return sorted(
            self.dependencies, key=lambda x: x.total_execute_compiler, reverse=True
        )[0:10]

    @lazy_property
    def json_object(self) -> dict:
        
        trace_events = {
            stages[field.name]: getattr(self, field.name) 
            for field in fields(Build) if field.name in stages
        }
        return {
            "trace_events": trace_events,
            "top_10_builds": [x.json_object for x in self.top_10_builds],
        }