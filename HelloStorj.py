from UplinkPython import libUplinkPy
import json

if __name__ == "__main__":

    #load default data from Storj config file
    with open("storj_config.json") as json_file:
        storj_config = json.load(json_file)

    #local variables with value from config file
    apikey = storj_config['apikey']
    satellite = storj_config['satellite']
    bucket = storj_config['bucket']
    uploadPath = storj_config['uploadPath']
    encryptionpassphrase = storj_config['encryptionpassphrase']

    #Source and destination path and file name for testing
    srcFullFileName = "SampleData.txt"
    destFullPathName = "DownloadedFile.txt"

    debugMode = True

    #create an object of libUplinkPy class
    StorjObj = libUplinkPy(debugMode)

    #function calls
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
