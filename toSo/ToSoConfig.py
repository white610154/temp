"""
toSoFolder: str = Want to package into the folder path of .so/pyd file
excepts: Dict = Do not package folder's name or file's name
copyOther: Dict = Copy others file or not
delC: bool = Delete .c file or not
includeBaseFolder: bool = Base path's file pack or not

"""
from typing import Dict

excepts: Dict = {
    'folder': ['__pycache__','.git', 'test', 'toSo', 'sample', 'assets', 'datasets', 'deploy', 'logs', 'projects'],
    'file' : ['.gitignore'],
    'type': ['.pyc', '.pyd', '.sh'],
}

copyOther: Dict ={
    'folder' : ['data', 'const'], 
    'file' : ['test.txt'],
    'type' : ['.py']
}

delC: bool = True
buildDir: str = "build"
buildTmpDir: str = buildDir + "/temp"
toSoFolder: str = '.'
includeBaseFolder: bool = False 
