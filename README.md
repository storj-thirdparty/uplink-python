# storj-python binding

## Initial Set-up

**NOTE**: For Golang

    Make sure your `PATH` includes the `$GOPATH/bin` directory, so that your commands can be easily used [Refer: Install the Go Tools](https://golang.org/doc/install):
    ```
    export PATH=$PATH:$GOPATH/bin
    ```

    Install [storj-uplink](https://godoc.org/storj.io/storj/lib/uplink) go package, by running:
    ```
    $ go get storj.io/storj/lib/uplink
    ```

**NOTE**: For Python 

    * Please ensure the following modules are installed on your system.
	1. ctypes
    ```
    $ pip install ctypes
    ```


## Set-up Files

* After git cloning this project, store *libuplinkc_custom.go* file within ```$HOME/go/src/storj.io/storj/lib/uplinkc``` folder

* Using cmd/terminal, navigate to the ```$HOME/go/src/storj.io/storj/lib/uplinkc``` folder.

* Create '.so' file at  ```$HOME/go/src/storj.io/storj/lib/uplinkc``` folder, by using following command:
```
$ go build -o libuplinkc.so -buildmode=c-shared 
```

* Copy *libuplinkc.so* file into the folder, where Python project was cloned



## Sample Hello Storj!
The sample *HelloStorj.py* code calls the *UplinkPython.py* file and import *libUplinkPy* binding class to do the following:
    * create a new bucket within desired Storj project
    * write a file from local computer to the created Storj bucket
    * read back the object from the Storj bucket to local PC for verification


## Python-Storj Binding Functions

**NOTE**: After calling a function, please ensure that the function returned True, before using it further. Please refer the sample *HelloStorj.py* file for example.

### new_uplink()
    * function to create new Storj uplink
    * pre-requisites: None
    * inputs: None
    * output: True/False

### parse_api_key(string)
    * function to parse API key, to be used by Storj
    * pre-requisites: None
    * inputs: API key (string)
    * output: True/False

### open_project(string)
    * function to open a Storj project
    * pre-requisites: new_uplink() and parse_api_key() functions have been already called
    * inputs: Satellite Address (string)
    * output: True/False

### get_encryption_access(string)
    * function to get encryption access to upload and download data on Storj
    * pre-requisites: open_project() function has been already called
    * inputs: Encryption Pass Phrase (string)
    * output: True/False

### open_bucket(string)
    * function to open an already existing bucket in Storj project
    * pre-requisites: get_encryption_access() function has been already called
    * inputs: Bucket Name (string)
    * output: True/False

### upload(string, string)
    * function to upload data from srcFullFileName (at local computer) to Storj (V3) bucket's path
    * pre-requisites: open_bucket() function has been already called
    * inputs: Storj Path/File Name (string) within the opened bucket, local Source Full File Name(string)
    * output: True/False

### download(string, string)
    * function to download Storj (V3) object's data and store it in given file with destFullFileName (on local computer)
    * pre-requisites: open_bucket() function has been already called
    * inputs: Storj Path/File Name (string) within the opened bucket, local Destination Full Path Name(string)
    * output: True/False

### create_bucket(string)
    * function to create new bucket in Storj project
    * pre-requisites: open_project() function has been already called
    * inputs: Bucket Name (string)
    * output: True/False

### close_uplink()
    * function to close currently opened uplink
    * pre-requisites: new_uplink() function has been already called
    * inputs: none
    * output: True/False

### close_project()
    * function to close currently opened Storj project
    * pre-requisites: open_project() function has been already called
    * inputs: none
    * output: True/False

### close_bucket()
    * function to close currently opened Bucket
    * pre-requisites: open_bucket() function has been already called
    * inputs: none
    * output: True/False
