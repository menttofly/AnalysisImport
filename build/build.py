#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

from enum import Enum
from abc import ABC

class stage(Enum):
    """
    编译流程中各执行阶段
    """
    TOTAL_EXECUTE_COMPILER = "Total ExecuteCompiler"
    TOTAL_FRONTEND = "Total Frontend"
    TOTAL_SOURCE = "Total Source"
    TOTAL_MODULE_LOAD = "Total Module Load"
    TOTAL_MODULE_COMPILE = "Total Module Compile"
    TOTAL_BACKEND = "Total Backend"

stages = {
    stage.TOTAL_EXECUTE_COMPILER.value,
    stage.TOTAL_FRONTEND.value,
    stage.TOTAL_SOURCE.value,
    stage.TOTAL_MODULE_LOAD.value,
    stage.TOTAL_MODULE_COMPILE.value,
    stage.TOTAL_BACKEND.value,
}

class Build(ABC):
    """
    Build 组合抽象接口
    """
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