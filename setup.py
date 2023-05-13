# pylint: disable=missing-docstring, broad-except
import os
import platform
import subprocess
import sys
import sysconfig

import setuptools
from setuptools.command.install import install

with open("README.md", "r") as fh:
    long_description = fh.read()

uplinkc_version = "v1.2.2"


class Install(install):
    @staticmethod
    def find_module_path():
        new_path = os.path.join(sysconfig.get_paths()["purelib"], "uplink_python")
        try:
            os.makedirs(new_path, exist_ok=True)
            os.system("echo Directory uplink_python created successfully.")
        except OSError as error:
            os.system("echo Error in creating uplink_python directory. Error: " + str(error))
        return new_path

    def run(self):
        try:
            install_path = self.find_module_path()
            print("Package installation path: " + install_path)
            print("Building libuplinkc.so")
            copy_command = "copy" if platform.system() == "Windows" else "cp"
            command = (
                f"git clone -c advice.detachedHead=false -b {uplinkc_version} https://github.com/storj/uplink-c"
                f"&& cd uplink-c && go build -o libuplinkc.so -buildmode=c-shared"
                f"&& {copy_command}  *.so {install_path}"
            )
            build_so = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            output, errors = build_so.communicate()
            build_so.wait()
            if output:
                print(output.decode("utf-8"))
                print("Building libuplinkc.so successful.")
            if errors:
                print(errors.decode("utf-8"))
                print("Building libuplinkc.so failed.")
            if build_so.returncode != 0:
                sys.exit(1)
        except Exception as error:
            print("Building libuplinkc.so failed: " + str(error))

        install.run(self)


setuptools.setup(
    name="uplink-python",
    version="1.2.2.0",
    author="Utropicmedia",
    author_email="development@utropicmedia.com",
    license="Apache Software License",
    description="Python-native language binding for uplink to " "communicate with the Storj network.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/storj-thirdparty/uplink-python",
    packages=["uplink_python"],
    install_requires=["wheel"],
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
    ],
    python_requires=">=3.4",
    cmdclass={
        "install": Install,
    },
)
