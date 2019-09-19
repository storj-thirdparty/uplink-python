##################################
# Python Bindings for Storj (V3) #
##################################

from ctypes import *
import os

##############################################
# Structure classes for go structure objects #
##############################################

# Defines:
# CipherSuite ENUM
(STORJ_ENC_UNSPECIFIED, STORJ_ENC_NULL, STORJ_ENC_AESGCM, STORJ_ENC_SECRET_BOX) = map(c_int, range(4))

# RedundancyAlgorithm ENUM
(STORJ_INVALID_REDUNDANCY_ALGORITHM, STORJ_REED_SOLOMON) = map(c_int, range(2))


# Uplink configuration nested structure
class TLS(Structure):
    _fields_ = [("SkipPeerCAWhitelist", c_bool)]


class Volatile(Structure):
    _fields_ = [("TLS", TLS), ("PartnerID", c_char_p)]


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


# Upload reference structure
class UploaderRef(Structure):
    _fields_ = [("_handle", c_long)]


# Download reference structure
class DownloaderRef(Structure):
    _fields_ = [("_handle", c_long)]


# Upload Options reference structure
class UploadOptions(Structure):
    pass


class EncryptionParameters(Structure):
    _fields_ = [("cipher_suite", c_int), ("block_size", c_int32)]


class RedundancyScheme(Structure):
    _fields_ = [("algorithm", c_int), ("share_size", c_int32), ("required_shares", c_int16),
                ("repair_shares", c_int16), ("optimal_shares", c_int16), ("total_shares", c_int16)]


class BucketConfig(Structure):
    _fields_ = [("path_cipher", c_int), ("encryption_parameters", EncryptionParameters),
                ("redundancy_scheme", RedundancyScheme)]


class BucketInfo(Structure):
    _fields_ = [("name", c_char_p), ("created", c_int64), ("path_cipher", c_int), ("segment_size", c_int64),
                ("encryption_parameters", EncryptionParameters), ("redundancy_scheme", RedundancyScheme)]


#########################################################
# Python Storj class with all Storj functions' bindings #
#########################################################

class libUplinkPy:
    def __init__(self):
        # private members of PyStorj class with reference objects
        # include the golang exported libuplink library functions
        so_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libuplinkc.so')
        self.m_libUplink = CDLL(so_path)

    """
    function to create new Storj uplink
    pre-requisites: none
    inputs: none
    output: Uplink Handle (long), Error (string) if any else None
    """

    def new_uplink(self):
        #
        # set-up uplink configuration
        lO_uplinkConfig = UplinkConfig()
        lO_uplinkConfig.Volatile.TLS.SkipPeerCAWhitelist = True
        ls_partnerID = "a1ba07a4-e095-4a43-914c-1d56c9ff5afd"
        lO_uplinkConfig.Volatile.PartnerID = c_char_p(ls_partnerID.encode('utf-8'))
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.new_uplink.argtypes = [UplinkConfig, POINTER(c_char_p)]
        self.m_libUplink.new_uplink.restype = UplinkRef
        # create error ref pointer
        lc_errorPtr = c_char_p()
        #
        # create new uplink by calling the exported golang function
        mO_uplinkRef = self.m_libUplink.new_uplink(lO_uplinkConfig, byref(lc_errorPtr))
        #
        # if error occurred
        if lc_errorPtr.value is not None:
            return None, lc_errorPtr.value.decode("utf-8")
        else:
            return mO_uplinkRef._handle, None

    """
    function to parse API key, to be used by Storj
    pre-requisites: none
    inputs: API key (string)
    output: Parse Api Key Handle (long), Error (string) if any else None
    """

    def parse_api_key(self, ps_API_Key):
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.parse_api_key.argtypes = [c_char_p, POINTER(c_char_p)]
        self.m_libUplink.parse_api_key.restype = APIKeyRef
        #
        # prepare the input for the function
        lc_ApiKeyPtr = c_char_p(ps_API_Key.encode('utf-8'))
        # create error ref pointer
        lc_errorPtr = c_char_p()
        # parse the API key by calling the exported golang function
        lO_apiKeyParsedRef = self.m_libUplink.parse_api_key(lc_ApiKeyPtr, byref(lc_errorPtr))
        #
        # if error occurred
        if lc_errorPtr.value is not None:
            return None, lc_errorPtr.value.decode("utf-8")
        else:
            return lO_apiKeyParsedRef._handle, None

    """
    function to open a Storj project
    pre-requisites: new_uplink() and parse_api_key() functions have been already called
    inputs: Uplink Handle (long), Api Key Parsed Handle (long), Satellite Address (string)
    output: Project Handle (long), Error (string) if any else None
    """

    def open_project(self, pl_uplinkHandle, pl_apiKeyParsedHandle, ps_satelliteAddress):
        #
        # ensure uplink and parsed API key objects are already created
        if pl_uplinkHandle <= 0:
            ls_Error = "Invalid Uplink handle, please check parameter[1] passed and try again."
            return None, ls_Error
        if pl_apiKeyParsedHandle <= 0:
            ls_Error = "Invalid ParsedApiKey handle, please check parameter[2] passed and try again."
            return None, ls_Error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.open_project.argtypes = [UplinkRef, c_char_p, APIKeyRef, POINTER(c_char_p)]
        self.m_libUplink.open_project.restype = ProjectRef
        #
        # prepare the input for the function
        lc_satelliteAddressPtr = c_char_p(ps_satelliteAddress.encode('utf-8'))
        lO_uplinkRef = UplinkRef()
        lO_uplinkRef._handle = pl_uplinkHandle
        lO_APIKeyRef = APIKeyRef()
        lO_APIKeyRef._handle = pl_apiKeyParsedHandle
        # create error ref pointer
        lc_errorPtr = c_char_p()
        # open project by calling the exported golang function
        lO_projectRef = self.m_libUplink.open_project(lO_uplinkRef, lc_satelliteAddressPtr,
                                                      lO_APIKeyRef, byref(lc_errorPtr))
        #
        # if error occurred
        if lc_errorPtr.value is not None:
            return None, lc_errorPtr.value.decode("utf-8")
        else:
            return lO_projectRef._handle, None

    """
    function to get encryption access to upload and download data on Storj
    pre-requisites: open_project() function has been already called
    inputs: Project Handle (long), Encryption Pass Phrase (string)
    output: Serialized Encryption Access Pointer (char Ptr), Error (string) if any else None
    """

    def get_encryption_access(self, pl_projectHandle, ps_encryptionPassPhrase):
        #
        # ensure project handle is valid
        if pl_projectHandle <= 0:
            ls_Error = "Invalid Storj Project handle, please check parameter[1] passed and try again."
            return None, ls_Error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.project_salted_key_from_passphrase.argtypes = [ProjectRef, c_char_p, POINTER(c_char_p)]
        self.m_libUplink.project_salted_key_from_passphrase.restype = POINTER(c_uint8)
        #
        # prepare the input for the function
        lc_encryptionPassPhrasePtr = c_char_p(ps_encryptionPassPhrase.encode('utf-8'))
        lO_ProjectRef = ProjectRef()
        lO_ProjectRef._handle = pl_projectHandle
        # create error ref pointer
        lc_errorPtr = c_char_p()
        # get encryption key by calling the exported golang function
        li_saltedKeyPtr = self.m_libUplink.project_salted_key_from_passphrase(lO_ProjectRef, lc_encryptionPassPhrasePtr,
                                                                              byref(lc_errorPtr))
        #
        # if error occurred
        if lc_errorPtr.value is not None:
            return None, lc_errorPtr.value.decode("utf-8")
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.new_encryption_access_with_default_key.argtypes = [POINTER(c_uint8)]
        self.m_libUplink.new_encryption_access_with_default_key.restype = EncryptionAccessRef
        #
        # get encryption key by calling the exported golang function
        lO_EncryptionAccessRef = self.m_libUplink.new_encryption_access_with_default_key(li_saltedKeyPtr)
        #
        # ensure encryption key handle is valid
        if lO_EncryptionAccessRef._handle <= 0:
            ls_Error = "FAILED to created encryption access from the salted key!"
            return None, ls_Error

        self.m_libUplink.serialize_encryption_access.argtypes = [EncryptionAccessRef, POINTER(c_char_p)]
        self.m_libUplink.serialize_encryption_access.restype = c_char_p
        #
        # create error ref pointer
        lc_errorPtr = c_char_p()
        # get encryption key by calling the exported golang function
        lc_serializedEncryptionAccessPtr = self.m_libUplink.serialize_encryption_access(lO_EncryptionAccessRef,
                                                                                        byref(lc_errorPtr))
        #
        # if error occurred
        if lc_errorPtr.value is not None:
            return None, lc_errorPtr.value.decode("utf-8")
        else:
            return lc_serializedEncryptionAccessPtr, None

    """
    function to open an already existing bucket in Storj project
    pre-requisites: get_encryption_access() function has been already called
    inputs: Project Handle (long), Encryption Access Handle (long), Bucket Name (string)
    output: Bucket Handle (long), Error (string) if any else None
    """

    def open_bucket(self, pl_projectHandle, pc_serializedEncryptionAccessPtr, ps_bucketName):
        #
        # ensure project handle and encryption handles are valid
        if pl_projectHandle <= 0:
            ls_Error = "Invalid Storj Project handle, please check parameter[1] passed and try again."
            return None, ls_Error
        if pc_serializedEncryptionAccessPtr is None:
            ls_Error = "Invalid Encryption Access Pointer, please check parameter[2] passed and try again."
            return None, ls_Error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.open_bucket.argtypes = [ProjectRef, c_char_p, c_char_p, POINTER(c_char_p)]
        self.m_libUplink.open_bucket.restype = BucketRef
        #
        # prepare the input for the function
        lc_bucketNamePtr = c_char_p(ps_bucketName.encode('utf-8'))
        lO_ProjectRef = ProjectRef()
        lO_ProjectRef._handle = pl_projectHandle
        lc_serializedEncryptionAccessPtr = pc_serializedEncryptionAccessPtr
        # create error ref pointer
        lc_errorPtr = c_char_p()
        # open bucket by calling the exported golang function
        lO_bucketRef = self.m_libUplink.open_bucket(lO_ProjectRef, lc_bucketNamePtr, lc_serializedEncryptionAccessPtr,
                                                    byref(lc_errorPtr))
        #
        # if error occurred
        if lc_errorPtr.value is not None:
            return None, lc_errorPtr.value.decode("utf-8")
        else:
            return lO_bucketRef._handle, None

    """
    function to get uploader handle used to upload data to Storj (V3) bucket's path
    pre-requisites: open_bucket() function has been already called
    inputs: Bucket Handle (long), Storj Path/File Name (string) within the opened bucket
    output: Uploader Handle (long), Error (string) if any else None
    """

    def upload(self, pl_bucketHandle, ps_storjPath):
        #
        # ensure bucket handle is valid
        if pl_bucketHandle <= 0:
            ls_Error = "Invalid Bucket handle, please check parameter[1] passed and try again."
            return None, ls_Error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.upload.argtypes = [BucketRef, c_char_p, c_void_p, POINTER(c_char_p)]
        self.m_libUplink.upload.restype = UploaderRef
        #
        # prepare the input for the function
        lc_storjPathPtr = c_char_p(ps_storjPath.encode('utf-8'))
        lO_BucketRef = BucketRef()
        lO_BucketRef._handle = pl_bucketHandle
        lO_UploadOptions = c_void_p()
        # create error ref pointer
        lc_errorPtr = c_char_p()
        # get uploader ref by calling the exported golang function
        lO_uploaderRef = self.m_libUplink.upload(lO_BucketRef, lc_storjPathPtr, lO_UploadOptions, byref(lc_errorPtr))
        #
        # if error occurred
        if lc_errorPtr.value is not None:
            return None, lc_errorPtr.value.decode("utf-8")
        else:
            return lO_uploaderRef._handle, None

    """
    function to write data to Storj (V3) bucket's path
    pre-requisites: upload() function has been already called
    inputs: Bucket Handle (long), Data to write obtained using file read (bytes), Size of data to write (int)
    output: Size of data written (long), Error (string) if any else None
    """

    def upload_write(self, pl_uploaderHandle, pbt_dataToWrite, pi_sizeToWrite):
        #
        # ensure uploader handle is valid
        if pl_uploaderHandle <= 0:
            ls_Error = "Invalid Uploader handle, please check parameter[1] passed and try again."
            return None, ls_Error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.upload_write.argtypes = [UploaderRef, POINTER(c_uint8), c_size_t, POINTER(c_char_p)]
        self.m_libUplink.upload_write.restype = c_size_t
        #
        # prepare the inputs for the function
        lc_dataToWrite = pbt_dataToWrite
        lc_data_size = c_int32(len(lc_dataToWrite))
        lc_dataToWrite = (c_uint8 * lc_data_size.value)(*lc_dataToWrite)
        lc_dataToWritePtr = cast(lc_dataToWrite, POINTER(c_uint8))
        lc_sizeToWrite = c_size_t(pi_sizeToWrite)
        lO_UploaderRef = UploaderRef()
        lO_UploaderRef._handle = pl_uploaderHandle
        # create error ref pointer
        lc_errorPtr = c_char_p()
        # upload data by calling the exported golang function
        lc_sizeWritten = self.m_libUplink.upload_write(lO_UploaderRef, lc_dataToWritePtr, lc_sizeToWrite,
                                                       byref(lc_errorPtr))
        #
        # if error occurred
        if lc_errorPtr.value is not None:
            return None, lc_errorPtr.value.decode("utf-8")
        else:
            return lc_sizeWritten, None

    """
    function to commit and finalize file for uploaded data to Storj (V3) bucket's path
    pre-requisites: upload() function has been already called
    inputs: Bucket Handle (long)
    output: Error (string) if any else None
    """

    def upload_commit(self, pl_uploaderHandle):
        #
        # ensure uploader handle is valid
        if pl_uploaderHandle <= 0:
            ls_Error = "Invalid Uploader handle, please check parameter[1] passed and try again."
            return ls_Error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.upload_write.argtypes = [UploaderRef, POINTER(c_char_p)]
        self.m_libUplink.upload_write.restype = None
        #
        # prepare the inputs for the function
        lO_UploaderRef = UploaderRef()
        lO_UploaderRef._handle = pl_uploaderHandle
        # create error ref pointer
        lc_errorPtr = c_char_p()
        # upload commit by calling the exported golang function
        self.m_libUplink.upload_commit(lO_UploaderRef, byref(lc_errorPtr))
        #
        # if error occurred
        if lc_errorPtr.value is not None:
            return lc_errorPtr.value.decode("utf-8")
        else:
            return None

    """
    function to get downloader handle to download Storj (V3) object's data and store it on local computer
    pre-requisites: open_bucket() function has been already called
    inputs: Bucket Handle (long), Storj Path/File Name (string) within the opened bucket
    output: Downloader Handle (long), Error (string) if any else None
    """

    def download(self, pl_bucketHandle, ps_storjPath):
        #
        # ensure bucket handle is valid
        if pl_bucketHandle <= 0:
            ls_Error = "Invalid Bucket handle, please check parameter[1] passed and try again."
            return None, ls_Error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.download.argtypes = [BucketRef, c_char_p, POINTER(c_char_p)]
        self.m_libUplink.download.restype = DownloaderRef
        #
        # prepare the input for the function
        lc_storjPathPtr = c_char_p(ps_storjPath.encode('utf-8'))
        lO_BucketRef = BucketRef()
        lO_BucketRef._handle = pl_bucketHandle
        # create error ref pointer
        lc_errorPtr = c_char_p()
        # get downloader ref by calling the exported golang function
        lO_downloaderRef = self.m_libUplink.download(lO_BucketRef, lc_storjPathPtr, byref(lc_errorPtr))
        #
        # if error occurred
        if lc_errorPtr.value is not None:
            return None, lc_errorPtr.value.decode("utf-8")
        else:
            return lO_downloaderRef._handle, None

    """
    function to read Storj (V3) object's data and return the data
    pre-requisites: download() function has been already called
    inputs: Bucket Handle (long), Length of data to read (int)
    output: Size of data downloaded (int), Error (string) if any else None
    """

    def download_read(self, pl_downloaderHandle, pi_sizeToRead):
        #
        # ensure downloader handle is valid
        if pl_downloaderHandle <= 0:
            ls_Error = "Invalid Downloader handle, please check parameter[1] passed and try again."
            return None, None, ls_Error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.download_read.argtypes = [DownloaderRef, POINTER(c_uint8), c_size_t, POINTER(c_char_p)]
        self.m_libUplink.download_read.restype = c_size_t
        #
        # prepare the inputs for the function
        lc_data_size = c_int32(pi_sizeToRead)
        lc_dataToWrite = [0]
        lc_dataToWrite = (c_uint8 * lc_data_size.value)(*lc_dataToWrite)
        lc_dataToWritePtr = cast(lc_dataToWrite, POINTER(c_uint8))
        lc_sizeToRead = c_size_t(pi_sizeToRead)
        lO_DownloaderRef = DownloaderRef()
        lO_DownloaderRef._handle = pl_downloaderHandle
        # create error ref pointer
        lc_errorPtr = c_char_p()
        # read file by calling the exported golang function
        lc_sizeRead = self.m_libUplink.download_read(lO_DownloaderRef, lc_dataToWritePtr, lc_sizeToRead,
                                                     byref(lc_errorPtr))
        #
        # prepare output to return received from function
        lc_dataToWrite = cast(lc_dataToWritePtr, c_char_p)
        #
        # if error occurred
        if lc_errorPtr.value is not None:
            return None, None, lc_errorPtr.value.decode("utf-8")
        else:
            return lc_dataToWrite.value, int(lc_sizeRead), None

    """
    function to close downloader after completing the data read process
    pre-requisites: download() function has been already called
    inputs: Downloader Handle (long)
    output: Error (string) if any else None
    """

    def download_close(self, pl_downloaderHandle):
        #
        # ensure downloader handle is valid
        if pl_downloaderHandle <= 0:
            ls_Error = "Invalid Downloader handle, please check parameter[1] passed and try again."
            return ls_Error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.download_close.argtypes = [DownloaderRef, POINTER(c_char_p)]
        self.m_libUplink.download_close.restype = None
        #
        # prepare the inputs for the function
        lO_DownloaderRef = DownloaderRef()
        lO_DownloaderRef._handle = pl_downloaderHandle
        # create error ref pointer
        lc_errorPtr = c_char_p()
        # close downloader by calling the exported golang function
        self.m_libUplink.download_close(lO_DownloaderRef, byref(lc_errorPtr))
        #
        # if error occurred
        if lc_errorPtr.value is not None:
            return lc_errorPtr.value.decode("utf-8")
        else:
            return None

    """
    function to create new bucket in Storj project
    pre-requisites: open_project() function has been already called
    inputs: Project Handle (long), Bucket Name (string)
    output: Bucket Info Handle (long), Error (string) if any else None
    """

    def create_bucket(self, pl_projectHandle, ps_bucketName, po_bucketConfig):
        #
        # ensure project handle is valid
        if pl_projectHandle <= 0:
            ls_Error = "Invalid Storj Project handle, please check parameter[1] passed and try again."
            return None, ls_Error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.create_bucket.argtypes = [ProjectRef, c_char_p, BucketConfig, POINTER(c_char_p)]
        self.m_libUplink.create_bucket.restype = BucketInfo
        #
        # prepare the input for the function
        lc_BucketName = c_char_p(ps_bucketName.encode('utf-8'))
        lO_ProjectRef = ProjectRef()
        lO_ProjectRef._handle = pl_projectHandle
        lO_BucketConfig = po_bucketConfig
        # create error ref pointer
        lc_errorPtr = c_char_p()
        #  by calling the exported golang function
        lO_bucketInfo = self.m_libUplink.create_bucket(lO_ProjectRef, lc_BucketName, lO_BucketConfig,
                                                       byref(lc_errorPtr))
        #
        # if error occurred
        if lc_errorPtr.value is not None:
            return None, lc_errorPtr.value.decode("utf-8")
        else:
            return lO_bucketInfo, None

    """
    function to close currently opened Bucket
    pre-requisites: open_bucket() function has been already called, successfully
    inputs: Bucket Handle (long)
    output: Error (string) if any else None
    """

    def close_bucket(self, pl_bucketHandle):
        #
        # ensure bucket handle is valid
        if pl_bucketHandle <= 0:
            ls_Error = "Invalid Bucket handle, please check parameter[1] passed and try again."
            return ls_Error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.close_bucket.argtypes = [BucketRef, POINTER(c_char_p)]
        self.m_libUplink.close_bucket.restype = None
        #
        # prepare the input for the function
        lO_BucketRef = BucketRef()
        lO_BucketRef._handle = pl_bucketHandle
        # create error ref pointer
        lc_errorPtr = c_char_p()
        #
        # close bucket by calling the exported golang function
        self.m_libUplink.close_bucket(lO_BucketRef, byref(lc_errorPtr))
        #
        # if error occurred
        if lc_errorPtr.value is not None:
            return lc_errorPtr.value.decode("utf-8")
        else:
            return None

    """
    function to close currently opened Storj project
    pre-requisites: open_project() function has been already called
    inputs: Project Handle (long)
    output: Error (string) if any else None
    """

    def close_project(self, pl_projectHandle):
        #
        # ensure project handle is valid
        if pl_projectHandle <= 0:
            ls_Error = "Invalid Storj Project handle, please check parameter[1] passed and try again."
            return ls_Error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.close_project.argtypes = [ProjectRef, POINTER(c_char_p)]
        self.m_libUplink.close_project.restype = None
        #
        # prepare the input for the function
        lO_projectRef = ProjectRef()
        lO_projectRef._handle = pl_projectHandle
        # create error ref pointer
        lc_errorPtr = c_char_p()
        #
        # close Storj project by calling the exported golang function
        self.m_libUplink.close_project(lO_projectRef, byref(lc_errorPtr))
        #
        # if error occurred
        if lc_errorPtr.value is not None:
            return lc_errorPtr.value.decode("utf-8")
        else:
            return None

    """
    function to close currently opened uplink
    pre-requisites: new_uplink() function has been already called
    inputs: Uplink Handle (long)
    output: Error (string) if any else None
    """

    def close_uplink(self, pl_uplinkHandle):
        #
        # ensure uplink handle is valid
        if pl_uplinkHandle <= 0:
            ls_Error = "Invalid Uplink handle, please check parameter[1] passed and try again."
            return ls_Error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.close_uplink.argtypes = [UplinkRef, POINTER(c_char_p)]
        self.m_libUplink.close_uplink.restype = None
        #
        # prepare the input for the function
        lO_UplinkRef = UplinkRef()
        lO_UplinkRef._handle = pl_uplinkHandle
        # create error ref pointer
        lc_errorPtr = c_char_p()
        #
        # close uplink by calling the exported golang function
        self.m_libUplink.close_uplink(lO_UplinkRef, byref(lc_errorPtr))
        #
        # if error occurred
        if lc_errorPtr.value is not None:
            return lc_errorPtr.value.decode("utf-8")
        else:
            return None

    """
    function to upload data from srcFullFileName (at local computer) to Storj (V3) bucket's path
    pre-requisites: open_bucket() function has been already called
    inputs: Bucket Handle (long), Storj Path/File Name (string) within the opened bucket, local Source Full File Name (string)
    output: True if successful else False, Error (string) if any else None
    """

    def upload_file(self, bucket, uploadPath, srcFullFileName):
        #
        # open file to be uploaded
        file_handle = open(srcFullFileName, 'r+b')
        data_len = os.path.getsize(srcFullFileName)
        #
        # call to get uploader handle
        uploader, ls_Error = self.upload(bucket, uploadPath)
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
            data = file_handle.read(size_to_write)
            #
            # call to write data to Storj bucket
            write_size, ls_Error = self.upload_write(uploader, data, size_to_write)
            if ls_Error is not None:
                return False, ls_Error
            #
            # exit while loop if nothing left to upload / unable to upload
            if write_size == 0:
                break
            # update last read location
            uploaded_total += write_size

        # commit upload data to bucket
        ls_Error = self.upload_commit(uploader)
        #
        # if error occurred
        if ls_Error is not None:
            return False, ls_Error
        else:
            return True, None

    """
    function to download Storj (V3) object's data and store it in given file with destFullFileName (on local computer)
    pre-requisites: open_bucket() function has been already called
    inputs: Bucket Handle (long), Storj Path/File Name (string) within the opened bucket, local Destination Full Path Name(string)
    output: True if successful else False, Error (string) if any else None
    """

    def download_file(self, bucket, storjPath, destFullPathName):
        #
        # open / create file with the given name to save the downloaded data
        file_handle = open(destFullPathName, 'w+b')
        #
        # call to get downloader handle
        downloader, ls_Error = self.download(bucket, storjPath)
        if ls_Error is not None:
            return False, ls_Error
        #
        # set packet size to be used while downloading
        size_to_write = 256
        # initialize local variables and start downloading packets of data
        downloaded_total = 0
        retry_count = 0
        while True:
            # call to read data from Storj bucket
            data, read_size, ls_Error = self.download_read(downloader, size_to_write)
            if ls_Error is not None:
                return False, ls_Error
            #
            # file writing process from the last written position if new data is downloaded
            written_size = 0
            if read_size != 0:
                file_handle.seek(downloaded_total)
                written_size = file_handle.write(data)
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
                    return False, "File download failed. Please try again."
            #
            retry_count = 0
            # update last read location
            downloaded_total += read_size

        # close downloader and free downloader access
        ls_Error = self.download_close(downloader)
        #
        # if error occurred
        if ls_Error is not None:
            return False, ls_Error
        else:
            return True, None
