#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import os

from .build import Build, stage
from .target_build import TargetBuild
from lazy import lazy_property
from functools import reduce

class PodsBuild(Build):
    """
    汇总 Pods 目录下所有 target
    """
    def __init__(self, project: str):
        derived_data_path = os.path.expanduser("~/Library/Developer/Xcode/DerivedData")
        
        projects = [x for x in os.listdir(derived_data_path) if x.startswith(f"{project}-")]
        if len(projects) != 1:
            raise Exception("没有符合条件的构建!")

        build_targets_dir = os.path.join(derived_data_path, f"{projects[0]}/Build/Intermediates.noindex")
        build_targets: list[TargetBuild] = []

        for path in os.listdir(build_targets_dir):
            if not path.endswith(".build") or path.startswith("Pods."):
                continue

            target_build = TargetBuild(os.path.join(build_targets_dir, path))
            build_targets.append(target_build)  

        self.__build_targets = build_targets

    @lazy_property
    def total_execute_compiler(self) -> float:
        return reduce(
            lambda acc, cur: acc + cur.total_execute_compiler, 
            self.__build_targets, 0.0
        )
    
    @lazy_property
    def total_frontend(self) -> float:
        return reduce(
            lambda acc, cur: acc + cur.total_frontend, 
            self.__build_targets, 0.0
        )

    @lazy_property
    def total_source(self) -> float:
        return reduce(
            lambda acc, cur: acc + cur.total_source, 
            self.__build_targets, 0.0
        )

    @lazy_property
    def total_module_load(self) -> float:
        return reduce(
            lambda acc, cur: acc + cur.total_module_load, 
            self.__build_targets, 0.0
        )

    @lazy_property
    def total_module_compile(self) -> float:
        return reduce(
            lambda acc, cur: acc + cur.total_module_compile, 
            self.__build_targets, 0.0
        )

    @lazy_property
    def total_backend(self) -> float:
        return reduce(
            lambda acc, cur: acc + cur.total_backend, 
            self.__build_targets, 0.0
        )

    @lazy_property
    def top_10_builds(self) -> list:
        """
        耗时前 10 的 target
        """
        builds = sorted(self.__build_targets, key=lambda x: x.total_execute_compiler, reverse=True)
        builds = builds[0:10]

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
            "trace_events": trace_events,
            "top_10_builds": self.top_10_builds,
            # "build_targets": [x.json_object for x in self.__build_targets]
        }

    
                

            
            
            


    