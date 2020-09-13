import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name='bld',
  version='0.0.1',
  # scripts=['src/bld.py'],
  author="Steven Landis",
  author_email="stevenlandis@comcast.net",
  description="A project building library and script",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/stevenlandis/bld",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
 )

# %USERPROFILE%\Google Drive\core\Programming\bld
# python setup.py bdist_wheel
