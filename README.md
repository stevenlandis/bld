This is a package for building projects.

# Overview

There are a few ways to use this package:
- as a library for manipulating files and directories
- as a library for building projects
- as a command line tool for running your project

# Install instructions

1. Clone this repo somewhere on your computer and open in a terminal.
2. Run `python setup.py install`. (or `python3 setup.py install` depending on how you want to set it up).
3. To make sure it's installed, go to another directory and run `python -m bld` which should print `build.py file not found` to the screen.

# Usage instructions

At the root of your project, add a file `build.py` which will contain a bunch of functions related to your project.

A common structure looks like:
```py
import bld

def main():
  # the default build command
  print('built the project')

def clean():
  # remove built files
  print('clean the project')
```

Running `python -m bld` in the root directory of your project will run `main()` from `build.py` and print out "built the project".

Alternatively, if you don't want to use `python -m bld`, you can always run `python build.py` after sticking the following code at the bottom of `build.py`:
```py
if __name__ == '__main__':
  main()
```

Running `python -m bld clean` will run `clean()` making it easy to write different commands for managing your project.

Now let's say your project has a `hello.c` file:

```c
#include <stdio.h>
int main() {
   printf("Hello, World!");
   return 0;
}
```

And you want to compile it using bld. If you were using make, you would write:
```Makefile
a.out: hello.c
  gcc hello.c
```

Using bld, this translates to:
```py
def main():
  if bld.shouldUpdate(bld.File('hello.c'), bld.File('a.out')):
    bld.call('gcc hello.c')
```

While this is more verbose than make, you can leverage all the programming constructs in python such as functions and classes to make building files easier and clearer:
```py
def compileC(inFile, outFile):
  if bld.shouldUpdate(inFile, outFile):
    bld.call(f'gcc {inFile.path} -o {outFile.path}')

def main():
  compileC(bld.File('hello.c'), bld.File('hello'))
```
