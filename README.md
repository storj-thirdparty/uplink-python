# storj-python binding

## Initial Set-up

**NOTE**: for Golang

Make sure your `PATH` includes the `$GOPATH/bin` directory, so that your commands can be easily used [Refer: Install the Go Tools](https://golang.org/doc/install):
```
export PATH=$PATH:$GOPATH/bin
```

Install [storj-uplink](https://godoc.org/storj.io/storj/lib/uplink) go package, by running:
```
$ go get storj.io/storj/lib/uplink
```

**NOTE**: for Python 

Please ensure [pip](https://pypi.org/project/pip/) is installed on your system. If you have Python version 3.4 or later, pip is included by default.
```
python get-pip.py
```

Install [storjPython](https://pypi.org/project/storjPython/) python package, by running:
```
$ pip install storjPython
```

## Set-up Files

* After git cloning go package, using cmd/terminal, navigate to the ```$HOME/go/src/storj.io/storj/lib/uplinkc``` folder.

* Create '.so' file at  ```$HOME/go/src/storj.io/storj/lib/uplinkc``` folder, by using following command:
```
$ go build -o libuplinkc.so -buildmode=c-shared 
```

* Copy *libuplinkc.so* file into the folder, where Python package was installed



## Sample Hello Storj!

File *helloStorj.py* can be found in folder where Python package was installed.

The sample *helloStorj.py* code calls the *uplinkPython.py* file and imports the *libUplinkPy* binding class to do the following:
* create a new bucket (if it does not exist) within desired Storj project
* write a file from local computer to the a Storj bucket
* read back the object from the Storj bucket to local system for verification


## Storj-Python Binding Functions

**NOTE**: Every function consists of error response. Please use it, to check if the function call was successful or not. In case, if it is not *None*, then you may also show the error's text. Please refer the sample *HelloStorj.py* file, for example.

### new_uplink()
    * function to create new Storj uplink
    * pre-requisites: None
    * inputs: None
    * outputs: Uplink Handle (long), Error (string) if any else None
	
### close_uplink(long)
    * function to close currently opened uplink
    * pre-requisites: new_uplink() function has been already called
    * inputs: Uplink Handle (long)
    * outputs: Error (string) if any else None

### parse_api_key(string)
    * function to parse API key, to be used by Storj
    * pre-requisites: None
    * inputs: API key (string)
    * outputs: Parse Api Key Handle (long), Error (string) if any else None

### open_project(long, long, string)
    * function to open a Storj project
    * pre-requisites: new_uplink() and parse_api_key() functions have been already called
    * inputs: Uplink Handle (long), Api Key Parsed Handle (long), Satellite Address (string)
    * outputs: Project Handle (long), Error (string) if any else None
	
### close_project(long)
    * function to close currently opened Storj project
    * pre-requisites: open_project() function has been already called
    * inputs: Project Handle (long)
    * outputs: Error (string) if any else None

### get_encryption_access(long, string)
    * function to get encryption access to upload and/or download data to/from Storj
    * pre-requisites: open_project() function has been already called
    * inputs: Project Handle (long), Encryption Pass Phrase (string)
    * outputs: Serialized Encryption Access (char Ptr), Error (string) if any else None
	
### create_bucket(long, string, obj)
    * function to create new bucket in Storj project
    * pre-requisites: open_project() function has been already called
	* inputs: Project Handle (long), Bucket Name (string), Bucket Config (obj) 
    * outputs: Bucket Info Handle (long), Error (string) if any else None
   * **Note:** To set Bucket Config Refer: [BucketConfig](https://godoc.org/storj.io/storj/lib/uplink#BucketConfig)

### open_bucket(long, charPtr, string)
    * function to open an already existing bucket in Storj project
    * pre-requisites: get_encryption_access() function has been already called
    * inputs: Project Handle (long), Serialized Encryption Access (char Ptr), Bucket Name (string)
    * outputs: Bucket Handle (long), Error (string) if any else None
	
### close_bucket(long)
    * function to close currently opened Bucket
    * pre-requisites: open_bucket() function has been already called
    * inputs: Bucket Handle (long)
    * outputs: Error (string) if any else None
	
### upload_file(long, string, string)
	* function to upload data from local system to Storj (V3) bucket's path
    * pre-requisites: open_bucket() function has been already called
    * inputs: Bucket Handle (long), Storj Path/File Name (string) within the opened bucket, local Source Full File Name (string)
    * outputs: True if successful else False, Error (string) if any else None
	
### download_file(long, string, string)
    * function to download Storj (V3) object's data and store it in given file on local computer
    * pre-requisites: open_bucket() function has been already called
    * inputs: Bucket Handle (long), Storj Path/File Name (string) within the opened bucket, local Destination Full Path Name(string)
    * outputs: True if successful else False, Error (string) if any else None
