## Flow Diagram

![](https://github.com/storj-thirdparty/uplink-python/blob/master/README.assets/arch.drawio.png)


## Binding Functions

>Note: All the functions, if unsuccessful, throw an exception that can be caught using try-except block. For implementation, refer to *hello_storj.py*.

## Uplink Functions

### request_access_with_passphrase(String, String, String)

#### Description

This function request_access_with_passphrase  requests satellite for a new access grant
using a passhprase, there is no pre-requisites required for this function.\
This function accepts 3 arguments Satellite URL, API Key and  encryptionpassphrase
and returns an access object on successful execution which can be used to 
call other functions which are bound to it.\
An access grant is a serialized structure that is internally comprised of an 
API Key, a set of encryption key information, and information about which Satellite
address is responsible for the metadata.\
An access grant is always associated with exactly one Project on one Satellite.

#### Arguments

| arguments | Description |  Type |
| --- | --- | --- |
|<code>satellite</code>| Storj V3 network satellite address | <code>string</code> |
|<code>api_key</code>| Storj V3 network API key |<code>string</code> |
|<code>passphrase</code>| Any passphrase |<code>string</code> |

### config_request_access_with_passphrase(Object, String, String, String)

#### Description

This function config_request_access_with_passphrase requests satellite for a new access grant 
using a passhprase and config.\
There is no pre-requisites required for this function.\
This function accepts 4 arguments Satellite URL, API Key, encryptionpassphrase and config object and returns an access object on successful execution which can be used to call other functions which are bound to it.

#### Arguments

| arguments | Description |  Type |
| --- | --- | --- |
|<code>config</code>| Create using uplink_python.module_classes | <code>object</code> |
|<code>satellite</code>|  Storj V3 network satellite address | <code>string</code> |
|<code>api_key</code>| Storj V3 network API key |<code>string</code> |
|<code>passphrase</code>| Any passphrase string |<code>string</code> |

### parse_access(String)

#### Description

parse_access function to parses serialized access grant string there is no pre-requisites 
required for this function.\
this function accepts one argument serialized access String
which is returned by access_serialize function it returns an access object on successful 
execution which can be used to call other functions which are bound to it.\
This should be the main way to instantiate an access grant for opening a project.

#### Arguments

| arguments | Description |  Type |
| --- | --- | --- |
|<code>serialized_access</code>| Serialized access string returned by access.serialize function | <code>string</code> |

## Access Functions

### serialize()

#### Description

serialize function serializes access grant into a string.\
parse access function is required as a pre-requisite for this function.
which is returned by access_share function.\
it returns an Serialized Access String 
on successful execution which is used to be as parse_access argument.

### share(Object, List)

#### Description

share function creates new access grant with specific permission. Permission will be
applied to prefixes when defined.
parse access function is required as a pre-requisite for this function.\
this function accepts 2 arguments permissions(object) Permission defines what actions can be used to share which is access 
from storj Permission defines what actions can be used to share, shared_prefix(python list of dictionaries) 
which is access from storj, and prefixcount is getting from the count of share prefix 
in the list.\
It returns an access object on successful execution which can be used 
to call other functions which are bound to it.

#### Arguments

| arguments | Description |  Type |
| --- | --- | --- |
|<code>permissions</code>| Create using uplink_python.module_classes |<code>object</code> |
|<code>shared_prefix</code>| Create using uplink_python.module_classes |<code>list of objects</code> |

### open_project()

#### Description

Once you have a valid access grant, you can open a Project with the access that access grant,
open_project function opens project using access grant.\
request_access_with_passphrase or config_request_access_with_passphrase function is required as a pre-requisite.\
it returns an project object on successful execution which can be used to call 
other functions which are bound to it.\
It allows you to manage buckets and objects within buckets.

### config_open_project(Object)

##### Description

config_open_project function opens project using access grant and config.\
request_access_with_passphrase or config_request_access_with_passphrase function
is required as a pre-requisite. This function accepts 1 argument config(object) which is access from storj
library.\
it returns an project object on successful execution which can be used to call 
other functions which are bound to it.

##### Arguments

| arguments | Description |  Type |
| --- | --- | --- |
|<code>config</code>| Create using uplink_python.module_classes | <code>object</code> |

## Project Functions

### close()

#### Description

close function closes the project and open_project function is required as a pre-requisite.\
it returns an error object if on successful execution is not occurred.

### ensure_bucket(String)

#### Description

ensure_bucket function creates a new bucket and ignores the error when it 
already exists and open_project function is required as a pre-requisite.\
 This function accepts 1 argument bucket name which is access from storj configuration.\
It returns an bucket 
object on successful execution it can be used to get other properties 
which are bound to it.

##### Arguments

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket_name</code>| Bucket name on storj V3 network | <code>string</code> |

### stat_bucket(String)

#### Description

stat_bucket function returns information about a bucket and open_project function is 
required as a pre-requisite.\
This function accepts 1 argument bucket name which is access from storj configuration.\
it returns an bucket object on successful execution it can be used to get
other properties which are bound to it.

#### Arguments

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket_name</code>| Bucket name on storj V3 network | <code>string</code> |

### create_bucket(String)

#### Description

create_bucket function creates a new bucket When bucket already exists it returns 
a valid Bucket and ErrBucketExists and open_project function is required
as a pre-requisite.\
This function accepts 1 argument bucket name which is access from storj 
configuration.\
It returns an bucket object on successful execution it can be 
used to get other properties which are bound to it.

#### Arguments

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket_name</code>| Bucket name on storj V3 network | <code>string</code> |

### list_buckets()

##### Description

lsit_buckets function lists buckets and open_project function is required
as a pre-requisite for this function.\
This function takes 1 optional argument listObjectOptions which is accessed from module_classes.
It returns an bucketList object on successful execution it can be used to get other
properties which are bound to it.

| arguments | Description |  Type |
| --- | --- | --- |
|<code>list_bucket_options</code>| Create using uplink_python.module_classes | <code>object</code> |

### delete_bucket(String)

#### Description

delete_bucket function deletes a bucket When bucket is not empty it returns ErrBucketNotEmpty.
and open_project function is requiredas a pre-requisite for this function .\
This function accepts 1 argument bucket name which is access from storj configuration.\
It returns an bucket object on successful execution it can be used to get other
properties which are bound to it.

#### Arguments

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket_name</code>| Bucket name on storj V3 network | <code>string</code> |

### stat_object(String, String)

##### Description

stat_object function information about an object at the specific key and 
open_project function is required as a pre-requisite for this function.\
This function accepts 2 argument bucket name which is access from storj configuration and Object Key which is access from storj configuration.\
It returns an objectinfo object on successful execution it can be used to get other
properties which are bound to it.

##### Arguments

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket_name</code>| Bucket name on storj V3 network | <code>string</code> |
|<code>storj_path</code>| Object path on storj V3 network | <code>string</code> |

### list_objects(String, Object)

##### Description

list_objects function lists objects, open_project function is required as a pre-requisite 
for this function.\
This function accepts 2 argument bucket name which is access from storj configuration and listObjectOptions 
which is access from storj library ListObjectsOptions defines object listing options.\
it returns an objectList object, on successful execution it can be used to get 
other properties which are bound to it.

##### Arguments

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket_name</code>| Bucket name on storj V3 network | <code>string</code> |
|<code>list_object_options</code>| Create using uplink_python.module_classes | <code>object</code> |

### delete_object(String, String)

##### Description

delete_object function deletes an object at the specific key, open_project function is required as a pre-requisite 
for this function.\
This function accepts 2 argument  bucket name which is access from storj configuration and ObjectKey
which is access from storj configuration.\
It returns an objectinfo object, on successful 
execution it can be used to get other properties which are bound to it.

##### Arguments

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket_name</code>| Bucket name on storj V3 network | <code>string</code> |
|<code>storj_path</code>| Object path on storj V3 network | <code>string</code> |

### upload_object(String, String, Object)

##### Description

upload_object function starts an upload to the specified key, open_project 
function is required as a pre-requisite for this function.\
This function accepts 3 argument bucket name 
which is access from storj configuration, ObjectKey which is access from storj 
configuration and uploadOptions which is access from storj library UploadOptions 
contains additional options for uploading.\
It returns an upload object, on successful execution it can be used to call other properties which are bound to it.

##### Arguments

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket_name</code>| Bucket name on storj V3 network | <code>string</code> |
|<code>storj_path</code>| Object path to be uploaded on storj V3 network | <code>string</code> |
|<code>upload_options</code>| Create using uplink_python.module_classes | <code>object</code> |
   
### download_object(String, String, Object)

##### Description

download_object function starts download to the specified key, open_project 
function is required as a pre-requisite for this function.\
This function accepts 3 argument  bucket name 
which is access from storj configuration, ObjectKey which is access from storj 
configuration and downloadOptions which is access from storj library.\
It returns an download object, on successful execution it can be used to call other properties which are bound to it.

##### Arguments

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket_name</code>| Bucket name on storj V3 network | <code>string</code> |
|<code>storj_path</code>| Path to object already uploaded on storj V3 network | <code>string</code> |
|<code>download_options</code>| Create using uplink_python.module_classes | <code>object</code> |
  
## Upload Functions

### write(Bytes, Int)

write function uploads bytes data to the object's data stream. It 
returns the number of bytes written and throuws any exception encountered 
that caused the write to stop early.\
upload_object function is required as a pre-requisite 
for this function. This function accepts 2 argument buffer object which is data_to_write in bytes and 
Length is data being read and returns an writeresult object.\
On successful execution it can be used to get other properties which are bound to it.

#### Arguments

| arguments | Description |  Type |
| --- | --- | --- |
|<code>data_to_write</code>| Data in bytes to be uploaded | <code>bytes</code> |
|<code>size_to_write</code>| Length of data to be upload on storj V3 network | <code>int</code> |

### write_file(Object)

write_file function uploads complete file whose handle is passed as parameter to the
object's data stream and commits the object after upload is complete.\
This function takes 1 arguement that is the file handle of the file to be uplaoded
and 1 optional buffer size argument.

>Note: File handle should be a BinaryIO, i.e. file should be opened using 'r+b" flag.
>e.g.: file_handle = open(SRC_FULL_FILENAME, 'r+b')
>Remember to commit the object on storj and also close the local file handle after this function exits.

##### Arguments

| arguments | Description |  Type |
| --- | --- | --- |
|<code>file_handle</code>| File Stream | <code>BinaryIO</code> |

### commit()

##### Description

commit function commits the uploaded data, upload_object function 
is required as a pre-requisite for this function. it returns an error object, 
if successful execution is not occurred.

### abort()

##### Description

abort function aborts an upload, upload_object function is required as 
a pre-requisite for this function. it returns an error object, 
if successful execution is not occurred.

### set_custom_metadata(Object)

##### Description

set_custom_metadata function set custom meta information, upload_object function 
is required as a pre-requisite for this function.\
This function accepts 1 argument CustomMetaData object which is access from storj library CustomMetadata contains custom user metadata about the object 
it returns an error object, if successful execution is not occurred.

##### Arguments

| arguments | Description |  Type |
| --- | --- | --- |
|<code>custom_metadata</code>| Create using uplink_python.module_classes | <code>object</code> |

### info()

##### Description

info function returns the last information about the uploaded object, upload_object function 
is required as a pre-requisite for this function.\ 
It returns an Object, on successful execution it can be use to get property which are bound to it.

## Download Functions

### read(Int)

##### Description

function downloads up to len size_to_read bytes from the object's data stream,
download_object function is required as a pre-requisite for this function.\
This function accepts1 argument size_to_read is length of the buffer.\
It returns an readresult object,
On successful execution it can be used to get other properties which are bound to it.

##### Arguments

| arguments | Description |  Type |
| --- | --- | --- |
|<code>size_to_read</code>| Length of data to be downloaded from storj V3 network | <code>int</code> |

### read_file(Object)

##### Description

read file function downloads complete object from it's data stream and writes it to the file whose handle is passed as parameter. After the download is complete it closes the download stream.

>Note: File handle should be a BinaryIO, i.e. file should be opened using 'w+b" flag.
>e.g.: file_handle = open(DESTINATION_FULL_FILENAME, 'w+b')
>Remember to close the object stream on storj and also close the local file handle
after this function exits.

#### Arguments

| arguments | Description |  Type |
| --- | --- | --- |
|<code>file_handle</code>| File Stream | <code>BinaryIO</code> |

### close()

##### Description

close function closes the download, download_object function is required as 
a pre-requisite for this function. it returns an error object, 
if successful execution is not occurred.

### info()

##### Description

Info function returns the last information about the object, download_object 
function is required as a pre-requisite for this function.\
It returns an download object. On successful execution it can be used to get other properties which are bound to it.
