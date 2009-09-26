#!/usr/bin/env python

import sys
import os
try:
    import subprocess
    has_subprocess = True
except:
    has_subprocess = False
import shutil

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup
from setuptools import Feature
from distutils.cmd import Command
from distutils.command.build_ext import build_ext
from distutils.errors import CCompilerError
from distutils.errors import DistutilsPlatformError, DistutilsExecError
from distutils.core import Extension

requirements = []
try:
    import xml.etree.ElementTree
except ImportError:
    requirements.append("elementtree")


if sys.platform == 'win32' and sys.version_info > (2, 6):
   # 2.6's distutils.msvc9compiler can raise an IOError when failing to
   # find the compiler
   build_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError,
                 IOError)
else:
   build_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError)


class custom_build_ext(build_ext):
    """Allow C extension building to fail.

    The C extension speeds up BSON encoding, but is not essential.
    """

    warning_message = """
**************************************************************
WARNING: %s could not
be compiled. No C extensions are essential for PyMongo to run,
although they do result in significant speed improvements.

%s
**************************************************************
"""

    def run(self):
        try:
            build_ext.run(self)
        except DistutilsPlatformError, e:
            print e
            print self.warning_message % ("Extension modules",
                                          "There was an issue with your "
                                          "platform configuration - see above.")

    def build_extension(self, ext):
        if sys.version_info[:3] >= (2, 4, 0):
            try:
                build_ext.build_extension(self, ext)
            except build_errors:
                print self.warning_message % ("The %s extension module" % ext.name,
                                              "Above is the ouput showing how "
                                              "the compilation failed.")
        else:
            print self.warning_message % ("The %s extension module" % ext.name,
                                          "Please use Python >= 2.4 to take "
                                          "advantage of the extension.")

c_ext = Feature(
    "optional C extension",
    standard=True,
    ext_modules=[Extension('pymonga._pymongo._cbson', ['pymonga/_pymongo/_cbsonmodule.c'])])

if "--no_ext" in sys.argv:
    sys.argv = [x for x in sys.argv if x != "--no_ext"]
    features = {}
else:
    features = {"c-ext": c_ext}

setup(
    name="pymonga",
    version="0.2",
    description="Python driver for MongoDB <http://www.mongodb.org>",
    long_description="bla bla",
    author="Alexandre Fiori",
    author_email="mongodb-user@googlegroups.com",
    url="http://github.com/mongodb/mongo-python-driver",
    keywords=["mongo", "mongodb", "pymongo", "gridfs", "pymonga"],
    packages=["pymonga", "pymonga._pymongo"],
    install_requires=requirements,
    features=features,
    license="Apache License, Version 2.0",
    test_suite="nose.collector",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Database"],
    cmdclass={"build_ext": custom_build_ext,
              "doc": "bla bla"})
