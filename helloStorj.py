from storjPython.uplinkPython import *
from datetime import datetime

"""
example function to put/upload data from srcFullFileName (at local computer) to 
Storj (V3) bucket's path
"""


def upload_file(storjObj, bucketHandle, uploadPath, uploadOptions, srcFullFileName):
    #
    # open file to be uploaded
    file_handle = open(srcFullFileName, 'r+b')
    data_len = os.path.getsize(srcFullFileName)
    #
    # call to get uploader handle
    uploader, ls_Error = storjObj.upload(bucketHandle, uploadPath, uploadOptions)
    if ls_Error is not None:
        return False, ls_Error
    #
    # initialize local variables and start uploading packets of data
    uploaded_total = 0
    while uploaded_total < data_len:
        # set packet size to be used while uploading
        size_to_write = 256 if (data_len - uploaded_total > 256) else data_len - uploaded_total
        #
        # exit while loop if nothing left to upload
        if size_to_write == 0:
            break
        #
        # file reading process from the last read position
        file_handle.seek(uploaded_total)
        lc_dataToWrite = file_handle.read(size_to_write)
        #
        # --------------------------------------------
        # data conversion to type required by function
        # get size of data in c type int32 variable
        lc_data_size = c_int32(len(lc_dataToWrite))
        # conversion of read bytes data to c type ubyte Array
        lc_dataToWrite = (c_uint8 * lc_data_size.value)(*lc_dataToWrite)
        # conversion of c type ubyte Array to LP_c_ubyte required by upload write function
        lc_dataToWritePtr = cast(lc_dataToWrite, POINTER(c_uint8))
        # --------------------------------------------
        #
        # call to write data to Storj bucket
        write_size, ls_Error = storjObj.upload_write(uploader, lc_dataToWritePtr, size_to_write)
        if ls_Error is not None:
            return False, ls_Error
        #
        # exit while loop if nothing left to upload / unable to upload
        if write_size == 0:
            break
        # update last read location
        uploaded_total += write_size

    # commit upload data to bucket
    ls_Error = storjObj.upload_commit(uploader)
    #
    # if error occurred
    if ls_Error is not None:
        return False, ls_Error
    else:
        return True, None


"""
example function to get/download Storj(V3) object's data and store it in given file 
with destFullFileName (on local computer)
"""


def download_file(storjObj, bucketHandle, storjPath, destFullPathName):
    #
    # open / create file with the given name to save the downloaded data
    file_handle = open(destFullPathName, 'w+b')
    #
    # call to get downloader handle
    downloader, ls_Error = storjObj.download(bucketHandle, storjPath)
    if ls_Error is not None:
        return False, ls_Error
    #
    # set packet size to be used while downloading
    size_to_read = 256
    # initialize local variables and start downloading packets of data
    downloaded_total = 0
    retry_count = 0
    while True:
        # call to read data from Storj bucket
        lc_dataReadPtr, read_size, ls_Error = storjObj.download_read(downloader, size_to_read)
        if ls_Error is not None:
            return False, ls_Error
        #
        # file writing process from the last written position if new data is downloaded
        written_size = 0
        if read_size != 0:
            #
            # --------------------------------------------
            # data conversion to type python readable form
            # conversion of LP_c_ubyte to python readable data variable
            lc_dataRead = string_at(lc_dataReadPtr, read_size)
            # --------------------------------------------
            #
            file_handle.seek(downloaded_total)
            written_size = file_handle.write(lc_dataRead)
        #
        # exit while loop if file is read completely
        if read_size == 0:
            break
        #
        # retry if write to file failed
        if written_size == 0:
            if retry_count < 5:
                retry_count += 1
                continue
            else:
                storjObj.download_close(downloader)
                return False, "File download failed. Please try again."
        #
        retry_count = 0
        # update last read location
        downloaded_total += read_size

    # close downloader and free downloader access
    ls_Error = storjObj.download_close(downloader)
    #
    # if error occurred
    if ls_Error is not None:
        return False, ls_Error
    else:
        return True, None


if __name__ == "__main__":

    # Storj configuration information
    myAPIKey = "change-me-to-the-api-key-created-in-satellite-gui"
    satellite = "us-central-1.tardigrade.io:7777"
    myBucket = "my-first-bucket"
    myStorjUploadPath = "(optional): path / (required): filename"  # (path + filename) OR filename
    myEncryptionPassphrase = "you'll never guess this"

    # Source and destination path and file name for testing
    srcFullFileName = "filename with extension of source file on local system"
    destFullFileName = "filename with extension to save on local system"

    # create an object of libUplinkPy class
    StorjObj = libUplinkPy()

    # function calls
    # create new uplink
    print("\nSetting-up new uplink...")
    uplinkHandle, err = StorjObj.new_uplink()
    if err is not None:
        print(err)
        exit()
    print("New uplink: SET-UP!")
    #

    # parse Api Key
    print("\nParsing the API Key...")
    parseApiKeyHandle, err = StorjObj.parse_api_key(myAPIKey)
    if err is not None:
        print(err)
        exit()
    print("API Key: PARSED!")
    #

    # open Storj project
    print(
        "\nOpening the Storj project, corresponding to the parsed API Key, on " + satellite + " satellite...")
    projectHandle, err = StorjObj.open_project(uplinkHandle, parseApiKeyHandle, satellite)
    if err is not None:
        print(err)
        exit()
    print("Desired Storj project: OPENED!")
    #

    # enlist all the buckets in given Storj project
    print("\nListing bucket's names and creation time...")
    bucketsList, err = StorjObj.list_buckets(projectHandle, None)
    if err is not None:
        print(err)
        exit()
    else:
        # print all bucket name and creation time
        for i in range(bucketsList.length):
            if bucketsList.items[i].name is None:
                break
            print(bucketsList.items[i].name.decode('utf-8'), " | ",
                  datetime.fromtimestamp(bucketsList.items[i].created))
        print("Buckets listing: COMPLETE!")
    #

    # free memory utilized by bucket list pointer object
    err = StorjObj.free_bucket_list(bucketsList)
    if err is not None:
        print(err)
        exit()
    # delete bucket list object
    del bucketsList
    #

    # delete given bucket
    print("\nDeleting '" + myBucket + "' bucket...")
    err = StorjObj.delete_bucket(projectHandle, myBucket)
    if err is not None:
        print(err)
        exit()
    print("Desired bucket: DELETED")
    #

    # set bucket config according to this link:
    # https://godoc.org/storj.io/storj/lib/uplink#BucketConfig
    lO_configBucket = BucketConfig()
    lO_configBucket.path_cipher = STORJ_ENC_AESGCM
    lO_configBucket.encryption_parameters.cipher_suite = STORJ_ENC_AESGCM
    lO_configBucket.encryption_parameters.block_size = 7424
    lO_configBucket.redundancy_scheme.algorithm = STORJ_REED_SOLOMON
    lO_configBucket.redundancy_scheme.share_size = 256
    lO_configBucket.redundancy_scheme.required_shares = 29
    lO_configBucket.redundancy_scheme.repair_shares = 35
    lO_configBucket.redundancy_scheme.optimal_shares = 80
    lO_configBucket.redundancy_scheme.total_shares = 130
    # create bucket in given project with above configuration or None
    print("\nCreating '" + myBucket + "' bucket...")
    bucketHandle, err = StorjObj.create_bucket(projectHandle, myBucket, lO_configBucket)
    if err is not None:
        print(err)
        exit()
    print("Desired Bucket: CREATED!")
    # free and delete bucket configuration object
    lO_configBucket = None
    del lO_configBucket
    #

    # get encryption access to upload and download data
    print("\nCreating serialized encryption key...")
    serializedEncryptionAccess, err = StorjObj.get_encryption_access(projectHandle, myEncryptionPassphrase)
    if err is not None:
        print(err)
        exit()
    print("Serialized encryption key: CREATED!")
    #

    # as an example of how to create shareable Scope key for easy storj access without API key and Encryption PassPhrase
    # create new Scope
    print("\nCreating new Scope...")
    newScopeHandle, err = StorjObj.new_scope(satellite, parseApiKeyHandle, serializedEncryptionAccess)
    if err is not None:
        print(err)
        exit()
    print("New Scope: CREATED!")

    # generate serialized Scope key
    print("\nGenerating serialized Scope key...")
    serializedScope, err = StorjObj.serialize_scope(newScopeHandle)
    if err is not None:
        print(err)
        exit()
    print("Serialized Scope key: ", serializedScope)
    #

    # as an example of how to retrieve information from shareable Scope key for storj access
    # retrieving Scope from serialized Scope key
    print("\nParsing serialized Scope key...")
    parsedScope, err = StorjObj.parse_scope(serializedScope)
    if err is not None:
        print(err)
        exit()
    print("Parsing Scope key: COMPLETE")
    #

    # retrieving satellite from Scope
    print("\nRetrieving satellite address from Scope...")
    satelliteFromScope, err = StorjObj.get_scope_satellite_address(parsedScope)
    if err is not None:
        print(err)
        exit()
    print("Satellite address from Scope: ", satelliteFromScope)
    #

    # open bucket in given project with given name and access
    print("\nOpening '" + myBucket + "' bucket...")
    bucketHandle, err = StorjObj.open_bucket(projectHandle, serializedEncryptionAccess, myBucket)
    if err is not None:
        print(err)
        exit()
    print("Desired bucket: OPENED!")
    #

    # as an example of 'put' , lets read and upload a local file
    # upload file/object
    print("\nUploading data...")
    uploadStatus, err = upload_file(StorjObj, bucketHandle, myStorjUploadPath, None, srcFullFileName)
    if err is not None or uploadStatus is False:
        print(err)
        exit()
    print("Upload: COMPLETE!")
    #

    # as an example of 'get' , lets download an object and write it to a local file
    # download file/object
    print("\nDownloading data...")
    downloadStatus, err = download_file(StorjObj, bucketHandle, myStorjUploadPath, destFullFileName)
    if err is not None or downloadStatus is False:
        print(err)
        exit()
    print("Download: COMPLETE!")
    #

    # set list options before calling list objects (optional)
    lO_listOption = ListOptions()
    lO_listOption.prefix = c_char_p("".encode('utf-8'))
    lO_listOption.cursor = c_char_p("".encode('utf-8'))
    lO_listOption.delimiter = c_char(' '.encode('utf-8'))
    lO_listOption.recursive = True
    lO_listOption.direction = STORJ_AFTER
    lO_listOption.limit = 0
    # list objects in given bucket with above options or None
    print("\nListing object's names...")
    objectsList, err = StorjObj.list_objects(bucketHandle, lO_listOption)
    if err is not None:
        print(err)
        exit()
    else:
        # print all objects path
        for i in range(objectsList.length):
            if objectsList.items[i].path is None:
                break
            print(objectsList.items[i].path.decode('utf-8'))
        print("Objects listing: COMPLETE!")
    # free and delete bucket configuration object
    lO_listOption = None
    del lO_listOption
    #

    # free memory utilized by object list pointer object
    err = StorjObj.free_list_objects(objectsList)
    if err is not None:
        print(err)
        exit()
    # delete bucket list object
    del objectsList
    #

    # delete given object
    print("\nDeleting '" + myStorjUploadPath + "' object...")
    err = StorjObj.delete_object(bucketHandle, myStorjUploadPath)
    if err is not None:
        print(err)
        exit()
    print("Desired object: DELETED!")
    #

    # close given bucket using handle
    print("\nClosing bucket...")
    err = StorjObj.close_bucket(bucketHandle)
    if err is not None:
        print(err)
        exit()
    print("Bucket CLOSED!")
    #

    # close given project using handle
    print("\nClosing Storj project...")
    err = StorjObj.close_project(projectHandle)
    if err is not None:
        print(err)
        exit()
    print("Project CLOSED!")
    #

    # close given uplink using handle
    print("\nClosing uplink...")
    err = StorjObj.close_uplink(uplinkHandle)
    if err is not None:
        print(err)
        exit()
    print("Uplink CLOSED!")
    #
