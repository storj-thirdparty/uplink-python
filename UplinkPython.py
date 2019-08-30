##################################
# Python Bindings for Storj (V3) #
##################################

from ctypes import *


##############################################
# Structure classes for go structure objects #
##############################################

# Uplink configuration nested structure
class tls(Structure):
    _fields_ = [("skip_peer_ca_whitelist", c_bool)]


class Volatile(Structure):
    _fields_ = [("tls", tls)]


class UplinkConfig(Structure):
    _fields_ = [("Volatile", Volatile)]


# Uplink reference structure
class UplinkRef(Structure):
    _fields_ = [("_handle", c_long)]


# API key reference structure
class APIKeyRef(Structure):
    _fields_ = [("_handle", c_long)]


# Project reference structure
class ProjectRef(Structure):
    _fields_ = [("_handle", c_long)]


# Access reference structure
class EncryptionAccessRef(Structure):
    _fields_ = [("_handle", c_long)]


# Bucket reference structure
class BucketRef(Structure):
    _fields_ = [("_handle", c_long)]


#########################################################
# Python Storj class with all Storj functions' bindings #
#########################################################

class libUplinkPy:
    def __init__(self, pb_DEBUG_MODE):
        # private members of PyStorj class with reference objects
        # include the golang exported libuplink library functions
        self.m_libUplink = CDLL('libuplinkc.so')
        self.mO_uplinkRef = None
        self.mO_apiKeyParsedRef = None
        self.mO_projectRef = None
        self.mO_accessRef = None
        self.mO_bucketRef = None
        # error pointer
        self.m_error = c_char_p()
        # debug mode
        self.mb_DEBUG_MODE = False
        if pb_DEBUG_MODE is not None:
            self.mb_DEBUG_MODE = pb_DEBUG_MODE

    """
    function to create new Storj uplink
    pre-requisites: none
    inputs: none
    output: returns true, if successful, else false
    """

    def new_uplink(self):
        if self.mb_DEBUG_MODE:
            print("\nSetting-up new uplink...")
        #
        # set-up uplink configuration
        lO_uplinkConfig = UplinkConfig()
        lO_uplinkConfig.Volatile.tls.skip_peer_ca_whitelist = True
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.uplink_custom.argtypes = [UplinkConfig, POINTER(c_char_p)]
        self.m_libUplink.uplink_custom.restype = UplinkRef
        # re-initialize error ref pointer
        self.m_error = c_char_p()
        #
        # create new uplink by calling the exported golang function
        self.mO_uplinkRef = self.m_libUplink.uplink_custom(lO_uplinkConfig, byref(self.m_error))
        # if error occurred
        if self.m_error.value is not None:
            print(self.m_error.value.decode("utf-8"))
            return False
        else:
            if self.mb_DEBUG_MODE:
                print("New uplink: SET-UP!")
            return True

    """
    function to parse API key, to be used by Storj
    pre-requisites: none
    inputs: API key (string)
    output: returns true, if successful, else false
    """

    def parse_api_key(self, ps_API_Key):
        if self.mb_DEBUG_MODE:
            print("\nParsing the API Key: ", ps_API_Key, " ...")
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.parse_api_key.argtypes = [c_char_p, POINTER(c_char_p)]
        self.m_libUplink.parse_api_key.restype = APIKeyRef
        #
        # prepare the input for the function
        lc_ApiKeyPtr = c_char_p(ps_API_Key.encode('utf-8'))
        # re-initialize error ref pointer
        self.m_error = c_char_p()
        # parse the API key by calling the exported golang function
        self.mO_apiKeyParsedRef = self.m_libUplink.parse_api_key(lc_ApiKeyPtr, byref(self.m_error))
        # if error occurred
        if self.m_error.value is not None:
            print(self.m_error.value.decode("utf-8"))
            return False
        else:
            if self.mb_DEBUG_MODE:
                print("API Key: PARSED!")
            return True

    """
    function to open a Storj project
    pre-requisites: new_uplink() and parse_api_key() functions have been already called
    inputs: Satellite Address (string)
    output: returns true, if successful, else false
    """

    def open_project(self, ps_satelliteAddress):
        if self.mb_DEBUG_MODE:
            print("\nOpening the Storj project, corresponding to the parsed API Key, on ",
                  ps_satelliteAddress, " satellite...")
        #
        # ensure uplink and parsed API key objects are already created
        if self.mO_uplinkRef is None:
            print("ERROR: An uplink is NOT yet created using 'new_uplink()' function.")
            return False
        if self.mO_apiKeyParsedRef is None:
            print("ERROR: API key is NOT yet parsed using 'parse_api_key(string)' function.")
            return False
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.open_project.argtypes = [UplinkRef, c_char_p, APIKeyRef, POINTER(c_char_p)]
        self.m_libUplink.open_project.restype = ProjectRef
        #
        # prepare the input for the function
        lc_satelliteAddressPtr = c_char_p(ps_satelliteAddress.encode('utf-8'))
        # re-initialize error ref pointer
        self.m_error = c_char_p()
        # open project by calling the exported golang function
        self.mO_projectRef = self.m_libUplink.open_project(self.mO_uplinkRef, lc_satelliteAddressPtr,
                                                           self.mO_apiKeyParsedRef,
                                                           byref(self.m_error))
        # if error occurred
        if self.m_error.value is not None:
            print(self.m_error.value.decode("utf-8"))
            return False
        else:
            if self.mb_DEBUG_MODE:
                print("Desired Storj project: OPENED!")
            return True

    """
    function to get encryption access to upload and download data on Storj
    pre-requisites: open_project() function has been already called
    inputs: Encryption Pass Phrase (string)
    output: returns true, if successful, else false
    """

    def get_encryption_access(self, ps_encryptionPassPhrase):
        if self.mb_DEBUG_MODE:
            print("\nCreating encryption key!")
        #
        # ensure projectRef object is already created
        if self.mO_projectRef is None:
            print("ERROR: Storj project is NOT yet opened using 'open_project()' function.")
            return False
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.encryption_key_custom.argtypes = [ProjectRef, c_char_p, POINTER(c_char_p)]
        self.m_libUplink.encryption_key_custom.restype = EncryptionAccessRef
        #
        # prepare the input for the function
        lc_encryptionPassPhrasePtr = c_char_p(ps_encryptionPassPhrase.encode('utf-8'))
        # re-initialize error ref pointer
        self.m_error = c_char_p()
        # get encryption key by calling the exported golang function
        self.mO_accessRef = self.m_libUplink.encryption_key_custom(self.mO_projectRef, lc_encryptionPassPhrasePtr,
                                                                   byref(self.m_error))
        # if error occurred
        if self.m_error.value is not None:
            print(self.m_error.value.decode("utf-8"))
            return False
        else:
            if self.mb_DEBUG_MODE:
                print("Encryption key: CREATED!")
            return True

    """
    function to open an already existing bucket in Storj project
    pre-requisites: get_encryption_access() function has been already called
    inputs: Bucket Name (string)
    output: returns true, if successful, else false
    """

    def open_bucket(self, ps_bucketName):
        if self.mb_DEBUG_MODE:
            print("\nOpening '", ps_bucketName, "' bucket...")
        #
        # ensure accessRef object is already created
        if self.mO_accessRef is None:
            print("ERROR: Encryption access is NOT yet created using 'get_encryption_access()' function.")
            return False
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.open_bucket_custom.argtypes = [ProjectRef, c_char_p, EncryptionAccessRef, POINTER(c_char_p)]
        self.m_libUplink.open_bucket_custom.restype = BucketRef
        #
        # prepare the input for the function
        lc_bucketNamePtr = c_char_p(ps_bucketName.encode('utf-8'))
        # re-initialize error ref pointer
        self.m_error = c_char_p()
        # open bucket by calling the exported golang function
        self.mO_bucketRef = self.m_libUplink.open_bucket_custom(self.mO_projectRef, lc_bucketNamePtr, self.mO_accessRef,
                                                                byref(self.m_error))
        # if error occurred
        if self.m_error.value is not None:
            print(self.m_error.value.decode("utf-8"))
            return False
        else:
            if self.mb_DEBUG_MODE:
                print("Desired bucket: OPENED!")
            return True

    """
    function to upload data from srcFullFileName (at local computer) to Storj (V3) bucket's path
    pre-requisites: open_bucket() function has been already called
    inputs: Storj Path/File Name (string) within the opened bucket, local Source Full File Name(string)
    output: returns true, if successful, else false
    """

    def upload(self, ps_storjPath, ps_srcFullFileName):
        if self.mb_DEBUG_MODE:
            print("\nUploading data.....")
        #
        # ensure bucketRef object is already created
        if self.mO_bucketRef is None:
            print("ERROR: Bucket is NOT yet opened using 'open_bucket()' function.")
            return False
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.upload_custom.argtypes = [BucketRef, c_char_p, c_char_p, POINTER(c_char_p)]
        self.m_libUplink.upload_custom.restype = None
        #
        # prepare the inputs for the function
        lc_storjPathPtr = c_char_p(ps_storjPath.encode('utf-8'))
        lc_srcFullFileNamePtr = c_char_p(ps_srcFullFileName.encode('utf-8'))
        # re-initialize error ref pointer
        self.m_error = c_char_p()
        # upload file by calling the exported golang function
        self.m_libUplink.upload_custom(self.mO_bucketRef, lc_storjPathPtr, lc_srcFullFileNamePtr, byref(self.m_error))
        # if error occurred
        if self.m_error.value is not None:
            print(self.m_error.value.decode("utf-8"))
            return False
        else:
            if self.mb_DEBUG_MODE:
                print("Upload SUCCESSFUL!")
            return True

    """
    function to download Storj (V3) object's data and store it in given file with destFullFileName (on local computer)
    pre-requisites: open_bucket() function has been already called
    inputs: Storj Path/File Name (string) within the opened bucket, local Destination Full Path Name(string)
    output: returns true, if successful, else false
    """

    def download(self, ps_storjPath, ps_destFullPathName):
        if self.mb_DEBUG_MODE:
            print("\nDownloading data.....")
        #
        # ensure bucketRef object is already created
        if self.mO_bucketRef is None:
            print("ERROR: Bucket is NOT yet opened using 'open_bucket()' function.")
            return False
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.download_custom.argtypes = [BucketRef, c_char_p, c_char_p, POINTER(c_char_p)]
        self.m_libUplink.download_custom.restype = None
        #
        # prepare the inputs for the function
        lc_storjPathPtr = c_char_p(ps_storjPath.encode('utf-8'))
        lc_destFullPathNamePtr = c_char_p(ps_destFullPathName.encode('utf-8'))
        # re-initialize error ref pointer
        self.m_error = c_char_p()
        # download file by calling the exported golang function
        self.m_libUplink.download_custom(self.mO_bucketRef, lc_storjPathPtr, lc_destFullPathNamePtr,
                                         byref(self.m_error))
        # if error occurred
        if self.m_error.value is not None:
            print(self.m_error.value.decode("utf-8"))
            return False
        else:
            if self.mb_DEBUG_MODE:
                print("Download SUCCESSFUL!")
            return True

    """
    function to create new bucket in Storj project
    pre-requisites: open_project() function has been already called
    inputs: Bucket Name (string)
    output: returns true, if successful, else false
    """

    def create_bucket(self, ps_bucketName):
        if self.mb_DEBUG_MODE:
            print("\nCreating '", ps_bucketName, "' bucket...")
        #
        # ensure projectRef object is already created
        if self.mO_projectRef is None:
            print("ERROR: Storj project is NOT yet opened using 'open_project()' function.")
            return False
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.create_bucket_custom.argtypes = [ProjectRef, c_char_p, POINTER(c_char_p)]
        self.m_libUplink.create_bucket_custom.restype = None
        #
        # prepare the input for the function
        lc_BucketName = c_char_p(ps_bucketName.encode('utf-8'))
        # re-initialize error ref pointer
        self.m_error = c_char_p()
        #  by calling the exported golang function
        self.mO_bucketRef = self.m_libUplink.create_bucket_custom(self.mO_projectRef, lc_BucketName,
                                                                  byref(self.m_error))
        # if error occurred
        if self.m_error.value is not None:
            return False
        else:
            if self.mb_DEBUG_MODE:
                print("Desired Bucket: CREATED!")
            return True

    """
    function to close currently opened Bucket
    pre-requisites: open_bucket() function has been already called, successfully
    inputs: none
    output: returns true, if successful, else false
    """

    def close_bucket(self):
        if self.mb_DEBUG_MODE:
            print("\nClosing bucket...")
        #
        # ensure bucketRef object is already created
        if self.mO_bucketRef is None:
            print("ERROR: Bucket is NOT yet opened using 'open_bucket()' function.")
            return False
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.close_bucket.argtypes = [BucketRef, POINTER(c_char_p)]
        self.m_libUplink.close_bucket.restype = None
        # re-initialize error ref pointer
        self.m_error = c_char_p()
        #
        # close bucket by calling the exported golang function
        self.m_libUplink.close_bucket(self.mO_bucketRef, byref(self.m_error))
        # if error occurred
        if self.m_error.value is not None:
            print(self.m_error.value.decode("utf-8"))
            return False
        else:
            if self.mb_DEBUG_MODE:
                print("Bucket CLOSED!")
            self.mO_bucketRef = None
            return True

    """
    function to close currently opened Storj project
    pre-requisites: open_project() function has been already called
    inputs: none
    output: returns true, if successful, else false
    """

    def close_project(self):
        if self.mb_DEBUG_MODE:
            print("\nClosing Storj project...")
        #
        # ensure projectRef object is already created
        if self.mO_projectRef is None:
            print("ERROR: Storj project is NOT yet opened using 'open_project()' function.")
            return False
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.close_project.argtypes = [ProjectRef, POINTER(c_char_p)]
        self.m_libUplink.close_project.restype = None
        # re-initialize error ref pointer
        self.m_error = c_char_p()
        #
        # close Storj project by calling the exported golang function
        self.m_libUplink.close_project(self.mO_projectRef, byref(self.m_error))
        # if error occurred
        if self.m_error.value is not None:
            print(self.m_error.value.decode("utf-8"))
            return False
        else:
            if self.mb_DEBUG_MODE:
                print("Project CLOSED!")
            self.mO_projectRef = None
            return True

    """
    function to close currently opened uplink
    pre-requisites: new_uplink() function has been already called
    inputs: none
    output: returns true, if successful, else false
    """

    def close_uplink(self):
        if self.mb_DEBUG_MODE:
            print("\nClosing uplink...")
        #
        # ensure uplinkRef object is already created
        if self.mO_uplinkRef is None:
            print("ERROR: Uplink is NOT yet opened using 'new_uplink()' function.")
            return False
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.close_uplink.argtypes = [UplinkRef, POINTER(c_char_p)]
        self.m_libUplink.close_uplink.restype = None
        # re-initialize error ref pointer
        self.m_error = c_char_p()
        #
        # cloase uplink by calling the exported golang function
        self.m_libUplink.close_uplink(self.mO_uplinkRef, byref(self.m_error))
        # if error occurred
        if self.m_error.value is not None:
            print(self.m_error.value.decode("utf-8"))
            return False
        else:
            if self.mb_DEBUG_MODE:
                print("Uplink CLOSED!")
            self.mO_uplinkRef = None
            return True
