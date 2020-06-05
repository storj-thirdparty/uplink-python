## Flow Diagram

![](https://github.com/storj-thirdparty/uplink-python/blob/master/README.assets/arch.drawio.png)


## Binding Functions

**NOTE**: Every function consists of error response. Please use it, to check if the function call was successful or not. In case, if it is not *None*, then you may also show the error's text. Please refer the sample *hello_storj.py* file, for example.


### request_access_with_passphrase(String, String, String)
    * function requests satellite for a new access grant using a passphrase
    * pre-requisites: none
    * inputs: Satellite Address (String), API key (String) and Passphrase (String)
    * output: AccessResult (Object), Error (String) if any else None

### config_request_access_with_passphrase(Object, String, String, String)
    * function requests satellite for a new access grant using a passphrase and custom configuration
    * pre-requisites: none
    * inputs: Config (Object), Satellite Address (String), API key (String) and Passphrase (String)
    * output: AccessResult (Object), Error (String) if any else None
   * **Note:** To set Config Refer: [Config](https://godoc.org/storj.io/uplink#Config)

### open_project(Object)
    * function opens Storj(V3) project using access grant.
    * pre-requisites: request_access_with_passphrase or parse_access function has been already called
    * inputs: Access (Object)
    * output: ProjectResult (Object), Error (String) if any else None

### config_open_project(Object, Object)
    * function opens Storj(V3) project using access grant and custom configuration.
    * pre-requisites: request_access_with_passphrase or parse_access function has been already called
    * inputs: Config (Object), Access (Object)
    * output: ProjectResult (Object), Error (String) if any else None
   * **Note:** To set Config Refer: [Config](https://godoc.org/storj.io/uplink#Config)

### close_project(Object)
    * function closes the Storj(V3) project.
    * pre-requisites: open_project function has been already called
    * inputs: Project (Object)
    * output: Error (Object) if any else None

### ensure_bucket(Object, String)
    * function creates a new bucket and ignores the error when it already exists
    * pre-requisites: open_project function has been already called
    * inputs: Project (Object) ,Bucket Name (String)
    * output: BucketResult (Object), Error (String) if any else None

### stat_bucket(Object, String)
    * function returns information about a bucket.
    * pre-requisites: open_project function has been already called
    * inputs: Project (Object), Bucket Name (String)
    * output: BucketResult (Object), Error (String) if any else None

### create_bucket(Object, String)
    * function creates a new bucket.
    * pre-requisites: open_project function has been already called
    * inputs: Project (Object), Bucket Name (String)
    * output: BucketResult (Object), Error (String) if any else None

### list_buckets(Object, Object)
    * function lists buckets
    * pre-requisites: open_project function has been already called
    * inputs: Project (Object), ListBucketsOptions (Object)
    * output: Bucket List (Python List), Error (String) if any else None
   * **Note:** To set List Bucket Options Refer: [ListBucketOptions](https://godoc.org/storj.io/uplink#ListBucketsOptions)

### delete_bucket(Object, String)
    * function deletes a bucket.
    * pre-requisites: open_project function has been already called
    * inputs: Project (Object), Bucket Name (String)
    * output: BucketResult (Object), Error (String) if any else None

### stat_object(Object, String, String)
    * function returns information about an object at the specific key.
    * pre-requisites: open_project
    * inputs: Project (Object) ,Bucket Name (String) , Object Key(String)
    * output: ObjectResult (Object), Error (string) if any else None

### list_objects(Object, String, Object)
    * function lists objects
    * pre-requisites: open_project function has been already called
    * inputs: Project (Object), Bucket Name (String), ListObjectsOptions (Object)
    * output: Bucket List (Python List), Error (String) if any else None
   * **Note:** To set List Object Options Refer: [ListObjectOptions](https://godoc.org/storj.io/uplink#ListObjectsOptions)

### delete_object(Object, String, String)
    * function deletes an object.
    * pre-requisites: open_project function has been already called
    * inputs: Project (Object), Bucket Name (String), Object Key (String)
    * output: ObjectResult (Object), Error (String) if any else None

### upload_object(bject, String, String, Object)
    * function starts an upload to the specified key.
    * pre-requisites: open_project function has been already called
    * inputs: Project (Object), Bucket Name (String), Object Key (String), Upload Options (Object)
    * output: UploadResult (Object), Error (String) if any else None
   * **Note:** To set Upload Options Refer: [UploadOptions](https://godoc.org/storj.io/uplink#UploadOptions)

### upload_write(Object, LP_c_ubyte, Integer)
    * function uploads bytes data passed as parameter to the object's data stream.
    * pre-requisites: upload_object function has been already called
    * inputs: Upload (Object), Bytes Data Stream(LP_c_ubyte) , Length (Integer)
    * output: WriteResult (Object), Error (String) if any else None
   * **Note:** The Data to upload (LP_c_ubyte) passed to function should be a ctypes char or uint8 pointer only. (Please refer the sample hello_storj.py file, for example.)

### upload_commit(Object)
    * function commits the uploaded data.
    * pre-requisites: upload_object function has been already called
    * inputs: Upload (Object)
    * output: Error (Object) if any else None

### upload_abort(Object)
    * function aborts an ongoing upload.
    * pre-requisites: upload_object function has been already called
    * inputs: Upload (Object)
    * output: Error (Object) if any else None

### upload_set_custom_metadata(Object, Object)
    * function to set custom meta information while uploading data
    * pre-requisites: upload_object function has been already called
    * inputs: Upload (Object), CustomMetadata (Object)
    * output: Error (Object) if any else None
   * **Note:** To set Custom Metadata Refer: [CustomMetadata](https://godoc.org/storj.io/uplink#CustomMetadata)

### upload_info(Object)
    * function returns the last information about the uploaded object.
    * pre-requisites: upload_object function has been already called
    * inputs: Upload (Object)
    * output: Object Result (Object), Error (String) if any else None

### download_object(Object, String, String, Object)
    * function starts download to the specified key.
    * pre-requisites: open_project function has been already called
    * inputs: Project (Object), Bucket Name(String), Object Key(String), Download Options(Object)
    * output: DownloadResult (Object), Error (String) if any else None
   * **Note:** To set Download Options Refer: [DownloadOptions](https://godoc.org/storj.io/uplink#DownloadOptions)

### download_read(Object, Integer)
    * function downloads from object's data stream into bytes up to length amount.
    * pre-requisites: download_object function has been already called
    * inputs: Download (Object), Length(Integer)
    * output: Data downloaded (LP_c_ubyte), ReadResult (Object), Error (String) if any else None

### close_download(Object)
    * function closes the download.
    * pre-requisites: download_object function has been already called
    * inputs: Download (Object)
    * output: Error (Object) if any else None

### download_info(Object)
    * function returns information about the downloaded object.
    * pre-requisites: download_object function has been already called
    * inputs: Download (Object)
    * output: Object Result (Object), Error (String) if any else None

### parse_access(String)
    * function to parses serialized access grant string
    * pre-requisites: none
    * inputs: Serialized Access (String)
    * output: AccessResult (Object), Error (String) if any else None

### access_serialize(Object)
    * function serializes access grant into a string.
    * pre-requisites: request_access_with_passphrase or parse_access function has been already called
    * inputs: Access (Object)
    * output: StringResult (Object), Error (String) if any else None

### access_share(Object, Object, List)
    * function creates new access grant with specific permission. Permission will be applied to prefixes when defined.
    * pre-requisites: request_access_with_passphrase or parse_access function has been already called
    * inputs: Access (Object), Permission (Object), Share Prefix (Python List of Dictionaries)
    * output: String Result (Object), Error (String) if any else None
   * **Note:** To set Permission Refer: [Permission](https://godoc.org/storj.io/uplink#Permission)
   * **Note:** To set Shared Prefix Refer: [SharedPrefix](https://godoc.org/storj.io/uplink#SharePrefix)
