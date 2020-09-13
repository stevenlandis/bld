from .Dir import File, Dir
from os.path import isfile, isdir, exists, join
INF = float('inf')

builtFiles = set()

def syncFiles(prevFilesPath):
  prevFiles = File(prevFilesPath)

  # delete old files
  if prevFiles.exists():
    for line in prevFiles.lines():
      line = line.strip()
      if line == '': continue
      f = File(line)
      if f.abspath not in builtFiles:
        print(f'deleting "{f.path}"')
        f.delete()
      parDir = f.parent()
      if parDir.isEmpty():
        parDir.delete()

  # save new files
  prevFiles.write('\n'.join(builtFiles) + '\n')

def getObj(path):
  if type(path) == File: return path
  if type(path) == Dir: return path
  if type(path) != str: assert(False)
  elif isfile(path): return File(path)
  elif isdir(path): return Dir(path)
  assert(False)

def getFile(path):
  if type(path) == File: return path
  assert(type(path) == str)
  assert(isfile(path) or not exists(path))
  return File(path)

def getDir(path):
  if type(path) == Dir: return path
  assert(type(path) == str)
  assert(isdir(path) or not exists(path))
  return Dir(path)

def needsUpdate(sources, results):
  if type(sources) != list:
    sources = [sources]
  if type(results) != list:
    results= [results]

  sources = [getFile(x) for x in sources]
  results = [getFile(x) for x in results]

  # always run when no results (such as running an executable)
  if len(results) == 0: return True

  resultTime = INF
  for file in results:
    builtFiles.add(file.abspath)
    time = file.getTime()
    # always run when a result doesn't exist
    if time == None: return True
    resultTime = min(resultTime, time);

  sourceTime = -INF
  for file in sources:
    if type(file) is str:
        file = File(file)
    time = file.getTime()
    # sources have to exist
    if time == None:
        raise Exception(f'Error: file "{file.name}" does not exist.')
    sourceTime = max(sourceTime, time)

  return sourceTime >= resultTime

def copyFile(f1, f2):
  f1 = getFile(f1)
  f2 = getFile(f2)
  assert(f1.exists())
  if needsUpdate(f1, f2):
    print(f'Copying "{f1.path}" -> "{f2.path}"')
    f2.writeBytes(f1.readBytes())

def copyDir(d1, d2):
  d1 = getDir(d1)
  d2 = getDir(d2)
  assert(d1.exists())
  for f in d1.files():
    relFPath = f.abspath[len(d1.abspath)+1:]
    copyFile(f, join(d2.abspath, relFPath))
  for d in d1.dirs():
    relDPath = d.abspath[len(d1.abspath)+1:]
    copyDir(d, join(d2.abspath, relDPath))

def copy(o1, o2):
  o1 = getObj(o1)
  if type(o1) == File:
    copyFile(o1, o2)
  else:
    copyDir(o1, o2)
