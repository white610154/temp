from genericpath import isdir, isfile
import os, shutil, time
from distutils.core import setup
from Cython.Build import cythonize
import ToSoConfig
from os.path import join, abspath, isfile, isdir, splitext , exists

def except_thing(fname):
    if fname in ToSoConfig.excepts['file']: return True

    if fname in ToSoConfig.excepts['folder']: return True

    if splitext(fname)[1] in ToSoConfig.excepts['type']: return True
        
    if fname == ToSoConfig.buildDir: return True
    
    if fname.startswith('.'): return True
        
    return False

def copy_thing(fname):
    if fname in ToSoConfig.copyOther['file']:  return True

    if fname in ToSoConfig.copyOther['folder']: return True

    if splitext(fname)[1] in ToSoConfig.copyOther['type']: return True
        
    return False


def copy_other(fname):
    '''
    copy file, folder, and what tpye from ToSoConfig.copyOther 
    '''
    dstdir = join(ToSoConfig.toSoFolder, ToSoConfig.buildDir)
    if fname in ToSoConfig.copyOther['folder']:
        shutil.copytree(join(ToSoConfig.toSoFolder, fname),  join(dstdir, fname))

    if splitext(fname)[1] in ToSoConfig.copyOther['type']:
        if not isdir(dstdir): os.makedirs(dstdir)
        shutil.copyfile(join(ToSoConfig.toSoFolder, fname), join(dstdir, fname))


def filter_list(full_list, excludes):
    '''
        Filter parameters in `excludes` from `full_list`
    '''
    s = set(excludes)
    return (x for x in full_list if x not in s)

def special_case(folderName):
    _countAllFile = 0
    _countAllPy = 0
    
    fileNumber = len(os.listdir(folderName))
    
    for fileName in os.listdir(folderName):
        
        if not except_thing(fileName):
            if isdir(join(folderName, fileName)) or splitext(fileName)[1] not in ['.py'] :
                _countAllFile += 1

            elif fileName.endswith('.c') and ToSoConfig.delC:
                os.remove(join(folderName, fileName))
                
            elif splitext(fileName)[1] in ['.py'] :
                _countAllPy += 1

        elif fileName == '__pycache__':
            _countAllFile += 1
            _countAllPy += 1

    if _countAllFile == fileNumber or _countAllPy == fileNumber:
        return True, folderName

    return False, None
