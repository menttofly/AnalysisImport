#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import json, os, heapq
from .build import Build, stages, stages_reversed
from dataclasses import dataclass, fields
from functools import reduce, cached_property

@dataclass
class File(Build):
    """
    解析单个文件 build 数据
    """
    @classmethod
    def from_file(self, json_file: str) -> Build:
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

    @cached_property
    def json_object(self) -> dict:

        stage_details = {
            stages[field.name]: round(getattr(self, field.name) / 1000.0, 3) 
            for field in fields(Build) if field.name in stages
        }
        return {
            "task": self.context,
            "compile_duration": self.total_execute_compiler,
            "stage_details": stage_details
        }

@dataclass
class Target(Build):
    """
    统计 target 下所有文件 build 数据
    """
    @classmethod
    def from_dir(self, target_dir: str) -> Build:
        """
        提取 target 目录所有 json
        """
        dependencies: list[Build] = []
        for root, _, files in os.walk(target_dir):
            for file in files:
                
                if not file.endswith(".json"): continue
                leaf = File.from_file(os.path.join(root, file))
                dependencies.append(leaf)

        def fuction(acc: dict, x: Build) -> dict:
            return {
                field.name: (acc.get(field.name, 0.0) + getattr(x, field.name)) 
                for field in fields(Build) if field.name in stages
            }

        kwargs = reduce(fuction, dependencies, {})
        kwargs = {k: round(v / 1000.0, 3) for k, v in kwargs.items()}

        kwargs["context"] = os.path.basename(target_dir).split(".")[0]
        kwargs["dependencies"] = dependencies

        return Target(**kwargs)

    @cached_property
    def top_ten(self) -> list[Build]:
        """
        耗时前 10 的源文件
        """
        return heapq.nlargest(
            10, self.dependencies, 
            key=lambda x: x.total_execute_compiler
        )

    @cached_property
    def json_object(self) -> dict:

        stage_details = {
            stages[field.name]: getattr(self, field.name) 
            for field in fields(Build) if field.name in stages
        }
        return {
            "module": self.context,
            "compile_duration": self.total_execute_compiler,
            "stage_details": stage_details,
            "top_ten": [
                x.json_object for x in self.top_ten
            ],
        }    

@dataclass
class Pods(Build):
    """
    汇总 Pods 目录下所有 target
    """
    @classmethod
    def from_scheme(self, project: str):
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

            target = Target.from_dir(os.path.join(project_dir, path))
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
        kwargs["context"] = project
        
        return Pods(**kwargs)

    @cached_property
    def top_ten(self) -> list[Build]:
        """
        耗时前 10 的 target
        """
        return sorted(
            self.dependencies, key=lambda x: x.total_execute_compiler, reverse=True
        )[0:10]

    @cached_property
    def json_object(self) -> dict:
        
        stage_details = {
            stages[field.name]: getattr(self, field.name) 
            for field in fields(Build) if field.name in stages
        }
        return {
            "project_name": self.context,
            "compile_duration": self.total_execute_compiler,
            "stage_details": stage_details,
            "top_ten": [x.json_object for x in self.top_ten],
        }