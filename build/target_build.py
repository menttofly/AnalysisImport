#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import os, heapq
from .build import Build, stage
from .file_build import FileBuild
from lazy import lazy_property
from functools import reduce

class TargetBuild(Build):
    """
    统计 target 下所有文件 build 数据
    """
    def __init__(self, build_dir: str):
        
        builds: list[FileBuild] = []
        for root, _, files in os.walk(build_dir):
            for file in files:
                if not file.endswith(".json"): continue

                leaf = FileBuild(os.path.join(root, file))
                builds.append(leaf)

        self.__file_builds = builds
        self.__target_name = os.path.basename(build_dir).split(".")[0]
    
    @lazy_property
    def total_execute_compiler(self) -> float:
        return reduce(
            lambda acc, cur: acc + cur.total_execute_compiler, 
            self.__file_builds, 0.0
        )

    @lazy_property
    def total_frontend(self) -> float:
        return reduce(
            lambda acc, cur: acc + cur.total_frontend, 
            self.__file_builds, 0.0
        )

    @lazy_property
    def total_source(self) -> float:
        return reduce(
            lambda acc, cur: acc + cur.total_source, 
            self.__file_builds, 0.0
        )

    @lazy_property
    def total_module_load(self) -> float:
        return reduce(
            lambda acc, cur: acc + cur.total_module_load, 
            self.__file_builds, 0.0
        )

    @lazy_property
    def total_module_compile(self) -> float:
        return reduce(
            lambda acc, cur: acc + cur.total_module_compile, 
            self.__file_builds, 0.0
        )

    @lazy_property
    def total_backend(self) -> float:
        return reduce(
            lambda acc, cur: acc + cur.total_backend, 
            self.__file_builds, 0.0
        )

    @lazy_property
    def top_10_builds(self) -> list:
        """
        耗时前 10 的源文件
        """
        builds = heapq.nlargest(
            10, self.__file_builds, 
            key=lambda build: build.total_execute_compiler
        )
        builds.sort(
            key=lambda x: x.total_execute_compiler, reverse=True
        )

        return [x.json_object for x in builds]

    @lazy_property
    def json_object(self) -> dict:

        trace_events = {
            stage.TOTAL_EXECUTE_COMPILER.value: self.total_execute_compiler,
            stage.TOTAL_FRONTEND.value: self.total_frontend,
            stage.TOTAL_SOURCE.value: self.total_source,
            stage.TOTAL_MODULE_LOAD.value: self.total_module_load,
            stage.TOTAL_MODULE_COMPILE.value: self.total_module_compile,
            stage.TOTAL_BACKEND.value: self.total_backend,
        }
        return {
            "build_target": self.__target_name,
            "trace_events": trace_events,
            "top_10_builds": self.top_10_builds,
        }    