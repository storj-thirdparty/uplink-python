# pylint: disable=missing-docstring, broad-except
import subprocess
import os
import sys
import platform
import setuptools
from setuptools.command.install import install

with open("README.md", "r") as fh:
    long_description = fh.read()


class Install(install):

    @staticmethod
    def find_module_path():
        for paths in sys.path:
            if os.path.isdir(paths) and "site-packages" in os.listdir(paths):
                new_path = os.path.join(paths, "site-packages", "uplink_python")
                try:
                    os.makedirs(new_path, exist_ok=True)
                    os.system("echo Directory uplink_python created successfully.")
                except OSError as error:
                    os.system("echo Error in creating uplink_python directory. Error: "+str(error))
                return new_path
        return ""

    def run(self):
        install.run(self)
        try:
            install_path = self.find_module_path()
            os.system("echo Package installation path: "+install_path)
            os.system("echo Building libuplinkc.so")
            copy_command = "copy" if platform.system() == "Windows" else "cp"
            command = "git clone https://github.com/storj/uplink-c && cd uplink-c" \
                      "&& go build -o libuplinkc.so " \
                      "-buildmode=c-shared && " + copy_command + " *.so " + install_path
            build_so = subprocess.Popen(command,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, shell=True)
            output, errors = build_so.communicate()
            build_so.wait()
            if output is not None:
                os.system("echo "+output.decode('utf-8'))
                os.system("echo Building libuplinkc.so successful.")
            if errors is not None:
                os.system("echo "+errors.decode('utf-8'))
                os.system("echo Building libuplinkc.so failed.")

        except Exception as error:
            os.system("echo " + str(error))
            os.system("echo Building libuplinkc.so failed.")


setuptools.setup(
    name="uplink-python",
    version="1.0.3",
    author="Utropicmedia",
    author_email="development@utropicmedia.com",
    license='Apache Software License',
    description="Python-native language binding for storj-uplink-c to"
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
    cmdclass={
        'install': Install,
    }
)
