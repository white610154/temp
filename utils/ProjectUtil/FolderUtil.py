import os
import shutil
from typing import List

def __subfolder(folder, layers):
    ans: dict = folder
    for layer in layers:
        children: List[dict] = ans.get('children')
        if children == None:
            break
        for i, child in enumerate(children):
            if child.get('name') == layer:
                ans = children[i]
                break
        else:
            return None
    return ans

def list_folder(root):
    rel = lambda path: os.path.relpath(path, root) # find relative path under root
    folder: dict = {'name': rel(root), 'children': []}
    for dir, subdirs, _ in os.walk(root):
        layers = dir.split('/')
        sub = __subfolder(folder, layers[1:])
        if sub == None:
            return None

        sub['fullpath'] = rel(dir)
        if len(subdirs) > 0:
            sub['children'] = [
                {'name': subdir}
                for subdir in subdirs
            ]
    return folder['children']

def create_folder(root, dir) -> bool:
    if os.path.isdir(root):
        path = os.path.join(root, dir)
        if not os.path.isdir(path):
            os.mkdir(path)
            return True
    return False

def rename_folder(root, src, dst) -> bool:
    src = os.path.join(root, src)
    dst = os.path.join(root, dst)
    if os.path.isdir(src) and not os.path.isdir(dst):
        os.rename(src, dst)
        return True
    return False

def remove_folder(root, dir) -> bool:
    path = os.path.join(root, dir)
    if os.path.isdir(path):
        shutil.rmtree(path)
        return True
    return False
