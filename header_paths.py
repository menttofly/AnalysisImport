#!/usr/bin/python3
# -*-coding:utf-8-*-

import os

class HeaderPaths:
    """
    获取 "${PODS_ROOT}/Headers/Public" 目录下所有的 .h 文件
    """
    def __init__(self, path: str):

        self.header_paths = {}
        self.headers_mapping = {}
        self.parse_all_headers(os.path.expanduser(path))

    
    def parse_all_headers(self, header_root):
        """
        解析 Headers 下所有头文件
        """
        for x in os.listdir(header_root):
            if x.startswith("."): continue

            paths, mapping = self.fetch_pod_headers(os.path.join(header_root, x))
            self.header_paths[x] = paths
            
            # 合并不同模块的字典，不重写已有 key
            for k, v in mapping.items():
                if not self.headers_mapping.get(k):
                    self.headers_mapping[k] = v
                else:
                    print(f"发现重名头文件：{k}")

        print("")

    
    def fetch_pod_headers(self, header_dir: str) -> tuple[set, dict]:
        """
        获取指定组件下的所有 .h 文件相对路径
        """
        header_paths, header_mapping = set(), {}

        for root, _, files in os.walk(header_dir):
            for file in files:
                # 与 header_dir 之间的相对路径
                if header_dir != root:
                    file = os.path.join(os.path.relpath(root, header_dir), file)
                
                header_paths.add(file)
                header_mapping[file] = os.path.basename(header_dir)
                # if os.path.islink(os.path.join(root, file)):
                #     real_path = os.readlink(os.path.join(root, file))
                #     real_path = os.path.abspath(real_path)
                
        return header_paths, header_mapping

