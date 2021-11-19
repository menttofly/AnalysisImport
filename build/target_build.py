#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import os, heapq
from .build import Build, stage
from .file_build import File
from lazy import lazy_property
from functools import reduce

class TargetBuild(Build):
    """
    统计 target 下所有文件 build 数据
    """
    def __init__(self, build_dir: str):
        
        builds: list[Build] = []
        for root, _, files in os.walk(build_dir):
            for file in files:
                if not file.endswith(".json"): continue

                # leaf = FileBuild(os.path.join(root, file))
                leaf = File.from_build(os.path.join(root, file))
                builds.append(leaf)

        self.__build_files = builds
        self.__target_name = os.path.basename(build_dir).split(".")[0]
    
    @lazy_property
    def total_execute_compiler(self) -> float:
        return reduce(
            lambda acc, cur: acc + cur.total_execute_compiler, 
            self.__build_files, 0.0
        )

    @lazy_property
    def total_frontend(self) -> float:
        return reduce(
            lambda acc, cur: acc + cur.total_frontend, 
            self.__build_files, 0.0
        )

    @lazy_property
    def total_source(self) -> float:
        return reduce(
            lambda acc, cur: acc + cur.total_source, 
            self.__build_files, 0.0
        )

    @lazy_property
    def total_module_load(self) -> float:
        return reduce(
            lambda acc, cur: acc + cur.total_module_load, 
            self.__build_files, 0.0
        )

    @lazy_property
    def total_module_compile(self) -> float:
        return reduce(
            lambda acc, cur: acc + cur.total_module_compile, 
            self.__build_files, 0.0
        )

    @lazy_property
    def total_backend(self) -> float:
        return reduce(
            lambda acc, cur: acc + cur.total_backend, 
            self.__build_files, 0.0
        )

    @lazy_property
    def top_10_builds(self) -> list:
        """
        耗时前 10 的源文件
        """
        builds = heapq.nlargest(
            10, self.__build_files, 
            key=lambda build: build.total_execute_compiler
        )
        builds.sort(
            key=lambda x: x.total_execute_compiler, reverse=True
        )

        return [x.json_object for x in builds]

    @lazy_property
    def json_object(self) -> dict:

        trace_events = {
            stage.total_execute_compiler.value: self.total_execute_compiler,
            stage.total_frontend.value: self.total_frontend,
            stage.total_source.value: self.total_source,
            stage.total_module_load.value: self.total_module_load,
            stage.total_module_compile.value: self.total_module_compile,
            stage.total_backend.value: self.total_backend,
        }
        return {
            "build_target": self.__target_name,
            "trace_events": trace_events,
            "top_10_builds": self.top_10_builds,
        }    