# Types, Errors, and Constants

## Types

### Config(user_agent, dial_timeout_milliseconds, temp_directory)

#### Description:

Config defines the configuration for using the uplink library.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>user_agent</code>| Name of the partner | <code>string</code> |
|<code>dial_timeout_milliseconds</code>| How long client should wait for establishing a connection to peers. | <code>int</code> |
|<code>temp_directory</code>| Where to save data during downloads to use less memory. | <code>string</code> |

#### Usage Example

```py
from uplink_python.module_classes import Config

config = Config(user_agent="UserAgent")
try:
    # some code
    project = access.config_open_project(config)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### Permission(allow_download, allow_upload, allow_list, allow_delete, not_before, not_after)

#### Description:

Permission defines what actions can be used to share.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>allow_download</code>| Gives permission to download the object's content |<code>string</code> |
|<code>allow_upload</code>| Gives permission to create buckets and upload new objects |<code>string</code> |
|<code>allow_list</code>| Gives permission to list buckets |<code>string</code> |
|<code>allow_delete</code>| Gives permission to delete buckets and objects |<code>string</code> |
|<code>not_before</code>| Restricts when the resulting access grant is valid for |<code>int</code> |
|<code>not_after</code>| Restricts when the resulting access grant is valid till |<code>int</code> |

#### Usage Example

```py
from uplink_python.module_classes import Permission

permissions = Permission(allow_list=True, allow_delete=False)
try:
    # some code
    new_access = access.share(permissions, shared_prefix)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### SharePrefix(bucket, prefix)

#### Description:

SharePrefix defines a prefix that will be shared.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket</code>| Bucket name on storj V3 network | <code>string</code> |
|<code>prefix</code>| Prefix is the prefix of the shared object keys | <code>string</code> |

>Note: that within a bucket, the hierarchical key derivation scheme is delineated by forwarding slashes (/), so encryption information will be included in the resulting access grant to decrypt any key that shares the same prefix up until the last slash.

#### Usage Example

```py
from uplink_python.module_classes import SharePrefix

shared_prefix = [SharePrefix(bucket=MY_BUCKET, prefix="")]
try:
    # some code
    new_access = access.share(permissions, shared_prefix)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### Bucket(name, created)

#### Description:

A bucket contains information about the bucket.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>name</code>| Bucket name on storj V3 network | <code>string</code> |
|<code>created</code>| Time of bucket created on storj V3 network | <code>int</code> |

#### Methods:

get_dict() -> convert bucket object to python dictionary

#### Usage Example

```py
try:
    # some code
    bucket = project.create_bucket(MY_BUCKET)
    print(bucket.name)
    print(bucket.get_dict())
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### CustomMetadata(entries, count)

#### Description:

CustomMetadata contains a list of CustomMetadataEntry about the object.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>entries</code>| List of CustomMetadataEntry about the object | <code>list of objects</code> |
|<code>count</code>| Number of entries | <code>int</code> |

#### Methods:

get_dict() -> convert CustomMetadata object to python dictionary

#### Usage Example

```py
try:
    # some code
    custom_metadata = CustomMetadata([CustomMetadataEntry(key="", key_length=0, value="", value_length=0)], 1)
    upload.set_custom_metadata(custom_metadata)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### CustomMetadataEntry(key, key_length, value, value_length)

#### Description:

CustomMetadata contains custom user metadata about the object.

When choosing a custom key for your application start it with a prefix "app: key",
as an example application named"Image Board" might use a key "image-board: title".

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>key</code>| Key | <code>string</code> |
|<code>key_length</code>| Length of key | <code>int</code> |
|<code>value</code>| Value | <code>string</code> |
|<code>value_length</code>| Length of value | <code>int</code> |

#### Methods:

get_dict() -> convert CustomMetadataEntry object to python dictionary

#### Usage Example

```py
try:
    # some code
    custom_metadata_entries = [CustomMetadataEntry(key="", key_length=0, value="", value_length=0), CustomMetadataEntry(key="", key_length=0, value="", value_length=0)]
    custom_metadata = CustomMetadata(custom_metadata_entries, 2)
    upload.set_custom_metadata(custom_metadata)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### SystemMetadata(created, expires, content_length)

#### Description:

SystemMetadata contains information about the object that cannot be changed directly.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>created</code>| Time when object was created | <code>int</code> |
|<code>expires</code>| Time till when object was be valid | <code>int</code> |
|<code>content_length</code>| Size of the object | <code>int</code> |

#### Methods:

get_dict() -> convert CustomMetadata object to python dictionary

#### Usage Example

```py
try:
    # some code
    object_ = project.delete_object(MY_BUCKET, MY_STORJ_UPLOAD_PATH)
    print(object_.system.content_length)
    print(object_.system.get_dict())
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### Object(key, is_prefix, system, custom)

#### Description:

The object contains information about an object.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>key</code>| Object path on storj V3 network | <code>string</code> |
|<code>is_prefix</code>| is_prefix indicates whether the Key is a prefix for other objects | <code>bool</code> |
|<code>system</code>| SystemMetadata contains information about the object | <code>object</code> |
|<code>custom</code>| CustomMetadata contains a list of CustomMetadataEntry about the object | <code>object</code> |

#### Methods:

get_dict() -> convert bucket object to python dictionary

#### Usage Example

```py
try:
    # some code
    bucket = project.create_bucket(MY_BUCKET)
    print(bucket.name)
    print(bucket.get_dict())
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### ListObjectsOptions(prefix, cursor, recursive, system, custom)

#### Description:

ListObjectsOptions defines object listing options.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>prefix</code>| Prefix allows to filter objects by a key prefix. If not empty, it must end with slash | <code>string</code> |
|<code>cursor</code>| Cursor sets the starting position of the iterator. The first item listed will be the one after the cursor | <code>string</code> |
|<code>recursive</code>| Recursive iterates the objects without collapsing prefixes | <code>bool</code> |
|<code>system</code>| System includes SystemMetadata in the results | <code>bool</code> |
|<code>custom</code>| Custom includes CustomMetadata in the results | <code>bool</code> |


#### Usage Example

```py
try:
    # some code
    list_object_options = ListObjectsOptions(recursive=True)
    objects_list = project.list_objects(MY_BUCKET, list_object_options)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### ListBucketsOptions(cursor)

#### Description:

ListBucketsOptions defines bucket listing options.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>cursor</code>| Cursor sets the starting position of the iterator. The first item listed will be the one after the cursor | <code>string</code> |

#### Usage Example

```py
try:
    # some code
    list_buckets_options = ListBucketsOptions(cursor="")
    bucket_list = project.list_buckets(list_buckets_options)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### UploadOptions(expires)

#### Description:

UploadOptions contains additional options for uploading.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>expires</code>| When expires is 0 or negative, it means no expiration | <code>int</code> |

#### Usage Example

```py
try:
    # some code
    upload_options = UploadOptions(expires=0)
    upload = project.upload_object(MY_BUCKET, MY_STORJ_UPLOAD_PATH, upload_options)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### DownloadOptions(offset, length)

#### Description:

DownloadOptions contains additional options for downloading.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>offset</code>| Offset to the download object | <code>int</code> |
|<code>length</code>| When length is negative, it will read until the end of the blob | <code>int</code> |

#### Usage Example

```py
try:
    # some code
    download_options = DownloadOptions(length=-1)
    download = project.download_object(MY_BUCKET, MY_STORJ_UPLOAD_PATH, download_options)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

## Errors

### StorjException

#### Description:

StorjException is a broad category of all the errors thrown from uplink functions.\
It can be used to catch error thrown from uplink when one does not know what exception can be thrown from a particular function.

#### Returns:

| Returns | Description |  Type |
| --- | --- | --- |
|<code>code</code>| Error code related to error | <code>int</code> |
|<code>message</code>| Short description of error  |<code>string</code> |
|<code>details</code>| Detailed description of the error |<code>string</code> |

#### Usage Example

```py
try:
    # function calls
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

StorjException is further sub-categorized into various error specific classes, These classes inherit all their properties from the base class, i.e. StorjException:

    InternalError
    BandwidthLimitExceededError
    BucketAlreadyExistError
    BucketNameInvalidError
    BucketNotEmptyError
    BucketNotFoundError
    ObjectKeyInvalidError
    ObjectNotFoundError
    TooManyRequestsError
    UploadDoneError
    CancelledError
    InvalidHandleError
    

### InternalError

InternalError is raised when there is an issue in resolving a request sent to uplink, it might be due to an invalid or incorrect parameter passed.

### BandwidthLimitExceededError

BandwidthLimitExceededError is raised when the project will exceed the bandwidth limit.

### BucketAlreadyExistError

BucketAlreadyExistError is raised when the bucket already exists during creation.

### BucketNameInvalidError

BucketNameInvalidError is raised when the bucket name is invalid

### BucketNotEmptyError

BucketNotEmptyError is raised when the bucket is not empty during deletion.

### BucketNotFoundError

BucketNotFoundError is raised when the bucket is not found.

### ObjectKeyInvalidError

ObjectKeyInvalidError is raised when the object key is invalid.

### ObjectNotFoundError

ObjectNotFoundError is raised when the object is not found.

### TooManyRequestsError

TooManyRequestsError is raised when the user has sent too many requests in a given amount of time.

### UploadDoneError

UploadDoneError is raised when either Abort or Commit has already been called.

### InvalidHandleError

InvalidHandleError is raised when object handle passes is either invalid or already freed.

## Constants

    ERROR_INTERNAL = 0x02
    ERROR_CANCELED = 0x03
    ERROR_INVALID_HANDLE = 0x04
    ERROR_TOO_MANY_REQUESTS = 0x05
    ERROR_BANDWIDTH_LIMIT_EXCEEDED = 0x06
# Types, Errors, and Constants

## Types

### Config(user_agent, dial_timeout_milliseconds, temp_directory)

#### Description:

Config defines the configuration for using the uplink library.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>user_agent</code>| Name of the partner | <code>string</code> |
|<code>dial_timeout_milliseconds</code>| How long client should wait for establishing a connection to peers. | <code>int</code> |
|<code>temp_directory</code>| Where to save data during downloads to use less memory. | <code>string</code> |

#### Usage Example

```py
from uplink_python.module_classes import Config

config = Config(user_agent="UserAgent")
try:
    # some code
    project = access.config_open_project(config)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### Permission(allow_download, allow_upload, allow_list, allow_delete, not_before, not_after)

#### Description:

Permission defines what actions can be used to share.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>allow_download</code>| Gives permission to download the object's content |<code>string</code> |
|<code>allow_upload</code>| Gives permission to create buckets and upload new objects |<code>string</code> |
|<code>allow_list</code>| Gives permission to list buckets |<code>string</code> |
|<code>allow_delete</code>| Gives permission to delete buckets and objects |<code>string</code> |
|<code>not_before</code>| Restricts when the resulting access grant is valid for |<code>int</code> |
|<code>not_after</code>| Restricts when the resulting access grant is valid till |<code>int</code> |

#### Usage Example

```py
from uplink_python.module_classes import Permission

permissions = Permission(allow_list=True, allow_delete=False)
try:
    # some code
    new_access = access.share(permissions, shared_prefix)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### SharePrefix(bucket, prefix)

#### Description:

SharePrefix defines a prefix that will be shared.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>bucket</code>| Bucket name on storj V3 network | <code>string</code> |
|<code>prefix</code>| Prefix is the prefix of the shared object keys | <code>string</code> |

>Note: that within a bucket, the hierarchical key derivation scheme is delineated by forwarding slashes (/), so encryption information will be included in the resulting access grant to decrypt any key that shares the same prefix up until the last slash.

#### Usage Example

```py
from uplink_python.module_classes import SharePrefix

shared_prefix = [SharePrefix(bucket=MY_BUCKET, prefix="")]
try:
    # some code
    new_access = access.share(permissions, shared_prefix)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### Bucket(name, created)

#### Description:

A bucket contains information about the bucket.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>name</code>| Bucket name on storj V3 network | <code>string</code> |
|<code>created</code>| Time of bucket created on storj V3 network | <code>int</code> |

#### Methods:

get_dict() -> convert bucket object to python dictionary

#### Usage Example

```py
try:
    # some code
    bucket = project.create_bucket(MY_BUCKET)
    print(bucket.name)
    print(bucket.get_dict())
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### CustomMetadata(entries, count)

#### Description:

CustomMetadata contains a list of CustomMetadataEntry about the object.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>entries</code>| List of CustomMetadataEntry about the object | <code>list of objects</code> |
|<code>count</code>| Number of entries | <code>int</code> |

#### Methods:

get_dict() -> convert CustomMetadata object to python dictionary

#### Usage Example

```py
try:
    # some code
    custom_metadata = CustomMetadata([CustomMetadataEntry(key="", key_length=0, value="", value_length=0)], 1)
    upload.set_custom_metadata(custom_metadata)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### CustomMetadataEntry(key, key_length, value, value_length)

#### Description:

CustomMetadata contains custom user metadata about the object.

When choosing a custom key for your application start it with a prefix "app: key",
as an example application named"Image Board" might use a key "image-board: title".

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>key</code>| Key | <code>string</code> |
|<code>key_length</code>| Length of key | <code>int</code> |
|<code>value</code>| Value | <code>string</code> |
|<code>value_length</code>| Length of value | <code>int</code> |

#### Methods:

get_dict() -> convert CustomMetadataEntry object to python dictionary

#### Usage Example

```py
try:
    # some code
    custom_metadata_entries = [CustomMetadataEntry(key="", key_length=0, value="", value_length=0), CustomMetadataEntry(key="", key_length=0, value="", value_length=0)]
    custom_metadata = CustomMetadata(custom_metadata_entries, 2)
    upload.set_custom_metadata(custom_metadata)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### SystemMetadata(created, expires, content_length)

#### Description:

SystemMetadata contains information about the object that cannot be changed directly.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>created</code>| Time when object was created | <code>int</code> |
|<code>expires</code>| Time till when object was be valid | <code>int</code> |
|<code>content_length</code>| Size of the object | <code>int</code> |

#### Methods:

get_dict() -> convert CustomMetadata object to python dictionary

#### Usage Example

```py
try:
    # some code
    object_ = project.delete_object(MY_BUCKET, MY_STORJ_UPLOAD_PATH)
    print(object_.system.content_length)
    print(object_.system.get_dict())
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### Object(key, is_prefix, system, custom)

#### Description:

The object contains information about an object.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>key</code>| Object path on storj V3 network | <code>string</code> |
|<code>is_prefix</code>| is_prefix indicates whether the Key is a prefix for other objects | <code>bool</code> |
|<code>system</code>| SystemMetadata contains information about the object | <code>object</code> |
|<code>custom</code>| CustomMetadata contains a list of CustomMetadataEntry about the object | <code>object</code> |

#### Methods:

get_dict() -> convert bucket object to python dictionary

#### Usage Example

```py
try:
    # some code
    bucket = project.create_bucket(MY_BUCKET)
    print(bucket.name)
    print(bucket.get_dict())
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### ListObjectsOptions(prefix, cursor, recursive, system, custom)

#### Description:

ListObjectsOptions defines object listing options.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>prefix</code>| Prefix allows to filter objects by a key prefix. If not empty, it must end with slash | <code>string</code> |
|<code>cursor</code>| Cursor sets the starting position of the iterator. The first item listed will be the one after the cursor | <code>string</code> |
|<code>recursive</code>| Recursive iterates the objects without collapsing prefixes | <code>bool</code> |
|<code>system</code>| System includes SystemMetadata in the results | <code>bool</code> |
|<code>custom</code>| Custom includes CustomMetadata in the results | <code>bool</code> |


#### Usage Example

```py
try:
    # some code
    list_object_options = ListObjectsOptions(recursive=True)
    objects_list = project.list_objects(MY_BUCKET, list_object_options)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### ListBucketsOptions(cursor)

#### Description:

ListBucketsOptions defines bucket listing options.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>cursor</code>| Cursor sets the starting position of the iterator. The first item listed will be the one after the cursor | <code>string</code> |

#### Usage Example

```py
try:
    # some code
    list_buckets_options = ListBucketsOptions(cursor="")
    bucket_list = project.list_buckets(list_buckets_options)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### UploadOptions(expires)

#### Description:

UploadOptions contains additional options for uploading.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>expires</code>| When expires is 0 or negative, it means no expiration | <code>int</code> |

#### Usage Example

```py
try:
    # some code
    upload_options = UploadOptions(expires=0)
    upload = project.upload_object(MY_BUCKET, MY_STORJ_UPLOAD_PATH, upload_options)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

### DownloadOptions(offset, length)

#### Description:

DownloadOptions contains additional options for downloading.

#### Arguments:

| arguments | Description |  Type |
| --- | --- | --- |
|<code>offset</code>| Offset to the download object | <code>int</code> |
|<code>length</code>| When length is negative, it will read until the end of the blob | <code>int</code> |

#### Usage Example

```py
try:
    # some code
    download_options = DownloadOptions(length=-1)
    download = project.download_object(MY_BUCKET, MY_STORJ_UPLOAD_PATH, download_options)
    # some code
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

## Errors

### StorjException

#### Description:

StorjException is a broad category of all the errors thrown from uplink functions.\
It can be used to catch error thrown from uplink when one does not know what exception can be thrown from a particular function.

#### Returns:

| Returns | Description |  Type |
| --- | --- | --- |
|<code>code</code>| Error code related to error | <code>int</code> |
|<code>message</code>| Short description of error  |<code>string</code> |
|<code>details</code>| Detailed description of the error |<code>string</code> |

#### Usage Example

```py
try:
    # function calls
except StorjException as exception:
        print("Exception Caught: ", exception.details)
```

StorjException is further sub-categorized into various error specific classes, These classes inherit all their properties from the base class, i.e. StorjException:

    InternalError
    BandwidthLimitExceededError
    BucketAlreadyExistError
    BucketNameInvalidError
    BucketNotEmptyError
    BucketNotFoundError
    ObjectKeyInvalidError
    ObjectNotFoundError
    TooManyRequestsError
    UploadDoneError
    CancelledError
    InvalidHandleError
    

### InternalError

InternalError is raised when there is an issue in resolving a request sent to uplink, it might be due to an invalid or incorrect parameter passed.

### BandwidthLimitExceededError

BandwidthLimitExceededError is raised when the project will exceed the bandwidth limit.

### BucketAlreadyExistError

BucketAlreadyExistError is raised when the bucket already exists during creation.

### BucketNameInvalidError

BucketNameInvalidError is raised when the bucket name is invalid

### BucketNotEmptyError

BucketNotEmptyError is raised when the bucket is not empty during deletion.

### BucketNotFoundError

BucketNotFoundError is raised when the bucket is not found.

### ObjectKeyInvalidError

ObjectKeyInvalidError is raised when the object key is invalid.

### ObjectNotFoundError

ObjectNotFoundError is raised when the object is not found.

### TooManyRequestsError

TooManyRequestsError is raised when the user has sent too many requests in a given amount of time.

### UploadDoneError

UploadDoneError is raised when either Abort or Commit has already been called.

### InvalidHandleError

InvalidHandleError is raised when object handle passes is either invalid or already freed.

## Constants

    ERROR_INTERNAL = 0x02
    ERROR_CANCELED = 0x03
    ERROR_INVALID_HANDLE = 0x04
    ERROR_TOO_MANY_REQUESTS = 0x05
    ERROR_BANDWIDTH_LIMIT_EXCEEDED = 0x06

    ERROR_BUCKET_NAME_INVALID = 0x10
    ERROR_BUCKET_ALREADY_EXISTS = 0x11
    ERROR_BUCKET_NOT_EMPTY = 0x12
    ERROR_BUCKET_NOT_FOUND = 0x13

    ERROR_OBJECT_KEY_INVALID = 0x20
    ERROR_OBJECT_NOT_FOUND = 0x21
    ERROR_UPLOAD_DONE = 0x22


> Note: You can view the libuplink documentation [here](https://godoc.org/storj.io/uplink).