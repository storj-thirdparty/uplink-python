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

Next, you need to create an object of Uplink class that will be used to call the libuplink functions.

```py
from uplink_python.uplink import Uplink

uplink = Uplink()
```

## Step 4: Create Access Handle

Once you have initialized the Uplink class object, you need to create an access to storj network in the following way:

```py
access = uplink.request_access_with_passphrase(MY_SATELLITE, MY_API_KEY, MY_ENCRYPTION_PASSPHRASE)
```

## Step 5: Open Project

To perform the uplink operations you need to create a project, which can be done using the following code fragmeent:

```py
project = access.open_project()
```

## Step 6: Create/Ensure Bucket

All the uploading and downloading is performed inside and from a bucket on the storj network. To ensure that the bucket you have specified in your configurations above exists or create one if not, use the following code:

```py
bucket = project.ensure_bucket(MY_BUCKET)
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
upload = project.upload_object(MY_BUCKET, MY_STORJ_UPLOAD_PATH)
```

You can pass an optional parameter *upload_options* by referring to the [libuplink documentation](https://godoc.org/storj.io/uplink) or simply pass *none*.

#### Stream data to Storj Network

Once the source and destination streams are created, its time to perform data streaming, this can be done in two ways:

##### 1. Upload data by providing data bytes and size:

```py
uploaded_total = 0
while uploaded_total < data_len:
    # set packet size to be used while uploading
    size_to_write = 256 if (data_len - uploaded_total > 256) else data_len - uploaded_total

    # exit while loop if nothing left to upload
    if size_to_write == 0:
        break

    # file reading process from the last read position
    data_to_write = file_handle.read(size_to_write)

    # call to write data to Storj bucket
    bytes_written = upload.write(data_to_write, size_to_write)

    # exit while loop if nothing left to upload / unable to upload
    if bytes_written == 0:
        break

    # update last read location
    uploaded_total += bytes_written
```

The above code streams the data in chunks of 256 bytes. You can change this size as per your requirement and convenience.

##### 2. Upload data by providing file handle:

```py
# file_handle should be a BinaryIO, i.e. file should be opened using 'r+b" flag.
upload.write_file(file_handle)
```
An option parameter here is buffer_size (default = 0), if not passes would iterate throught the file and upload in blocks with appropriate buffer size based on system.

#### Commit Upload

Once the data has been successfully streamed, the upload needs to be committed using the following method:

```py
upload.commit()
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
download = project.download_object(MY_BUCKET, MY_STORJ_UPLOAD_PATH)
```

You can pass an optional parameter *download_options* by referring to the [libuplink documentation](https://godoc.org/storj.io/uplink) or simply pass *none*.

#### Stream data from Storj Network

Once the source and destination streams are created, its time to perform data streaming, this can be done in two ways:

##### 1. Downloading data by providing size_to_read:

In this method we would provide size of data to be read from stream and maintaining a loop (if required) and writing the data to file ourself.

Before streaming the data we need to know the amount of data we are downloading to avoid discrepancies. Fetching the data size can be done using the following code:

```py
# find size of object to be downloaded
file_size = upload.file_size()
```

Now, its time to do the required downloading and can be done as follows:

```py
# set packet size to be used while downloading
size_to_read = 256
# initialize local variables and start downloading packets of data
downloaded_total = 0
while True:
    # call to read data from Storj bucket
    data_read, bytes_read = download.read(size_to_read)
   
    # file writing process from the last written position if new data is downloaded
    if bytes_read != 0:
        file_handle.write(data_read)
    #
    # update last read location
    downloaded_total += bytes_read
    #
    # break if download complete
    if downloaded_total == file_size:
        break
```

The above code streams the data in chunks of 256 bytes. You can change this size as per your requirement and convenience.

##### 2. Downloading data by providing file handle:

```py
# file_handle should be a BinaryIO, i.e. file should be opened using 'w+b" flag.
download.read_file(file_handle)
```
An option parameter here is buffer_size (default = 0), if not passes would iterate throught the object and write the data to file in blocks with appropriate buffer size based on system.

#### Close Download Stream

Once the download streaming is complete, its important to close the download stream.

```py
download.close()
```

> NOTE: Perform error handling as per your implmentation.

> NOTE: Alternatively, you can simple create a method(s) that can be called from the main method and performs all the above steps internally as done in the sample file.

## Step 8: Create Shareable Access Key(Optioal)

A shared access key with specific restrictions can be generated using the following code:

```py
# set permissions for the new access to be created
permissions = Permission(allow_list=True, allow_delete=False)

# set shared prefix as list of SharePrefix for the new access to be created
shared_prefix = [SharePrefix(bucket=MY_BUCKET, prefix="")]

# create new access
new_access = access.share(permissions, shared_prefix)

# generate serialized access to share
serialized_access = access.serialize()
```

## Step 9: Close Project

Once you have performed all the required operations, closing the project is must to avoid memory leaks.

```py
project.close()
```

> NOTE: For more binding functions refer to the [uplink-python Binding Functions](/library.md) and for implemtation purpose refer *hello_storj.py* file.
