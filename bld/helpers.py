from os.path import isfile, isdir, join, getmtime, abspath, split
from os import mkdir
import subprocess

INF = float('infinity')

class linesGen:
    def __init__(self,path):
        self.path = path
        self.file = None
    def __iter__(self): return self
    def __next__(self):
        if self.file == None:
            self.file = open(self.path,'r')
        try:
            return next(self.file)
        except:
            self.file.close()
            self.file = None
            raise StopIteration()

def call(cmd):
    print(f'> {cmd}')
    subprocess.run(cmd, shell=True)

def splitFName(name):
    dotI = name.find('.')
    if dotI == -1: return (name, '')
    else: return (name[:dotI], name[dotI+1:])

def makeDir(path):
    if isdir(path): return
    path = abspath(path)
    parentDir,_ = split(path)
    makeDir(parentDir)
    mkdir(path)

def getPathList(path):
    if type(path) == list: return path
    return normpath(path).split(sep)

def getAllFiles(dirPath):
    paths = [join(dirPath,f) for f in listdir(dirPath)]
    fPaths = [p for p in paths if isfile(p)]
    dPaths = [p for p in paths if isdir(p)]
    for dPath in dPaths:
        for fPath in getAllFiles(dPaths):
            fPaths.append(fPath)
    return fPaths

