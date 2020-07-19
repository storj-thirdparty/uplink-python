# Tutorial

> Welcome to the guide to create a project by yourself that uses python binding. Let's start!

## Step 1: Storj Configurations

First and foremost, you need to have all the keys and configuration to connect to the storj network. You can create a JSON file and parse the JSON file to sotre the values in a class/strucure or you can simply initialize the corrsponding variables inside the main method as done in the sample *hello_storj.py* file in the following way:

```py
# Storj configuration information
MY_API_KEY = "change-me-to-the-api-key-created-in-satellite-gui"
MY_SATELLITE = "us-central-1.tardigrade.io:7777"
MY_BUCKET = "my-first-bucket"
MY_STORJ_UPLOAD_PATH = "(optional): path / (required): filename"

# (path + filename) OR filename
MY_ENCRYPTION_PASSPHRASE = "you'll never guess this"
```

## Step 2: File Path

File path could be path of the file to be upload from or path where a file needs to be download at or both. You can create a JSON file and parse it or simply initialize file path variable(s) as done in the sample *hello_storj.py* file in the following way:

```py
# Source and destination path and file name for testing
SRC_FULL_FILENAME = "filename with extension of source file on local system"
DESTINATION_FULL_FILENAME = "filename with extension to save on local system"
```

## Step 3: Create libuplink class object

Next, you need to create an object of libUplinkPy class that will be used to call the libuplink functions.

```py
StorjObj = LibUplinkPy()
```

## Step 4: Create Access Handle

Once you have initialized the libuplink class object, you need to create an access handle to sotrj network in the following way:

```py
access_result, err = StorjObj.request_access_with_passphrase(MY_SATELLITE, MY_API_KEY, MY_ENCRYPTION_PASSPHRASE)
if err is not None:
    print(err)
    sys.exit()
```

## Step 5: Open Project

To perform the uplink operations you need to create a project, which can be done using the following code fragmeent:

```py
project_result, err = StorjObj.open_project(access_result.access)
if err is not None:
    print(err)
    sys.exit()
```

## Step 6: Create/Ensure Bucket

All the uploading and downloading is performed inside and from a bucket on the sotrj network. To ensure that the bucket you have specified in your configurations above exists or create one if not, use the following code:

```py
bucket_result, err = StorjObj.ensure_bucket(project_result.project, MY_BUCKET)
if err is not None:
    print(err)
    sys.exit()
```

## Step 7: Upload/Download

### Upload Data

Uploading a file consists of the following sub-steps:

#### Create File Handle

To stream the data to storj you need to create a file stream or handle which can be done in the following way:

```py
file_handle = open(src_full_filename, 'r+b')
data_len = path.getsize(src_full_filename)
```

#### Create Upload Handle

While file handle acts as the source stream, upload handle acts as the destination stream and can be created as follows:

```py
upload_result, error = storj_obj.upload_object(project, bucket_name, storj_path, upload_options)
```

You can create *upload_options* by referring to the [libuplink documentation](https://godoc.org/storj.io/uplink) or simply pass *none*.

#### Stream the data

Once the source and desctination streams are created, its time to perform data streaming using the following code:

```py
uploaded_total = 0
while uploaded_total < data_len:
    # set packet size to be used while uploading
    size_to_write = 256 if (data_len - uploaded_total > 256) else data_len - uploaded_total

    # exit while loop if nothing left to upload
    if size_to_write == 0:
        break

    # file reading process from the last read position
    file_handle.seek(uploaded_total)
    data_to_write = file_handle.read(size_to_write)

    # --------------------------------------------
    # data conversion to type required by function
    # get size of data in c type int32 variable
    # conversion of read bytes data to c type ubyte Array
    data_to_write = (c_uint8 * c_int32(len(data_to_write)).value)(*data_to_write)
    # conversion of c type ubyte Array to LP_c_ubyte required by upload write function
    data_to_write_ptr = cast(data_to_write, POINTER(c_uint8))
    # --------------------------------------------

    # call to write data to Storj bucket
    write_result, error = storj_obj.upload_write(upload_result.upload, data_to_write_ptr, size_to_write)

    # exit while loop if nothing left to upload / unable to upload
    if int(write_result.bytes_written) == 0:
        break

    # update last read location
    uploaded_total += int(write_result.bytes_written)
```

The above code streams the data in chunks of 256 bytes. You can change this size as per your requirement and convenience.

#### Commit Upload

Once the data has been successfully streamed, the upload needs to be committed using the following method:

```py
error = storj_obj.upload_commit(upload_result.upload)
```

### Download Data

Downloading a file consists of the following sub-steps:

#### Open/Create Destination File

First we need to create a destination file to store the downloaded data into. This will also act as the destination stream.

```py
 # open / create file with the given name to save the downloaded data
file_handle = open(dest_full_pathname, 'w+b')
```

#### Create Download Stream

The source stream for downloading data from storj to the required file can be created using the following code:

```py
download_result, error = storj_obj.download_object(project, bucket_name, storj_path, download_options)
```

You can create *download_options* by referring to the [libuplink documentation](https://godoc.org/storj.io/uplink) or simply pass *none*.

#### Retrieve the Download File Size

Before streaming the data we need to know the amount of data we are downloading to avoid discrepancies. Fetching the data size can be done using the following code:

```py
# get object data
obj_result, error = storj_obj.stat_object(project, bucket_name, storj_path)

# find object size
file_size = int(obj_result.object.contents.system.content_length)
```

#### Stream the data

Now, its time to do the required downloading and can be done as follows:

```py
# set packet size to be used while downloading
size_to_read = 256
# initialize local variables and start downloading packets of data
downloaded_total = 0
while True:
    # call to read data from Storj bucket
    data_read_ptr, read_result, error = storj_obj.download_read(download_result.download,
                                                                size_to_read)
   
    # file writing process from the last written position if new data is downloaded
    if int(read_result.bytes_read) != 0:
        #
        # --------------------------------------------
        # data conversion to type python readable form
        # conversion of LP_c_ubyte to python readable data variable
        data_read = string_at(data_read_ptr, int(read_result.bytes_read))
        # --------------------------------------------
        #
        file_handle.seek(downloaded_total)
        file_handle.write(data_read)
    #
    # update last read location
    downloaded_total += int(read_result.bytes_read)
    #
    # break if download complete
    if downloaded_total == file_size:
        break
```

The above code streams the data in chunks of 256 bytes. You can change this size as per your requirement and convenience.

#### Close Download Stream

Once the download streaming is complete, its important to close the download stream.

```py
# close downloader and free downloader access
error = storj_obj.close_download(download_result.download)
```

> NOTE: Perform error handling as per your implmentation.

> NOTE: Alternatively, you can simple create a method(s) that can be called from the main method and performs all the above steps internally as done in the sample file.

## Step 8: Create Shareable Access Key(Optioal)

A shared access key with specific restrictions can be generated using the following code:

```py
# set permissions for the new access to be created
permissions = Permission()
permissions.allow_list = True
permissions.allow_delete = False

# set shared prefix as list of dictionaries for the new access to be created
shared_prefix = [{"bucket": MY_BUCKET, "prefix": ""}]

# create new access
new_access_result, err = StorjObj.access_share(access_result.access, permissions, shared_prefix)
if err is not None:
    print(err)
    sys.exit()

# generate serialized access to share
serialized_access_result, err = StorjObj.access_serialize(new_access_result.access)
if err is not None:
    print(err)
    sys.exit()
```

## Step 9: Close Project

Once you have performed all the required operations, closing the project is must to avoid memory leaks.

```py
err = StorjObj.close_project(project_result.project)
if err is not None:
    print(err)
    sys.exit()
```

> NOTE: For more binding functions refer to the [uplink-python Binding Functions](/library.md) and for implemtation purpose refer *hello_storj.py* file.
