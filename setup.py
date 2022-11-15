# pylint: disable=missing-docstring, broad-except
import subprocess
import os
import platform
import sysconfig
import sys

from distutils.errors import CompileError
from subprocess import call

import setuptools
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

with open("README.md", "r") as fh:
    long_description = fh.read()

uplinkc_version = "v1.2.2"

class build_go_ext(build_ext):
    """Custom command to build extension from Go source files"""
    def build_extension(self, ext):

        print("os.name                      ",  os.name)
        print("sys.platform                 ",  sys.platform)
        print("platform.system()            ",  platform.system())
        print("sysconfig.get_platform()     ",  sysconfig.get_platform())
        print("platform.machine()           ",  platform.machine())
        print("platform.architecture()      ",  platform.architecture())
        print("platform.python      ",  platform.python_version())
        print("BUILDING EXT FOR ", platform.release(), " ---- ",platform.machine())

        ext_path = self.get_ext_fullpath(ext.name)
        print("ext path = ", ext_path)
        cmd = ['rm', '-rf', './uplink-c']
        out = call(cmd)
        if out != 0:
            raise CompileError('Go build failed')
        cmd = ['git', 'clone', 'https://github.com/storj/uplink-c']
        out = call(cmd)
        if out != 0:
            raise CompileError('Go build failed')
        os.chdir('./uplink-c')
        cmd = ['/usr/bin/go/bin/go', 'build', '-buildmode=c-shared', '-o', '../'+ext_path]#, "."]
        out = call(cmd)
        os.chdir('..')
        if out != 0:
            raise CompileError('Go build failed')


setuptools.setup(
    name="uplink-python",
    version="1.2.2.0",
    author="Utropicmedia",
    author_email="development@utropicmedia.com",
    license='Apache Software License',
    description="Python-native language binding for uplink to "
                "communicate with the Storj network.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/storj-thirdparty/uplink-python",
    packages=['uplink_python'],
    install_requires=['wheel'],
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
    ],
    python_requires='>=3.4',
    ext_modules=[
        Extension('libuplinkc', [])
    ],
    cmdclass={
        'build_ext': build_go_ext,
    }
)
