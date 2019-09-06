from UplinkPython import libUplinkPy
import json

if __name__ == "__main__":

    # Storj configuration information
    apikey = "13Yqf9SJhb9ApNZQdY2H4h47pacMyQeAtGafLUygWhTuugCU17P5BffEZveFnP8ivv2dsrWFaKPZJnRupHHgkw9abTw3hzxpHt2td5Y"
    satellite = "us-central-1.tardigrade.io:7777"
    bucket = "partnertest01"
    uploadPath = "path01/sample.txt"
    encryptionpassphrase = "test"

    # Source and destination path and file name for testing
    srcFullFileName = "SampleData.txt"
    destFullPathName = "DownloadedFile.txt"

    debugMode = True

    # create an object of libUplinkPy class
    StorjObj = libUplinkPy(debugMode)

    # function calls
    if StorjObj.new_uplink() is True:
        if StorjObj.parse_api_key(apikey) is True:
            if StorjObj.open_project(satellite) is True:
                if StorjObj.create_bucket(bucket) is True:
                    if StorjObj.get_encryption_access(encryptionpassphrase) is True:
                        if StorjObj.open_bucket(bucket) is True:
                            if StorjObj.upload(uploadPath, srcFullFileName) is True:
                                StorjObj.download(uploadPath, destFullPathName)
                            # close the opened Storj bucket
                            StorjObj.close_bucket()
                # close the opened Storj project
                StorjObj.close_project()
        # close the opened Storj uplink
        StorjObj.close_uplink()
