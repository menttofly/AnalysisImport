#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

from enum import Enum
from abc import ABC, abstractclassmethod
from typing import Any

class stage(Enum):
    """
    编译流程中各执行阶段
    """
    total_execute_compiler = "Total ExecuteCompiler"
    total_frontend = "Total Frontend"
    total_source = "Total Source"
    total_module_load = "Total Module Load"
    total_module_compile = "Total Module Compile"
    total_backend = "Total Backend"

stages = { e.name: e.value for e in stage }
stages_reversed = { e.value: e.name for e in stage }

class Build(ABC):
    """
    Build 组合抽象接口
    """
    @property
    def context(self) -> str:
        """
        构建的上下文
        """
        pass

    @property
    def total_execute_compiler(self) -> float:
        """
        编译总时长
        """
        pass
    
    @property 
    def total_frontend(self) -> float:
        """
        前端总时长
        """
        pass

    @property 
    def total_source(self) -> float:
        """
        头文件处理总时长
        """
        pass

    @property
    def total_module_load(self) -> float:
        """
        Module 加载总时长
        """
        pass

    @property
    def total_module_compile(self) -> float:
        """
        Module 编译总时长
        """
        pass

    @property 
    def total_backend(self) -> float:
        """
        后端总时长
        """
        pass

    @property 
    def top_10_builds(self) -> list:
        """
        耗时前 10 的任务
        """
        pass

    @property 
    def json_object(self) -> dict:
        """
        json 形式表示 build 数据
        """
        pass