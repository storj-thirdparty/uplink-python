from storjPython import uplinkPython

if __name__ == "__main__":

    # Storj configuration information
    myAPIKey = "change-me-to-the-api-key-created-in-satellite-gui"
    satellite = "mars.tardigrade.io:7777"
    myBucket = "my-first-bucket"
    myStorjUploadPath = "(optional): path / (required): filename"  # (path + filename) OR filename
    myEncryptionPassphrase = "you'll never guess this"

    # Source and destination path and file name for testing
    srcFullFileName = "filename with extension of source file on local system"
    destFullFileName = "filename with extension to save on local system"

    # create an object of libUplinkPy class
    StorjObj = uplinkPython.libUplinkPy()

    # function calls
    uplinkHandle, err = StorjObj.new_uplink()
    if err is not None:
        print(err)
        exit()

    parseApiKeyHandle, err = StorjObj.parse_api_key(myAPIKey)
    if err is not None:
        print(err)
        exit()

    projectHandle, err = StorjObj.open_project(uplinkHandle, parseApiKeyHandle, satellite)
    if err is not None:
        print(err)
        exit()

    serializedEncryptionAccess, err = StorjObj.get_encryption_access(projectHandle, myEncryptionPassphrase)
    if err is not None:
        print(err)
        exit()

    # set bucket config according to this link:
    # https://godoc.org/storj.io/storj/lib/uplink#BucketConfig
    configBucket = uplinkPython.BucketConfig()
    configBucket.path_cipher = uplinkPython.STORJ_ENC_AESGCM
    configBucket.encryption_parameters.cipher_suite = uplinkPython.STORJ_ENC_AESGCM
    configBucket.encryption_parameters.block_size = 7424
    configBucket.redundancy_scheme.algorithm = uplinkPython.STORJ_REED_SOLOMON
    configBucket.redundancy_scheme.share_size = 256
    configBucket.redundancy_scheme.required_shares = 29
    configBucket.redundancy_scheme.repair_shares = 35
    configBucket.redundancy_scheme.optimal_shares = 80
    configBucket.redundancy_scheme.total_shares = 130

    bucketHandle, err = StorjObj.create_bucket(projectHandle, myBucket, configBucket)
    if err is not None:
        print(err)
        exit()

    bucketHandle, err = StorjObj.open_bucket(projectHandle, serializedEncryptionAccess, myBucket)
    if err is not None:
        print(err)
        exit()

    uploadStatus, err = StorjObj.upload_file(bucketHandle, myStorjUploadPath, srcFullFileName)
    if err is not None or uploadStatus is False:
        print(err)
        exit()

    downloadStatus, err = StorjObj.download_file(bucketHandle, myStorjUploadPath, destFullFileName)
    if err is not None or downloadStatus is False:
        print(err)
        exit()

    err = StorjObj.close_bucket(bucketHandle)
    if err is not None:
        print(err)
        exit()

    err = StorjObj.close_project(projectHandle)
    if err is not None:
        print(err)
        exit()

    err = StorjObj.close_uplink(uplinkHandle)
    if err is not None:
        print(err)
        exit()
