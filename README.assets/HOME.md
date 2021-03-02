## Flow Diagram

![](https://github.com/storj-thirdparty/uplink-python/blob/master/README.assets/arch.drawio.png)


## Binding Functions

>Note: All the functions, if unsuccessful, throw an exception that can be caught using the try-except block. For implementation, refer to *hello_storj.py*.

## *Uplink Functions*

### request_access_with_passphrase(satellite, api_key, passphrase)

#### Description:

This function request_access_with_passphrase  requests satellite for a new access grant using a passphrase, there are no pre-requisites required for this function.\
This function accepts 3 arguments Satellite URL, API Key, and encryption passphrase and returns an access object on successful execution which can be used to call other functions which are bound to it.\
An access grant is a serialized structure that is internally comprised of an 
API Key, a set of encryption key information, and information about which Satellite address is responsible for the metadata.\
An access grant is always associated with exactly one Project on one Satellite.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>satellite</code>| Storj V3 network satellite address | <code>string</code> |
|<code>api_key</code>| Storj V3 network API key |<code>string</code> |
|<code>passphrase</code>| Any passphrase |<code>string</code> |

#### Usage Example

```py
MY_API_KEY = "change-me-to-the-api-key-created-in-satellite-gui"
MY_SATELLITE = "12EayRS2V1kEsWESU9QMRseFhdxYxKicsiFmxrsLZHeLUtdps3S@us-central-1.tardigrade.io:7777"
MY_ENCRYPTION_PASSPHRASE = "you'll never guess this"

try:
    # create an object of Uplink class
    uplink = Uplink()

    # function calls
    # request access using passphrase
    print("\nRequesting Access using passphrase...")
    access = uplink.request_access_with_passphrase(MY_SATELLITE, MY_API_KEY, MY_ENCRYPTION_PASSPHRASE)
    ### some code ###
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### config_request_access_with_passphrase(config, satellite, api_key, passphrase)

#### Description:

This function config_request_access_with_passphrase requests satellite for a new access grant using a passphrase and config.\
There are no pre-requisites required for this function.\
This function accepts 4 arguments Satellite URL, API Key, encryption passphrase, and config object and returns an access object on successful execution which can be used to call other functions that are bound to it.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>config</code>| Create using uplink_python.module_classes | <code>object</code> |
|<code>satellite</code>|  Storj V3 network satellite address | <code>string</code> |
|<code>api_key</code>| Storj V3 network API key |<code>string</code> |
|<code>passphrase</code>| Any passphrase string |<code>string</code> |

#### Usage Example

```py
from uplink_python.module_classes import Config

MY_API_KEY = "change-me-to-the-api-key-created-in-satellite-gui"
MY_SATELLITE = "12EayRS2V1kEsWESU9QMRseFhdxYxKicsiFmxrsLZHeLUtdps3S@us-central-1.tardigrade.io:7777"
MY_ENCRYPTION_PASSPHRASE = "you'll never guess this"
config = Config()

try:
    # create an object of Uplink class
    uplink = Uplink()

    # function calls
    # request access using passphrase
    print("\nRequesting Access using passphrase...")
    access = uplink.config_request_access_with_passphrase(config, MY_SATELLITE, MY_API_KEY, MY_ENCRYPTION_PASSPHRASE)
    ### some code ###
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### parse_access(serialized_access)

#### Description:

parse_access function to parses serialized access grant string there are no pre-requisites required for this function.\
this function accepts one argument serialized access String which is returned by access_serialize function, it returns an access object on successful execution which can be used to call other functions which are bound to it.\
This should be the main way to instantiate an access grant for opening a project.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>serialized_access</code>| Serialized access string returned by access.serialize function | <code>string</code> |

#### Usage Example

```py
try:
    # some code
    shared_access = uplink.parse_access(serialized_access)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details) 
```

## *Access Functions*

### derive_encryption_key(passphrase, salt)

#### Description:

derive encryption key function derives a salted encryption key for passphrase using the salt, This function is useful for deriving a salted encryption key for users when implementing multitenancy in a single app bucket.
parse access function is required as a pre-requisite for this function.\
this function accepts 2 arguments passphrase(string) and salt(string).\
It throws an error if unsuccessful.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>passphrase</code>| Any passphrase string |<code>string</code> |
|<code>salt</code>| Any string used as salt |<code>string</code> |

#### Usage Example

```py
try:
    # create derive encryption key
    encryption_key = access.derive_encryption_key("new_passphrase", "salt")
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### override_encryption_key(bucket_name, prefix, encryption_key)

#### Description:

override encryption key function overrides the root encryption key for the prefix in bucket with encryptionKey. This function is useful for overriding the encryption key in user-specific access grants when implementing multitenancy in a single app bucket.
parse access function is required as a pre-requisite for this function.\
this function accepts 3 arguments bucket_name(string), prefix(string) and encryption_key(object). encryption_key can be obtained by using the function derive_encryption_key.\
It returns an access object on successful execution which can be used 
to call other functions that are bound to it.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket_name</code>| Bucket name on storj V3 network  |<code>string</code> |
|<code>prefix</code>| Path on storj V3 network |<code>string</code> |
|<code>encryption_key</code>| Obtained using function derive_encryption_key |<code>object</code> |

#### Usage Example

```py
try:
    # create derive encryption key
    encryption_key = access.derive_encryption_key("new_passphrase", "salt")
    #
    new_access = access.override_encryption_key(MY_BUCKET, MY_OBJECT, encryption_key)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### serialize()

#### Description:

serialize function serializes access grant into a string.\
parse access function is required as a pre-requisite for this function.
which is returned by access_share function.\
it returns a Serialized Access String on successful execution which is used to be as parse_access argument.

#### Usage Example

```py
try:
    # some code
    serialized_access = access.serialize()
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### share(permissions, shared_prefix)

#### Description:

share function creates a new access grant with specific permission. Permission will be applied to prefixes when defined.
parse access function is required as a pre-requisite for this function.\
this function accepts 2 arguments permissions(object) and shared_prefix(python list of dictionaries) which are accessible from uplink python module_classes.\
It returns an access object on successful execution which can be used 
to call other functions that are bound to it.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>permissions</code>| Create using uplink_python.module_classes |<code>object</code> |
|<code>shared_prefix</code>| Create using uplink_python.module_classes |<code>list of objects</code> |

#### Usage Example

```py
try:
    # set permissions for the new access to be created
    permissions = Permission(allow_list=True, allow_delete=False)
    
    # set shared prefix as list of dictionaries for the new access to be created
    shared_prefix = [SharePrefix(bucket=MY_BUCKET, prefix="")]
    
    # create new access
    new_access = access.share(permissions, shared_prefix)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### open_project()

#### Description:

Once you have a valid access grant, you can open a Project with the access that access grant, open_project function opens project using access grant.\
request_access_with_passphrase or config_request_access_with_passphrase function is required as a pre-requisite.\
it returns a project object on successful execution which can be used to call other functions which are bound to it.\
It allows you to manage buckets and objects within buckets.

#### Usage Example

```py
try:
    # some code
    project = access.open_project()
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### config_open_project(config)

#### Description:

config_open_project function opens a project using an access grant and config.\
request_access_with_passphrase or config_request_access_with_passphrase function
is required as a pre-requisite. This function accepts 1 argument config(object) which is accessible from uplink python module_classes.\
it returns a project object on successful execution which can be used to call other functions that are bound to it.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>config</code>| Create using uplink_python.module_classes | <code>object</code> |

#### Usage Example

```py
from uplink_python.module_classes import Config

config = Config()
try:
    # some code
    project = access.config_open_project(config)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

## *Project Functions*

### close()

#### Description:

close function closes the project and open_project function is required as a pre-requisite.\
it throws an error if unsuccessful.

#### Usage Example

```py
try:
    # some code
    project.close()
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### ensure_bucket(bucket_name)

#### Description:

ensure_bucket function creates a new bucket and ignores the error when it already exists and open_project function is required as a pre-requisite.\
This function accepts 1 argument bucket name.\
It returns a bucket object on successful execution it can be used to get other properties that are bound to it.

##### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket_name</code>| Bucket name on storj V3 network | <code>string</code> |

#### Usage Example

```py
MY_BUCKET = "my-first-bucket"
try:
    # some code
    _ = project.ensure_bucket(MY_BUCKET)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### stat_bucket(bucket_name)

#### Description:

stat_bucket function returns information about a bucket and open_project function is required as a pre-requisite.\
This function accepts 1 argument bucket name.\
it returns a bucket object on successful execution it can be used to get
other properties that are bound to it.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket_name</code>| Bucket name on storj V3 network | <code>string</code> |

#### Usage Example

```py
MY_BUCKET = "my-first-bucket"
try:
    # some code
    _ = project.stat_bucket(MY_BUCKET)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### create_bucket(bucket_name)

#### Description:

create_bucket function creates a new bucket whereas when bucket already exists it returns a valid Bucket and throws ErrBucketExists, open_project function is required as a pre-requisite.\
This function accepts 1 argument bucket name.\
It returns a bucket object on successful execution it can be 
used to get other properties that are bound to it.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket_name</code>|Bucket name on storj V3 network | <code>string</code> |

#### Usage Example

```py
MY_BUCKET = "my-first-bucket"
try:
    # some code
    _ = project.create_bucket(MY_BUCKET)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### list_buckets()

#### Description:

list_buckets function lists buckets and open_project function is required
as a pre-requisite for this function.\
This function takes 1 optional argument list_bucket_options which is accessed from module_classes.
It returns a list of Bucket objects on successful execution.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>list_bucket_options</code>| Create using uplink_python.module_classes | <code>object</code> |

#### Usage Example

```py
try:
    # some code
     bucket_list = project.list_buckets()
        for bucket in bucket_list:
            # as python class object
            print(bucket.name, " | ", datetime.fromtimestamp(bucket.created))
            # as python dictionary
            print(bucket.get_dict())
        print("Buckets listing: COMPLETE!")
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### delete_bucket(bucket_name)

#### Description:

delete_bucket function deletes a bucket while when bucket is not empty it throws ErrBucketNotEmpty, open_project function is required as a pre-requisite for this function .\
This function accepts 1 argument bucket name.\
It returns a bucket object on successful execution it can be used to get other properties that are bound to it.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket_name</code>| Bucket name on storj V3 network | <code>string</code> |

#### Usage Example

```py
MY_BUCKET = "my-first-bucket"
try:
    # some code
    
    try:
        bucket = project.delete_bucket(MY_BUCKET)
    # if delete bucket fails due to "not empty", delete all the objects and try again
    except BucketNotEmptyError as exception:
        print("Error while deleting bucket: ", exception.message)
        print("Deleting object's inside bucket and try to delete bucket again...")
        # list objects in given bucket recursively using ListObjectsOptions
        print("Listing and deleting object's inside bucket...")
        objects_list = project.list_objects(MY_BUCKET, ListObjectsOptions(recursive=True))
        # iterate through all objects path
        for obj in objects_list:
            # delete selected object
            print("Deleting '" + obj.key)
            _ = project.delete_object(MY_BUCKET, obj.key)
        print("Delete all objects inside the bucket : COMPLETE!")

        # try to delete given bucket
        print("Deleting '" + MY_BUCKET + "' bucket...")
        _ = project.delete_bucket(MY_BUCKET)
        print("Desired bucket: DELETED")
    except BucketNotFoundError as exception:
        print("Desired bucket delete error: ", exception.message)
        
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### stat_object(bucket_name, storj_path)

#### Description:

stat_object function information about an object at the specific key, 
open_project function is required as a pre-requisite for this function.\
This function accepts 2 argument bucket name and object key.\
It returns an Object object on successful execution it can be used to get other properties that are bound to it.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket_name</code>| Bucket name on storj V3 network | <code>string</code> |
|<code>storj_path</code>| Object path on storj V3 network | <code>string</code> |

#### Usage Example

```py
MY_BUCKET = "my-first-bucket"
MY_OBJECT = "my-object-name"
try:
    # some code
    _ = project.stat_object(MY_BUCKET, MY_OBJECT)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### list_objects(bucket_name, list_object_options)

#### Description:

list_objects function lists objects, open_project function is required as a pre-requisite 
for this function.\
This function accepts 2 argument bucket name and listObjectOptions.\
ListObjectsOptions defines object listing options.\
it returns an Object object, on successful execution it can be used to get other properties that are bound to it.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket_name</code>| Bucket name on storj V3 network | <code>string</code> |
|<code>list_object_options</code>| Create using uplink_python.module_classes | <code>object</code> |

#### Usage Example

```py
MY_BUCKET = "my-first-bucket"
try:
    # some code
    
    objects_list = project.list_objects(MY_BUCKET, ListObjectsOptions(recursive=True, system=True))
    # print all objects path
    for obj in objects_list:
        print(obj.key, " | ", obj.is_prefix)  # as python class object
        print(obj.get_dict())  # as python dictionary
        
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### delete_object(bucket_name, storj_path)

#### Description:

delete_object function deletes an object at the specific key, open_project function is required as a pre-requisite 
for this function.\
This function accepts 2 argument bucket name and object key.\
It returns an Object object, on successful execution it can be used to get other properties that are bound to it.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket_name</code>| Bucket name on storj V3 network | <code>string</code> |
|<code>storj_path</code>| Object path on storj V3 network | <code>string</code> |

#### Usage Example

```py
MY_BUCKET = "my-first-bucket"
MY_OBJECT = "my-object-name"
try:
    # some code
    _ = project.delete_object(MY_BUCKET, MY_OBJECT)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### upload_object(bucket_name, storj_path, upload_options)

#### Description:

upload_object function starts an upload to the specified key, open_project 
function is required as a pre-requisite for this function.\
This function accepts 3 argument bucket name, object key, and upload options.\
UploadOptions contains additional options for uploading.\
It returns an upload object, on successful execution it can be used to call other properties that are bound to it.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket_name</code>| Bucket name on storj V3 network | <code>string</code> |
|<code>storj_path</code>| Object path to be uploaded on storj V3 network | <code>string</code> |
|<code>upload_options</code>| Create using uplink_python.module_classes | <code>object</code> |

#### Usage Example

```py
MY_BUCKET = "my-first-bucket"
MY_STORJ_UPLOAD_PATH = "(optional): path / (required): filename"

try:
    # some code
    upload = project.upload_object(MY_BUCKET, MY_STORJ_UPLOAD_PATH)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```
   
### download_object(bucket_name, storj_path, download_options)

#### Description:

download_object function starts to download to the specified key, open_project function is required as a pre-requisite for this function.\
This function accepts 3 argument bucket name, object key, and download options.\
It returns a download object, on successful execution it can be used to call other properties that are bound to it.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket_name</code>| Bucket name on storj V3 network | <code>string</code> |
|<code>storj_path</code>| Path to object already uploaded on storj V3 network | <code>string</code> |
|<code>download_options</code>| Create using uplink_python.module_classes | <code>object</code> |

#### Usage Example

```py
MY_BUCKET = "my-first-bucket"
MY_STORJ_UPLOAD_PATH = "(optional): path / (required): filename"

try:
    # some code
    download = project.download_object(MY_BUCKET, MY_STORJ_UPLOAD_PATH)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```
   
## *Upload Functions*

### write(data_to_write, size_to_write)

#### Description:

write function uploads bytes data to the object's data stream. It returns the number of bytes written and throws any exception encountered that caused the write to stop early.\
upload_object function is required as a pre-requisite for this function. This function accepts 2 argument buffer object which is data_to_write in bytes and length is data being read, it returns the number of bytes written.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>data_to_write</code>| Data in bytes to be uploaded | <code>bytes</code> |
|<code>size_to_write</code>| Length of data to be upload on storj V3 network | <code>int</code> |

#### Usage Example

```py
try:
    # some code
    upload.write(bytes('some data', 'utf-8'), 9)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### write_file(file_handle)

#### Description:

write_file function uploads complete file whose handle is passed as a parameter to the object's data stream and commits the object after the upload is complete.\
This function takes 1 argument that is the filehandle of the file to be uploaded and 1 optional buffer size argument.

>Note: Filehandle should be a BinaryIO, i.e. file should be opened using the 'r+b' flag.
>e.g.: file_handle = open(SRC_FULL_FILENAME, 'r+b')
>Remember to commit the object on storj and also close the local filehandle after this function exits.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>file_handle</code>| File Stream | <code>BinaryIO</code> |

#### Usage Example

```py
try:
    # some code
    file_handle = open(SRC_FULL_FILENAME, 'r+b')
    upload.write_file(file_handle)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### commit()

#### Description:

commit function commits the uploaded data, upload_object function is required as a pre-requisite for this function. it throws an error if unsuccessful.

#### Usage Example

```py
try:
    # some code
    upload.commit()
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### abort()

#### Description:

abort function aborts an upload, upload_object function is required as a pre-requisite for this function. it throws an error if unsuccessful.

#### Usage Example

```py
try:
    # some code
    upload.abort()
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### set_custom_metadata(custom_metadata)

#### Description:

set_custom_metadata function set custom meta information, upload_object function is required as a pre-requisite for this function.\
This function accepts 1 argument CustomMetaData object which is create using uplink_python.module_classes.\
CustomMetadata contains custom user metadata about the object

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>custom_metadata</code>| Create using uplink_python.module_classes | <code>object</code> |

```py
try:
    # some code
    custom_metadata = CustomMetadata([CustomMetadataEntry(key="", key_length=0, value="", value_length=0)], 1)
    upload.set_custom_metadata(custom_metadata)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### info()

#### Description:

info function returns the last information about the uploaded object, upload_object function is required as a pre-requisite for this function.\ 
It returns an Object, on successful execution it can be used to get the property that is bound to it.

#### Usage Example

```py
try:
    # some code
    _ = upload.info()
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

## *Download Functions*

### read(size_to_read)

#### Description:

function downloads up to len size_to_read bytes from the object's data stream, download_object function is required as a pre-requisite for this function.\
This function accepts 1 argument, size_to_read is the length of the buffer.\
It returns data read and size of data read, throws an error if unsuccessful.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>size_to_read</code>| Length of data to be downloaded from storj V3 network | <code>int</code> |

#### Usage Example

```py
try:
    # some code
    _ = download.read(100)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### read_file(file_handle)

#### Description:

read file function downloads the complete object from its data stream and writes it to the file whose handle is passed as a parameter. After the download is complete it closes the download stream.

>Note: Filehandle should be a BinaryIO, i.e. file should be opened using the 'w+b' flag.
>e.g.: file_handle = open(DESTINATION_FULL_FILENAME, 'w+b')
>Remember to close the object stream on storj and also close the local filehandle
after this function exits.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>file_handle</code>| File Stream | <code>BinaryIO</code> |

#### Usage Example

```py
try:
    # some code
    download.read_file(file_handle)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### close()

#### Description:

close function closes the download, download_object function is required as a pre-requisite for this function. it throws an error if unsuccessful.

#### Usage Example

```py
try:
    # some code
    download.close()
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### info()

#### Description:

Info function returns the last information about the object, download_object function is required as a pre-requisite for this function.\
It returns a download object. On successful execution, it can be used to get other properties that are bound to it.

#### Usage Example

```py
try:
    # some code
    _ = download.info()
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```


> Note: You can view the libuplink documentation [here](https://godoc.org/storj.io/uplink).