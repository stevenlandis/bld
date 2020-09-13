import sys
import os
import re
import argparse

fcnPattern = re.compile(r'^def\s+(\w[\w\d]*)\s*\(\s*\):\s*$', re.MULTILINE)

def main():
  if not os.path.isfile('build.py'):
    print('build.py file not found')

  parser = argparse.ArgumentParser(description='Build a project')
  parser.add_argument(
    'command', type=str, nargs='?',
    help='function from build.py to run')
  parser.add_argument(
    '-l', '--list', action='store_true',
    help='list available functions in build.py')
  args = parser.parse_args()
  if args.list:
    print('listing contents')
    with open('build.py','r') as f:
      ftxt = f.read()
    print('Functions in build.py:')
    for name in re.findall(fcnPattern, ftxt):
      print(f' - {name}()')
  elif args.command != None:
    runCmd(args.command)
  else:
    runCmd('main')

def runCmd(cmd):
  print(f'Running {cmd}()')
  with open('build.py','r') as f:
    ftxt = f.read()
  tempGlobals = globals().copy()
  del tempGlobals['main']
  del tempGlobals['sys']
  del tempGlobals['os']
  del tempGlobals['__file__']
  del tempGlobals['__name__']
  exec(ftxt, tempGlobals)

  if cmd in tempGlobals:
    tempGlobals[cmd]()
  else:
    print(f'Unable to find {cmd}() in build.py')

main()
