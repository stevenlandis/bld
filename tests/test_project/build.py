import bld

def foo():
  print('running foo')

def bar():
  print('running bar')

def main():
  f = bld.File('test.txt')
  f.write('stuff and things')
  bld.copy(bld.File('copy_source.txt'), bld.File('copy_dest.txt'))

def clean():
  bld.File('copy_dest.txt').delete()
