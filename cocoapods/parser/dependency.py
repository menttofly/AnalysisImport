#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import os, re
from datetime import datetime

class Dependency:
    """
    解析 Podfile.lock 文件，获取所有组件及其直接、间接依赖
    """
    def __init__(self, path: str) -> None:
        # {pod => dependencies} 
        self.__dependencies = {}
        self.__lock_file = os.path.expanduser(path)

    @property
    def pods(self):
        """
        返回当前所有的组件库
        """
        return self.__dependencies.keys()

    def dependencies(self, pod: str) -> set[str]:
        """
        获取某个组件的直接、间接依赖
        """
        return self.__dependencies.get(pod)

    def analyze(self):
        """
        主函数
        """
        begin = datetime.now()
        self.graph = self.__parse_lock_file()
        
        # 遍历所有顶点
        for vertex, _ in self.graph.items():
            res = set()
            self.__dfs(vertex, [], res); 
            res.remove(vertex) if vertex in res else None
            
            # 保存组件依赖关系
            self.__dependencies[vertex] = res

        # 清洗结果，合并 subspecs
        self.__purge_subspecs()
        print(
            f"{os.path.basename(self.__lock_file)} 依赖分析耗时: {(datetime.now() - begin).total_seconds()}s"
        )
        
    def __parse_lock_file(self) -> dict:
        """
        解析 Podfile.lock，创建邻接表用于表示依赖关系
        """
        if not os.path.exists(self.__lock_file):
            raise Exception(f"{self.__lock_file} 不存在!")

        # 邻接表
        graph = {}
        
        with open(self.__lock_file, "r") as file:
            res = re.match(r"PODS:\n([\s\S]+)\nDEPENDENCIES:", file.read())
            pre_adjacency = []

            # 从后向前遍历，子依赖提前计算
            for line in reversed(res.group(1).splitlines()):
                #'  - Action (4.2.0):', 提取 'Action'
                vertex = re.match(r"\s{2}-\s([\w\/\.-]+)\s\([\.\w-]+\)", line)
                #'    - RxCocoa (< 7.0, >= 5.0)', 提取 'RxCocoa'
                adjacency = re.match(r"\s{4}-\s([\w\/\.-]+)\s*", line)

                if vertex:
                    graph[vertex[1]] = pre_adjacency
                    pre_adjacency = []
                elif adjacency:
                    pre_adjacency.append(adjacency[1])

        return graph

    def __dfs(self, vertex: str, path: list[str], dependencies: set[str]):
        """
        深度优先遍历所有路径，取得 vertex 所有直接、间接依赖
        """
        # 已经计算过的 vertex 依赖项
        if counted := self.__dependencies.get(vertex):
            res = set(counted); res.add(vertex)
            dependencies.update(res)
            return

        path.append(vertex) 
        # 邻接顶点不存在，将当前路径加入依赖结果
        if len(self.graph.get(vertex, [])) == 0: 
            dependencies.update(set(path))
            path.pop()
            return

        # 遍历所有邻接顶点
        for adjacency in self.graph.get(vertex, []):
            self.__dfs(adjacency, path, dependencies)

        path.pop()

    def __purge_subspecs(self):
        """
        合并所有 subspecs 依赖
        """
        res = {}
        for vertex, dependencies in self.__dependencies.items():
            vertex = vertex.split("/")[0]
            # 过滤 YYKit -> YYKit/no-arc 这种 subspecs 依赖声明
            dependencies = {
                x.split("/")[0] for x in dependencies
            }
            dependencies = filter(
                lambda x: vertex not in x, 
                dependencies
            )

            if not res.get(vertex):
                res[vertex] = set() 
            res[vertex].update(set(dependencies)) 
        
        self.__dependencies = res