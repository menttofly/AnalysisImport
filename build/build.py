#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

from enum import Enum
from dataclasses import dataclass, field

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

@dataclass
class Build:
    """
    Build 结果抽象
    """
    context: str = ""                  # 构建的上下文
    dependencies: list = field(default_factory=list) # 所有子任务
    
    total_execute_compiler: float = 0  # 编译总时长
    total_frontend:         float = 0  # 前端总时长
    total_source:           float = 0  # 头文件处理总时长
    total_module_load:      float = 0  # Module 加载总时长
    total_module_compile:   float = 0  # Module 编译总时长
    total_backend:          float = 0  # 后端总时长

    @property 
    def top_ten(self) -> list:
        """
        耗时排名前 10 任务
        """
        pass

    @property 
    def json_object(self) -> dict:
        """
        json 形式展示构建数据
        """
        pass