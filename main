#!/usr/bin/python3
# -*-coding:utf-8-*-

__author__ = "zhengqi"

import os, re

from ios_system import iOSSystem
from header_paths import HeaderPaths
from dependency_analyzer import DependencyAnalyzer

class FileRefsAnalyzer:
    """
    分析某个组件及其依赖的 Development Pods，生成 podspec dependency 补全、非法 import 的报告
    """
    def __init__(self, path: str):
        self.analyzer = DependencyAnalyzer(
            "/Users/menttofly/Desktop/Gaoding-iOS/apps/fc_ios/FireCat/Podfile.lock"
        )
        self.store = HeaderPaths(
            "~/Desktop/Gaoding-iOS/apps/fc_ios/FireCat/Pods/Headers/Public"
        )
        self.system = iOSSystem()
        self.root_path = os.path.expanduser(path)
        self.root_pod = os.path.basename(path)
    
    def analyze(self):
        self.analyzer.analyze()

        files = self.list_all_files(self.root_path)

        refs, illegal_imports = set(), []
        for file_path in files:
            with open(file_path) as file:
                lines = file.readlines()

                for i in range(len(lines)):
                    line = lines[i]
                    rex = re.match(r'#import\s["<](\S+)([">])', line)
                    if not rex: continue

                    ref = self.find_refs(file_path, rex.group(1), rex.group(2) != ">")
                    if ref:
                        refs.add(ref)
                    else:
                        illegal_imports.append({
                            "file": file_path,
                            "line": (i + 1),
                            "message": line
                        })

        # 排除系统库，当前库
        refs.difference_update(self.system.sdks)
        refs.remove(self.root_pod) if self.root_pod in refs else None
        refs.difference_update(self.analyzer.all_dependencies[self.root_pod])

        print("All Done!")
    
    def find_refs(self, file: str, header: str, is_quote: bool) -> str or None:
        """
        筛选：合法依赖，非法依赖（自定义 header search paths，通过 header map 引用）
        """
        # 命中组件内自己的 Header Search Paths
        # eg. "${PODS_ROOT}/Headers/Private/AFNetworking"
        self_headers = self.store.header_paths[self.root_pod]
        if header in self_headers: 
            return self.root_pod

        # 引号导包，命中相对路径的搜索规则
        refs = os.path.join(os.path.dirname(file), header)
        if is_quote and os.path.exists(refs): 
            return self.root_pod
        
        # 设定了 header_dir，通过 header_dir 上级目录访问其它组件 .h
        # Header Search Paths 合法依赖 
        ref = self.store.headers_mapping.get(header)
        if ref == "XVImagePicker":
            print("")
        if ref: return ref

        parts = header.split("/", 1)
        if len(parts) > 1:
            # 非 header_dir 规则命中的
            ref = self.store.headers_mapping.get(parts[1])
            if ref: 
                return ref 
            if parts[0] in self.system.sdks:
                return parts[0]


    def list_all_files(self, directory: str) -> list[str]:
        """
        返回指定目录下的所有 .{.h,m} 文件
        """
        res = []
        for root, dir, files in os.walk(directory):
            if root.startswith("."): 
                continue
            if os.path.basename(root) == "Example": 
                dir[:] = [] # 忽略当前目录下的子目录
                continue

            for file in files:
                if file.endswith('.h') or file.endswith('.m'):
                    res.append(os.path.join(root, file))

        return res


if __name__ == "__main__":

    analyzer = FileRefsAnalyzer("~/Desktop/Gaoding-iOS/modules/GDMVideoTemplateUI")
    analyzer.analyze()


