from os.path import abspath, split, isdir, join, isfile, getmtime
from .helpers import splitFName, linesGen, makeDir, getAllFiles
from os import listdir, rmdir, mkdir, remove

class File:
    def __init__(self, path):
        self.path = path
        self.baseDir, self.name = split(path)
        self.abspath = abspath(path)
        self.title, self.type = splitFName(self.name)
    def exists(self):
        return isfile(self.path)
    def parent(self):
        parentDir,_ = split(self.abspath)
        return Dir(parentDir)
    def read(self):
        with open(self.path, 'r') as f: return f.read()
    def readBytes(self):
        with open(self.path, 'rb') as f: return f.read()
    def lines(self):
        with open(self.path, 'r') as f:
            lines = [line for line in f]
        return lines
    def write(self,txt):
        parentDir,_ = split(self.abspath)
        makeDir(parentDir)
        with open(self.path,'w') as f: f.write(txt)
    def writeBytes(self,content):
        parentDir,_ = split(self.abspath)
        makeDir(parentDir)
        with open(self.path,'wb') as f: f.write(content)
    def delete(self): remove(self.path)
    def getTime(self):
        if not self.exists(): return None
        try: return getmtime(self.path)
        except: return None

class Dir:
    def __init__(self, path):
        self.path = path
        self.abspath = abspath(path)
        _,self.name = split(self.abspath)
    def exists(self):
        return isdir(self.path)
    def isEmpty(self):
        return len(listdir(self.path)) == 0
    def files(self):
        paths = [join(self.path,f) for f in listdir(self.path)]
        paths = [f for f in paths if isfile(f)]
        return [File(p) for p in paths]
    def dirs(self):
        paths = [join(self.path,f) for f in listdir(self.path)]
        paths = [f for f in paths if isdir(f)]
        return [Dir(p) for p in paths]
    def allFiles(self):
        return getAllFiles(self.path)
    def getDir(self, relPath):
        return Dir(join(self.abspath, relPath))
    def getFile(self, relPath):
        return File(join(self.abspath, relPath))
    def delete(self):
        for f in self.files(): f.delete()
        for d in self.dirs(): d.delete()
        # wait until files are actually deleted
        # needed b/c windows is a shitty os
        while len(listdir(self.path)) != 0:
            pass
        rmdir(self.path)
    def make(self):
        if not self.exists(): mkdir(self.path)
    def pathTo(obj):
        assert(type(obj) == Dir or type(obj) == File)
        assert(obj.abspath.startswith(self.abspath))
        return obj.abspath[len(self.abspath):]
