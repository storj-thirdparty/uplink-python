# storj-python binding 
### *Developed using libuplinkc v0.28.4*

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
$ python get-pip.py
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

* To include uplinkPython in you project, import the library, by using following command:
```
from storjPython.uplinkPython import *
```
* Create an object of ```libUplinkPy``` class to access all the functions of library. Please refer the sample *HelloStorj.py* file, for example.
```
variable_name = libUplinkPy()
```

## Sample Hello Storj!

File *helloStorj.py* can be found in folder where Python package was installed.

The sample *helloStorj.py* code calls the *uplinkPython.py* file and imports the *libUplinkPy* binding class to do the following:
* list all buckets in a Storj project
* create a new bucket (if it does not exist) within desired Storj project
* write a file from local computer to the a Storj bucket
* read back the object from the Storj bucket to local system for verification
* list all objects in a bucket
* delete bucket from a Storj project
* create shareable Scope key using API key and Encryption PassPhrase
* retrieving information from shareable Scope key for storj access
* delete object from a bucket using created scope key


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

### serialize_api_key(long)
    * function to serialize API key
    * pre-requisites: None
    * inputs: API key Handle (long)
    * outputs: Serialized Api Key (string), Error (string) if any else None

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
	
### create_bucket(long, string, obj)
    * function to create new bucket in Storj project
    * pre-requisites: open_project() function has been already called
	* inputs: Project Handle (long), Bucket Name (string), Bucket Config (obj) 
    * outputs: Bucket Info Handle (long), Error (string) if any else None
   * **Note:** To set Bucket Config Refer: [BucketConfig](https://godoc.org/storj.io/storj/lib/uplink#BucketConfig)

### get_encryption_access(long, string)
    * function to get encryption access to upload and/or download data to/from Storj
    * pre-requisites: open_project() function has been already called
    * inputs: Project Handle (long), Encryption Pass Phrase (string)
    * outputs: Serialized Encryption Access (string), Error (string) if any else None
	
### open_bucket(long, string, string)
    * function to open an already existing bucket in Storj project
    * pre-requisites: get_encryption_access() function has been already called
    * inputs: Project Handle (long), Serialized Encryption Access (string), Bucket Name (string)
    * outputs: Bucket Handle (long), Error (string) if any else None
	
### close_bucket(long)
    * function to close currently opened Bucket
    * pre-requisites: open_bucket() function has been already called
    * inputs: Bucket Handle (long)
    * outputs: Error (string) if any else None
	
### delete_bucket(long, string)
    * function to delete a bucket (if bucket contains any Objects at time of deletion, they may be lost permanently)
    * pre-requisites: open_project() function has been already called, successfully
    * inputs: Storj Project Handle (long), Bucket Name (string)
    * output: Error (string) if any else None
	
### list_buckets(long, obj)
    * function to list all the buckets in a Storj project
    * pre-requisites: open_project() function has been already called
    * inputs: Project Handle (long), Bucket List Options (obj)
    * output: Bucket List (obj), Error (string) if any else None
   * **Note:** To set Bucket List Options Refer: [BucketListOptions](https://godoc.org/storj.io/storj/pkg/storj#BucketListOptions)

### free_bucket_list(obj)
    * function to free Bucket List pointer
    * pre-requisites: list_bucket() function has been already called
    * inputs: Bucket List (obj)
    * output: Error (string) if any else None
	
### delete_object(long, string)
    * function to delete an object in a bucket
    * pre-requisites: open_bucket() function has been already called, successfully
    * inputs: Bucket Handle (long), Object Path (string)
    * output: Error (string) if any else None
	
### list_objects(long, obj)
    * function to list all the objects in a bucket
    * pre-requisites: open_project() function has been already called
    * inputs: Bucket Handle (long), List Options (obj)
    * output: Bucket List (obj), Error (string) if any else None
   * **Note:** To set List Options Refer: [ListOptions](https://godoc.org/storj.io/storj/pkg/storj#BucketListOptions)

### free_list_objects(obj)
    * function to free Object List pointer
    * pre-requisites: list_objects() function has been already called
    * inputs: Object List (obj)
    * output: Error (string) if any else None
	
### upload(long, string, obj)
	* function to get uploader handle used to upload data to Storj (V3) bucket's path
    * pre-requisites: open_bucket() function has been already called
    * inputs: Bucket Handle (long), Storj Path/File Name (string) within the opened bucket, Upload Options (obj)
    * output: Uploader Handle (long), Error (string) if any else None
   * **Note:** To set Upload Options Refer: [UploadOptions](https://godoc.org/storj.io/storj/lib/uplink#Bucket)
	
### upload_write(long, LP_c_ubyte, int)
	* function to write data to Storj (V3) bucket's path
    * pre-requisites: upload() function has been already called
    * inputs: Uploader Handle (long), Data to upload (LP_c_ubyte), Size of data to upload (int)
    * output: Size of data uploaded (long), Error (string) if any else None
   * **Note:** The Data to upload (LP_c_ubyte) passed to function should be a ctypes char or uint8 pointer only. (Please refer the sample helloStorj.py file, for example.)
	
### upload_commit(long)
	* function to commit and finalize file for uploaded data to Storj (V3) bucket's path
    * pre-requisites: upload() function has been already called
    * inputs: Uploader Handle (long)
    * output: Error (string) if any else None
	
### download(long, string)
    * function to get downloader handle to download Storj (V3) object's data and store it on local computer
    * pre-requisites: open_bucket() function has been already called
    * inputs: Bucket Handle (long), Storj Path/File Name (string) within the opened bucket
    * output: Downloader Handle (long), Error (string) if any else None
	
### download_read(long, int)
    * function to read Storj (V3) object's data and return the data
    * pre-requisites: download() function has been already called
    * inputs: Downloader Handle (long), Length of data to download (int)
    * output: Data downloaded (LP_c_ubyte), Size of data downloaded (int), Error (string) if any else None
	
### download_close(long)
    * function to close downloader after completing the data read process
    * pre-requisites: download() function has been already called
    * inputs: Downloader Handle (long)
    * output: Error (string) if any else None

### new_scope(string, long, string)
    * function to create new Scope keyprocess
    * pre-requisites: parse_api_key() and get_encryption_access() functions have been already called
    * inputs: Satellite Address (string), Api Key Parsed Handle (long),  Serialized Encryption Access (string)
    * output: Scope Handle (long), Error (string) if any else None

### get_scope_satellite_address(long)
    * function to get satellite address from Parsed Scope key
    * pre-requisites: None
    * inputs: Scope Handle (long)
    * output: Satellite Address (string), Error (string) if any else None

### get_scope_api_key(long)
    * function to get API key from Parsed Scope key
    * pre-requisites: None
    * inputs: Scope Handle (long)
    * output: Parsed Api Key Handle (long), Error (string) if any else None

### get_scope_enc_access(long)
    * function to get Encryption Access from Parsed Scope key
    * pre-requisites: None
    * inputs: Scope Handle (long)
    * output: Serialized Encryption Access (string), Error (string) if any else None

### parse_scope(string)
    * function to get Parsed Scope key
    * pre-requisites: None
    * inputs: Serialized Scope Key (string)
    * output: Parsed Scope Key Handle (long), Error (string) if any else None

### serialize_scope(long)
    * function to get Serialized Scope Key
    * pre-requisites: None
    * inputs: Scope Handle (long)
    * output: Serialized Scope Key (string), Error (string) if any else None

### restrict_scope(long, obj, list)
    * function to restrict Scope key with the provided caveat and encryption restrictions
    * pre-requisites: none
    * inputs: Parsed Scope Key Handle (long), Caveat (obj), Encryption Restriction (list)
    * output: Restricted Scope Key Handle (long), Error (string) if any else None