from genericpath import isdir, isfile
import os, time
from distutils.core import setup
from Cython.Build import cythonize
import ToSoConfig
from os.path import join, abspath, isfile, isdir, splitext
from PackToSoFunc import except_thing, copy_thing, copy_other, special_case, filter_list


def get_py_list(basepath= abspath('.'), parentpath='', name=''):
    fullpath =  join(basepath, parentpath, name)
    for fileName in os.listdir(fullpath):
        ffile =  join(fullpath, fileName)
        if not except_thing(fileName):
            if isdir(ffile):
                for f in get_py_list(basepath,  join(parentpath, name), fileName):
                    yield f
            elif isfile(ffile):
                ext = splitext(fileName)[1]
                if ext in ('.py') and not fileName.startswith('.'):
                    yield  join(parentpath, name, fileName)
                elif ext in ('.c') and ToSoConfig.delC:
                    os.remove(ffile)
            else:
                pass

def getPyNotBasePath(basepath=abspath('.')):
    
    for fname in os.listdir(basepath):
        ffile = join(basepath, fname)
        if not except_thing(fname):
            if copy_thing(fname):
                copy_other(fname)
            elif isdir(ffile):
                for f in get_py_list(basepath, fname):
                    yield f
                state, filePath = special_case(ffile)
                if state:
                    tempList = []
                    filePath = filePath.replace(f'{ToSoConfig.toSoFolder}/','')
                    newList = list(get_py_list(basepath= filePath))
                    for i in range(len(newList)): 
                        tempList.append(join(filePath,newList[i]))
                    specialDict[filePath] = tempList    

specialDict = {}
def PackToSo():
    
    starttime = time.time()

    if ToSoConfig.includeBaseFolder:        
        packPathList = list(get_py_list(basepath=ToSoConfig.toSoFolder))
    else:
        packPathList = list(getPyNotBasePath(basepath=ToSoConfig.toSoFolder))
    print(f'packPathList: {packPathList}')

    print(f'specialDict: {specialDict.keys()}')
    try:
        for i in specialDict.keys():
            packPathList  = list(filter_list(packPathList, specialDict[i]))
            print(f"{i} : {specialDict[i]}")
            setup(ext_modules = cythonize(specialDict[i], compiler_directives={'language_level' : "4"}),
                script_args=["build_ext", "-b", join(ToSoConfig.buildDir, i), "-t", ToSoConfig.buildTmpDir])

    except Exception as ex:
        print("error! ", ex)

    print(f'OtherList: {packPathList}')
    try:
        setup(ext_modules = cythonize(packPathList, compiler_directives={'language_level' : "3"}),
            script_args=["build_ext", "-b", ToSoConfig.buildDir, "-t", ToSoConfig.buildTmpDir])
    except Exception as ex:
        print("error! ", ex)
    list(get_py_list(basepath=ToSoConfig.toSoFolder))
    print("complate! time:", time.time()-starttime, 's')
