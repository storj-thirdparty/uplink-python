# <b>uplink-python binding</b>

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/aaee609406154b1794061386bb0ca60e)](https://app.codacy.com/gh/storj-thirdparty/uplink-python?utm_source=github.com&utm_medium=referral&utm_content=storj-thirdparty/uplink-python&utm_campaign=Badge_Grade_Dashboard)

> Developed using v1.0.5 storj/uplink-c

## <b>Initial Set-up (Important)</b>

> NOTE: For Golang
>
>Make sure your `PATH` includes the `$GOPATH/bin` directory, so that your commands can be easily used [Refer: Install the Go Tools](https://golang.org/doc/install):
>```
>export PATH=$PATH:$GOPATH/bin
>```
>
>Depending on your operating system, you will need to install:
>
>**On Unix**
>* A proper C/C++ compiler toolchain, like [GCC](https://gcc.gnu.org/)
>
>**On macOS**
>* [Xcode](https://developer.apple.com/xcode/download/) : You also need to install the XCode Command Line Tools by running xcode-select --install. Alternatively, if you already have the full Xcode installed, you can find them under the menu Xcode -> Open Developer Tool -> More Developer Tools.... This step will install clang, clang++, and make.
>
>**On Windows**
>* Install Visual C++ Build Environment: [Visual Studio Build Tools](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools) (using "Visual C++ build tools" workload) or [Visual Studio 2017 Community](https://visualstudio.microsoft.com/pl/thank-you-downloading-visual-studio/?sku=Community) (using the "Desktop development with C++" workload)
>* Make sure you have access to ```site-packages``` folder inside the directory where python is installed. To do this navigate to the directory where python is installed, if you get an error "Permission Denied", follow the instruction in message box and allow access using ```security tab```.

## <b>Binding Set-up</b>


Please ensure you have Python 3.x and [pip](https://pypi.org/project/pip/) installed on your system. If you have Python version 3.4 or later, pip is included by default. uplink-python does not support Python 2.x.
```
$ python get-pip.py
```

### Option 1

Install [uplink-python](https://pypi.org/project/uplink-python/) python package with ```--no-cache-dir``` tag if re-installing or upgrading from previous version, otherwise tag can be ignored (using Terminal/Powershell/CMD as ```Administrator```):
```
$ pip install --no-cache-dir uplink-python
```

### Option 2

Follow these steps to set-up binding manually or if ```libuplinkc.so``` fails to build using Option 1.

Install [uplink-python](https://pypi.org/project/uplink-python/) python package (using Terminal/Powershell/CMD) if not already done in ```Option 1```
```
$ pip install uplink-python
```

Install [storj-uplink-c](https://godoc.org/storj.io/storj/lib/uplink) go package, by running:
```
$ go get storj.io/uplink-c
```

* After git cloning go package, using cmd/terminal, navigate to the ```$HOME/go/src/storj.io/uplink-c``` folder.

* Create '.so' file at  ```$HOME/go/src/storj.io/uplink-c``` folder, by using following command:
```
$ go build -o libuplinkc.so -buildmode=c-shared
```

* Copy created *libuplinkc.so* file into the folder, where Python package was installed (python3.X ```->``` site-packages ```->``` uplink_python)


## <b>Project Set-up</b>

To include uplink in you project, import the library, by using following command:
```
from uplink_python.uplink import LibUplinkPy, c
```
Create an object of ```LibUplinkPy``` class to access all the functions of library. Please refer the sample *hello_storj.py* file, for example.
```
variable_name = LibUplinkPy()
```

To use various structures such as ListBucketsOptions, ListObjectsOptions, Permissions, etc you would require to import them first from their respective classes i.e. uplink and exchange.
```
from uplink_python.exchange import DownloadOptions
from uplink_python.uplink import ListObjectsOptions, Permission
```

## <b>Sample Hello Storj</b>

File *hello_storj.py* can be found in folder where Python package was installed.

The sample *hello_storj.py* code calls the *uplink.py* file and imports the *LibUplinkPy* binding class to do the following:
* list all buckets in a Storj project
* create a new bucket (if it does not exist) within desired Storj project
* write a file from local computer to the a Storj bucket
* read back the object from the Storj bucket to local system for verification
* list all objects in a bucket
* delete bucket from a Storj project
* create shareable Access with permissions and shared prefix.
* list all buckets and objects with permission to shareable access.


## <b>Flow Diagram</b>

[Flow Diagram](/_images/arch.drawio.png ':include :type=iframe width=100% height=1000px')