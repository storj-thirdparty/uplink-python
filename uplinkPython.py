##################################
# Python Bindings for Storj (V3) #
##################################
import os
from ctypes import *

##############################################
# Structure classes for go structure objects #
##############################################

# Error defines:
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


# Various handle structures:
class Handle(Structure):
    _fields_ = [("_handle", c_size_t)]


class Access(Structure):
    _fields_ = [("_handle", c_size_t)]


class Project(Structure):
    _fields_ = [("_handle", c_size_t)]


class Download(Structure):
    _fields_ = [("_handle", c_size_t)]


class Upload(Structure):
    _fields_ = [("_handle", c_size_t)]


# Various configuration structures:
class Config(Structure):
    _fields_ = [("user_agent", c_char_p), ("dial_timeout_milliseconds", c_int32),
                ("temp_directory", c_char_p)]


class Bucket(Structure):
    _fields_ = [("name", c_char_p), ("created", c_int64)]


class SystemMetadata(Structure):
    _fields_ = [("created", c_int64), ("expires", c_int64), ("content_length", c_int64)]


class CustomMetadataEntry(Structure):
    _fields_ = [("key", c_char_p), ("key_length", c_size_t), ("value", c_char_p), ("value_length", c_size_t)]


class CustomMetadata(Structure):
    _fields_ = [("entries", POINTER(CustomMetadataEntry)), ("count", c_size_t)]


class Object(Structure):
    _fields_ = [("key", c_char_p), ("is_prefix", c_bool), ("system", SystemMetadata),
                ("custom", CustomMetadata)]


class UploadOptions(Structure):
    _fields_ = [("expires", c_int64)]


class DownloadOptions(Structure):
    _fields_ = [("offset", c_int64), ("length", c_int64)]


class ListObjectsOptions(Structure):
    _fields_ = [("prefix", c_char_p), ("cursor", c_char_p), ("recursive", c_bool), ("system", c_bool),
                ("custom", c_bool)]


class ListBucketsOptions(Structure):
    _fields_ = [("cursor", c_char_p)]


class ObjectIterator(Structure):
    _fields_ = [("_handle", c_size_t)]


class BucketIterator(Structure):
    _fields_ = [("_handle", c_size_t)]


class Permission(Structure):
    _fields_ = [("allow_download", c_bool), ("allow_upload", c_bool), ("allow_list", c_bool), ("allow_delete", c_bool),
                ("not_before", c_int64), ("not_after", c_int64)]


class SharePrefix(Structure):
    _fields_ = [("bucket", c_char_p), ("prefix", c_char_p)]


class Error(Structure):
    _fields_ = [("code", c_int32), ("message", c_char_p)]


# Various result structures:
class AccessResult(Structure):
    _fields_ = [("access", POINTER(Access)), ("error", POINTER(Error))]


class ProjectResult(Structure):
    _fields_ = [("project", POINTER(Project)), ("error", POINTER(Error))]


class BucketResult(Structure):
    _fields_ = [("bucket", POINTER(Bucket)), ("error", POINTER(Error))]


class ObjectResult(Structure):
    _fields_ = [("object", POINTER(Object)), ("error", POINTER(Error))]


class UploadResult(Structure):
    _fields_ = [("upload", POINTER(Upload)), ("error", POINTER(Error))]


class DownloadResult(Structure):
    _fields_ = [("download", POINTER(Download)), ("error", POINTER(Error))]


class WriteResult(Structure):
    _fields_ = [("bytes_written", c_size_t), ("error", POINTER(Error))]


class ReadResult(Structure):
    _fields_ = [("bytes_read", c_size_t), ("error", POINTER(Error))]


class StringResult(Structure):
    _fields_ = [("string", c_char_p), ("error", POINTER(Error))]


#########################################################
# Python Storj class with all Storj functions' bindings #
#########################################################

class LibUplinkPy:
    def __init__(self):
        # private members of PyStorj class with reference objects
        # include the golang exported libuplink library functions
        so_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libuplinkc.so')
        self.m_libUplink = CDLL(so_path)

    """
    function requests satellite for a new access grant using a passphrase
    pre-requisites: none
    inputs: Satellite Address (String), API key (String) and Passphrase (String)
    output: AccessResult (Object), Error (String) if any else None
    """

    def request_access_with_passphrase(self, ps_satellite, ps_api_key, ps_passphrase):
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.request_access_with_passphrase.argtypes = [c_char_p, c_char_p, c_char_p]
        self.m_libUplink.request_access_with_passphrase.restype = AccessResult
        #
        # prepare the input for the function
        lc_satellite_ptr = c_char_p(ps_satellite.encode('utf-8'))
        lc_api_key_ptr = c_char_p(ps_api_key.encode('utf-8'))
        lc_passphrase_ptr = c_char_p(ps_passphrase.encode('utf-8'))

        # get access to Storj by calling the exported golang function
        lo_access_result = self.m_libUplink.request_access_with_passphrase(lc_satellite_ptr, lc_api_key_ptr,
                                                                           lc_passphrase_ptr)
        #
        # if error occurred
        if bool(lo_access_result.error):
            return lo_access_result, lo_access_result.error.contents.message.decode("utf-8")
        else:
            return lo_access_result, None

    """
    function requests satellite for a new access grant using a passphrase and custom configuration
    pre-requisites: none
    inputs: Config (Object), Satellite Address (String), API key (String) and Passphrase (String)
    output: AccessResult (Object), Error (String) if any else None
    """

    def config_request_access_with_passphrase(self, po_config, ps_satellite, ps_api_key, ps_passphrase):
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.config_request_access_with_passphrase.argtypes = [Config, c_char_p, c_char_p, c_char_p]
        self.m_libUplink.config_request_access_with_passphrase.restype = AccessResult
        #
        # prepare the input for the function
        if po_config is None:
            lo_config = Config()
        else:
            lo_config = po_config
        lc_satellite_ptr = c_char_p(ps_satellite.encode('utf-8'))
        lc_api_key_ptr = c_char_p(ps_api_key.encode('utf-8'))
        lc_passphrase_ptr = c_char_p(ps_passphrase.encode('utf-8'))

        # get access to Storj by calling the exported golang function
        lo_access_result = self.m_libUplink.config_request_access_with_passphrase(lo_config, lc_satellite_ptr,
                                                                                  lc_api_key_ptr,
                                                                                  lc_passphrase_ptr)
        #
        # if error occurred
        if bool(lo_access_result.error):
            return lo_access_result, lo_access_result.error.contents.message.decode("utf-8")
        else:
            return lo_access_result, None

    """
    function opens Storj(V3) project using access grant.
    pre-requisites: request_access_with_passphrase or parse_access function has been already called
    inputs: Access (Object)
    output: ProjectResult (Object), Error (String) if any else None
    """

    def open_project(self, po_access):
        #
        # ensure access object is already created
        if po_access is None:
            ls_error = "Invalid access object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.open_project.argtypes = [POINTER(Access)]
        self.m_libUplink.open_project.restype = ProjectResult
        #
        # open project by calling the exported golang function
        lo_project_result = self.m_libUplink.open_project(po_access)
        #
        # if error occurred
        if bool(lo_project_result.error):
            return lo_project_result, lo_project_result.error.contents.message.decode("utf-8")
        else:
            return lo_project_result, None

    """
    function opens Storj(V3) project using access grant and custom configuration.
    pre-requisites: request_access_with_passphrase or parse_access function has been already called
    inputs: Config (Object), Access (Object)
    output: ProjectResult (Object), Error (String) if any else None
    """

    def config_open_project(self, po_config, po_access):
        #
        # ensure access object is already created
        if po_access is None:
            ls_error = "Invalid access object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.config_open_project.argtypes = [Config, POINTER(Access)]
        self.m_libUplink.config_open_project.restype = ProjectResult
        #
        # prepare the input for the function
        if po_config is None:
            lo_config = Config()
        else:
            lo_config = po_config
        #
        # open project by calling the exported golang function
        lo_project_result = self.m_libUplink.config_open_project(lo_config, po_access)
        #
        # if error occurred
        if bool(lo_project_result.error):
            return lo_project_result, lo_project_result.error.contents.message.decode("utf-8")
        else:
            return lo_project_result, None

    """
    function creates a new bucket and ignores the error when it already exists
    pre-requisites: open_project function has been already called
    inputs: Project (Object) ,Bucket Name (String)
    output: BucketResult (Object), Error (String) if any else None
    """

    def ensure_bucket(self, po_project, ps_bucket_name):
        #
        # ensure project object is valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.ensure_bucket.argtypes = [POINTER(Project), c_char_p]
        self.m_libUplink.ensure_bucket.restype = BucketResult
        #
        # prepare the input for the function
        lc_bucket_name_ptr = c_char_p(ps_bucket_name.encode('utf-8'))

        # open bucket if doesn't exist by calling the exported golang function
        lo_bucket_result = self.m_libUplink.ensure_bucket(po_project, lc_bucket_name_ptr)
        #
        # if error occurred
        if bool(lo_bucket_result.error):
            return lo_bucket_result, lo_bucket_result.error.contents.message.decode("utf-8")
        else:
            return lo_bucket_result, None

    """
    function returns information about a bucket.
    pre-requisites: open_project function has been already called
    inputs: Project (Object) ,Bucket Name (String)
    output: BucketResult (Object), Error (String) if any else None
    """

    def stat_bucket(self, po_project, ps_bucket_name):
        #
        # ensure project object is valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.stat_bucket.argtypes = [POINTER(Project), c_char_p]
        self.m_libUplink.stat_bucket.restype = BucketResult
        #
        # prepare the input for the function
        lc_bucket_name_ptr = c_char_p(ps_bucket_name.encode('utf-8'))

        # get bucket information by calling the exported golang function
        lo_bucket_result = self.m_libUplink.stat_bucket(po_project, lc_bucket_name_ptr)
        #
        # if error occurred
        if bool(lo_bucket_result.error):
            return lo_bucket_result, lo_bucket_result.error.contents.message.decode("utf-8")
        else:
            return lo_bucket_result, None

    """
    function returns information about an object at the specific key.
    pre-requisites: open_project
    inputs: Project (Object) ,Bucket Name (String) , Object Key(String)
    output: ObjectResult (Object), Error (string) if any else None
    """

    def stat_object(self, po_project, ps_bucket_name, ps_storj_path):
        #
        # ensure project object is valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.stat_object.argtypes = [POINTER(Project), c_char_p, c_char_p]
        self.m_libUplink.stat_object.restype = ObjectResult
        #
        # prepare the input for the function
        lc_bucket_name_ptr = c_char_p(ps_bucket_name.encode('utf-8'))
        lc_storj_path_ptr = c_char_p(ps_storj_path.encode('utf-8'))

        # get object information by calling the exported golang function
        lo_object_result = self.m_libUplink.stat_object(po_project, lc_bucket_name_ptr, lc_storj_path_ptr)
        #
        # if error occurred
        if bool(lo_object_result.error):
            return lo_object_result, lo_object_result.error.contents.message.decode("utf-8")
        else:
            return lo_object_result, None

    """
    function creates a new bucket.
    pre-requisites: open_project function has been already called
    inputs: Project (Object) ,Bucket Name (String)
    output: BucketResult (Object), Error (String) if any else None
    """

    def create_bucket(self, po_project, ps_bucket_name):
        #
        # ensure project object is valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.create_bucket.argtypes = [POINTER(Project), c_char_p]
        self.m_libUplink.create_bucket.restype = BucketResult
        #
        # prepare the input for the function
        lc_bucket_name_ptr = c_char_p(ps_bucket_name.encode('utf-8'))

        # create bucket by calling the exported golang function
        lo_bucket_result = self.m_libUplink.create_bucket(po_project, lc_bucket_name_ptr)
        #
        # if error occurred
        if bool(lo_bucket_result.error):
            return lo_bucket_result, lo_bucket_result.error.contents.message.decode("utf-8")
        else:
            return lo_bucket_result, None

    """
    function starts an upload to the specified key.
    pre-requisites: open_project function has been already called
    inputs: Project (Object), Bucket Name (String), Object Key(String), Upload Options(Object)
    output: UploadResult (Object), Error (String) if any else None
    """

    def upload_object(self, po_project, ps_bucket_name, ps_storj_path, po_upload_options):
        #
        # ensure project object is valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.upload_object.argtypes = [POINTER(Project), c_char_p, c_char_p, POINTER(UploadOptions)]
        self.m_libUplink.upload_object.restype = UploadResult
        #
        # prepare the input for the function
        if po_upload_options is None:
            lo_upload_options = POINTER(UploadOptions)()
        else:
            lo_upload_options = byref(po_upload_options)

        lc_bucket_name_ptr = c_char_p(ps_bucket_name.encode('utf-8'))
        lc_storj_path_ptr = c_char_p(ps_storj_path.encode('utf-8'))

        # get uploader by calling the exported golang function
        lo_upload_result = self.m_libUplink.upload_object(po_project, lc_bucket_name_ptr, lc_storj_path_ptr,
                                                          lo_upload_options)
        #
        # if error occurred
        if bool(lo_upload_result.error):
            return lo_upload_result, lo_upload_result.error.contents.message.decode("utf-8")
        else:
            return lo_upload_result, None

    #
    """
    function uploads bytes data passed as parameter to the object's data stream.
    pre-requisites: upload_object function has been already called
    inputs: Upload (Object), Bytes Data Stream(LP_c_ubyte) , Length (Integer)
    output: WriteResult (Object), Error (String) if any else None
    """

    def upload_write(self, po_upload, pbt_data_to_write_ptr, pi_size_to_write):
        #
        # ensure upload object is valid
        if po_upload is None:
            ls_error = "Invalid upload object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.upload_write.argtypes = [POINTER(Upload), POINTER(c_uint8), c_size_t]
        self.m_libUplink.upload_write.restype = WriteResult
        #
        # prepare the inputs for the function
        lc_size_to_write = c_size_t(pi_size_to_write)

        # upload data by calling the exported golang function
        lo_write_result = self.m_libUplink.upload_write(po_upload, pbt_data_to_write_ptr, lc_size_to_write)
        #
        # if error occurred
        if bool(lo_write_result.error):
            return lo_write_result, lo_write_result.error.contents.message.decode("utf-8")
        else:
            return lo_write_result, None

    """
    function commits the uploaded data.
    pre-requisites: upload_object function has been already called
    inputs: Upload (Object)
    output: Error (Object) if any else None
    """

    def upload_commit(self, po_upload):
        #
        # ensure upload object is valid
        if po_upload is None:
            ls_error = "Invalid upload object, please check the parameter passed and try again."
            return ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.upload_commit.argtypes = [POINTER(Upload)]
        self.m_libUplink.upload_commit.restype = POINTER(Error)
        #

        # upload commit by calling the exported golang function
        lo_error = self.m_libUplink.upload_commit(po_upload)
        #
        # if error occurred
        if bool(lo_error):
            return lo_error
        else:
            return None

    """
    function aborts an ongoing upload.
    pre-requisites: upload_object function has been already called
    inputs: Upload (Object)
    output: Error (Object) if any else None
    """

    def upload_abort(self, po_upload):
        #
        # ensure upload object is valid
        if po_upload is None:
            ls_error = "Invalid upload object, please check the parameter passed and try again."
            return ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.upload_abort.argtypes = [POINTER(Upload)]
        self.m_libUplink.upload_abort.restype = POINTER(Error)
        #

        # abort ongoing upload by calling the exported golang function
        lo_error = self.m_libUplink.upload_abort(po_upload)
        #
        # if error occurred
        if bool(lo_error):
            return lo_error
        else:
            return None

    """
    function to set custom meta information while uploading data
    pre-requisites: upload_object function has been already called
    inputs: Upload (Object), CustomMetadata (Object)
    output: Error (Object) if any else None
    """

    def upload_set_custom_metadata(self, po_upload, po_custom_metadata):
        #
        # ensure upload object is valid
        if po_upload is None:
            ls_error = "Invalid upload object, please check the parameter passed and try again."
            return ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.upload_set_custom_metadata.argtypes = [POINTER(Upload), CustomMetadata]
        self.m_libUplink.upload_set_custom_metadata.restype = POINTER(Error)
        #
        # prepare the input for the function
        if po_custom_metadata is None:
            lo_custom_metadata = CustomMetadata()
        else:
            lo_custom_metadata = po_custom_metadata
        #
        # set custom metadata to upload by calling the exported golang function
        lo_error = self.m_libUplink.upload_set_custom_metadata(po_upload, lo_custom_metadata)
        #
        # if error occurred
        if bool(lo_error):
            return lo_error
        else:
            return None

    """
    function returns information about the downloaded object.
    pre-requisites: download_object function has been already called
    inputs: Download (Object)
    output: Object Result (Object), Error (String) if any else None
    """

    def download_info(self, po_download):
        #
        # ensure download object is valid
        if po_download is None:
            ls_error = "Invalid download object, please check the parameter passed and try again."
            return ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.download_info.argtypes = [POINTER(Download)]
        self.m_libUplink.download_info.restype = ObjectResult
        #
        # get last download info by calling the exported golang function
        lo_object_result = self.m_libUplink.download_info(po_download)
        #
        # if error occurred
        if bool(lo_object_result.error):
            return lo_object_result, lo_object_result.error.contents.message.decode("utf-8")
        else:
            return lo_object_result, None

    """
    function returns the last information about the uploaded object.
    pre-requisites: upload_object function has been already called
    inputs: Upload (Object)
    output: Object Result (Object), Error (String) if any else None
    """

    def upload_info(self, po_upload):
        #
        # ensure upload object is valid
        if po_upload is None:
            ls_error = "Invalid upload object, please check the parameter passed and try again."
            return ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.upload_info.argtypes = [POINTER(Upload)]
        self.m_libUplink.upload_info.restype = ObjectResult
        #
        # get last upload info by calling the exported golang function
        lo_object_result = self.m_libUplink.upload_info(po_upload)
        #
        # if error occurred
        if bool(lo_object_result.error):
            return lo_object_result, lo_object_result.error.contents.message.decode("utf-8")
        else:
            return lo_object_result, None

    """
    function starts download to the specified key.
    pre-requisites: open_project function has been already called
    inputs: Project (Object), Bucket Name(String), Object Key(String), Download Options(Object)
    output: DownloadResult (Object), Error (String) if any else None
    """

    def download_object(self, po_project, ps_bucket_name, ps_storj_path, po_download_options):
        #
        # ensure project object is valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.download_object.argtypes = [POINTER(Project), c_char_p, c_char_p, POINTER(DownloadOptions)]
        self.m_libUplink.download_object.restype = DownloadResult
        #
        # prepare the input for the function
        if po_download_options is None:
            lo_download_options = POINTER(DownloadOptions)()
        else:
            lo_download_options = byref(po_download_options)

        lc_bucket_name_ptr = c_char_p(ps_bucket_name.encode('utf-8'))
        lc_storj_path_ptr = c_char_p(ps_storj_path.encode('utf-8'))

        # get downloader by calling the exported golang function
        lo_download_result = self.m_libUplink.download_object(po_project, lc_bucket_name_ptr, lc_storj_path_ptr,
                                                              lo_download_options)
        #
        # if error occurred
        if bool(lo_download_result.error):
            return lo_download_result, lo_download_result.error.contents.message.decode("utf-8")
        else:
            return lo_download_result, None

    """
    function downloads from object's data stream into bytes up to length amount.
    pre-requisites: download_object function has been already called
    inputs: Download (Object), Length(Integer)
    output: Data downloaded (LP_c_ubyte), ReadResult (Object), Error (String) if any else None
    """

    def download_read(self, po_download, pi_size_to_read):
        #
        # ensure download object is valid
        if po_download is None:
            ls_error = "Invalid download object, please check the parameter passed and try again."
            return None, None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.download_read.argtypes = [POINTER(Download), POINTER(c_uint8), c_size_t]
        self.m_libUplink.download_read.restype = ReadResult
        #
        # prepare the inputs for the function
        lc_data_size = c_int32(pi_size_to_read)
        lc_data_to_write = [0]
        lc_data_to_write = (c_uint8 * lc_data_size.value)(*lc_data_to_write)
        lc_data_to_write_ptr = cast(lc_data_to_write, POINTER(c_uint8))
        lc_size_to_read = c_size_t(pi_size_to_read)

        # read data from Storj by calling the exported golang function
        lc_read_result = self.m_libUplink.download_read(po_download, lc_data_to_write_ptr, lc_size_to_read)
        #
        # if error occurred
        if bool(lc_read_result.error):
            return lc_data_to_write_ptr, lc_read_result, lc_read_result.error.contents.message.decode("utf-8")
        else:
            return lc_data_to_write_ptr, lc_read_result, None

    """
    function closes the download.
    pre-requisites: download_object function has been already called
    inputs: Download (Object)
    output: Error (Object) if any else None
    """

    def close_download(self, po_download):
        #
        # ensure download object is valid
        if po_download is None:
            ls_error = "Invalid download object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.close_download.argtypes = [POINTER(Download)]
        self.m_libUplink.close_download.restype = POINTER(Error)
        #
        # close downloader by calling the exported golang function
        lo_error = self.m_libUplink.close_download(po_download)
        #
        # if error occurred
        if bool(lo_error):
            return lo_error
        else:
            return None

    """
    function closes the Storj(V3) project.
    pre-requisites: open_project function has been already called
    inputs: Project (Object)
    output: Error (Object) if any else None
    """

    def close_project(self, po_project):
        #
        # ensure project object is valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.close_project.argtypes = [POINTER(Project)]
        self.m_libUplink.close_project.restype = POINTER(Error)
        #
        # close Storj project by calling the exported golang function
        lo_error = self.m_libUplink.close_project(po_project)
        #
        # if error occurred
        if bool(lo_error):
            return lo_error
        else:
            return None

    """
    function lists buckets
    pre-requisites: open_project function has been already called
    inputs: Project (Object), ListBucketsOptions (Object)
    output: Bucket List (Python List), Error (String) if any else None
    """

    def list_buckets(self, po_project, po_list_bucket_options):
        #
        # ensure project object is valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.list_buckets.argtypes = [POINTER(Project), POINTER(ListBucketsOptions)]
        self.m_libUplink.list_buckets.restype = POINTER(BucketIterator)
        #
        self.m_libUplink.bucket_iterator_item.argtypes = [POINTER(BucketIterator)]
        self.m_libUplink.bucket_iterator_item.restype = POINTER(Bucket)
        #
        self.m_libUplink.bucket_iterator_next.argtypes = [POINTER(BucketIterator)]
        self.m_libUplink.bucket_iterator_next.restype = c_bool
        #
        # prepare the input for the function
        if po_list_bucket_options is None:
            lo_list_bucket_options = POINTER(ListBucketsOptions)()
        else:
            lo_list_bucket_options = byref(po_list_bucket_options)

        # get bucket list by calling the exported golang function
        lo_bucket_iterator = self.m_libUplink.list_buckets(po_project, lo_list_bucket_options)
        lo_bucket_list = list()
        while self.m_libUplink.bucket_iterator_next(lo_bucket_iterator):
            lo_bucket_list.append(self.m_libUplink.bucket_iterator_item(lo_bucket_iterator))

        #
        # if error occurred
        if len(lo_bucket_list) == 0:
            return None, "No bucket found!"
        else:
            return lo_bucket_list, None

    """
    function lists objects
    pre-requisites: open_project function has been already called
    inputs: Project (Object), Bucket Name (String), ListObjectsOptions (Object)
    output: Bucket List (Python List), Error (String) if any else None
    """

    def list_objects(self, po_project, ps_bucket_name, po_list_object_options):
        #
        # ensure project object is valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.list_objects.argtypes = [POINTER(Project), c_char_p, POINTER(ListObjectsOptions)]
        self.m_libUplink.list_objects.restype = POINTER(ObjectIterator)
        #
        self.m_libUplink.object_iterator_item.argtypes = [POINTER(ObjectIterator)]
        self.m_libUplink.object_iterator_item.restype = POINTER(Object)
        #
        self.m_libUplink.object_iterator_next.argtypes = [POINTER(ObjectIterator)]
        self.m_libUplink.object_iterator_next.restype = c_bool
        #
        # prepare the input for the function
        if po_list_object_options is None:
            lo_list_object_options = POINTER(ListObjectsOptions)()
        else:
            lo_list_object_options = byref(po_list_object_options)
        lc_bucket_name_ptr = c_char_p(ps_bucket_name.encode('utf-8'))

        # get object list by calling the exported golang function
        lo_object_iterator = self.m_libUplink.list_objects(po_project, lc_bucket_name_ptr, lo_list_object_options)
        lo_object_list = list()
        while self.m_libUplink.object_iterator_next(lo_object_iterator):
            lo_object_list.append(self.m_libUplink.object_iterator_item(lo_object_iterator))

        #
        # if error occurred
        if len(lo_object_list) == 0:
            return None, "No object found!"
        else:
            return lo_object_list, None

    """
    function deletes a bucket.
    pre-requisites: open_project function has been already called
    inputs: Project (Object), Bucket Name (String)
    output: BucketResult (Object), Error (String) if any else None
    """

    def delete_bucket(self, po_project, ps_bucket_name):
        #
        # ensure project handle and encryption handles are valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.delete_bucket.argtypes = [POINTER(Project), c_char_p]
        self.m_libUplink.delete_bucket.restype = BucketResult
        #
        # prepare the input for the function
        lc_bucket_name_ptr = c_char_p(ps_bucket_name.encode('utf-8'))

        # delete bucket by calling the exported golang function
        lo_bucket_result = self.m_libUplink.delete_bucket(po_project, lc_bucket_name_ptr)
        #
        # if error occurred
        if bool(lo_bucket_result.error):
            return lo_bucket_result, lo_bucket_result.error.contents.message.decode("utf-8")
        else:
            return lo_bucket_result, None

    """
    function deletes an object.
    pre-requisites: open_project function has been already called
    inputs: Project (Object), Bucket Name (String), Object Key (String)
    output: ObjectResult (Object), Error (String) if any else None
    """

    def delete_object(self, po_project, ps_bucket_name, ps_storj_path):
        #
        # ensure project handle and encryption handles are valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.delete_object.argtypes = [POINTER(Project), c_char_p, c_char_p]
        self.m_libUplink.delete_object.restype = ObjectResult
        #
        # prepare the input for the function
        lc_bucket_name_ptr = c_char_p(ps_bucket_name.encode('utf-8'))
        lc_storj_path_ptr = c_char_p(ps_storj_path.encode('utf-8'))

        # delete object by calling the exported golang function
        lo_object_result = self.m_libUplink.delete_object(po_project, lc_bucket_name_ptr, lc_storj_path_ptr)
        #
        # if error occurred
        if bool(lo_object_result.error):
            return lo_object_result, lo_object_result.error.contents.message.decode("utf-8")
        else:
            return lo_object_result, None

    """
    function to parses serialized access grant string
    pre-requisites: none
    inputs: Serialized Access (String)
    output: AccessResult (Object), Error (String) if any else None
    """

    def parse_access(self, ps_serialized_access):
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.parse_access.argtypes = [c_char_p]
        self.m_libUplink.parse_access.restype = AccessResult
        #

        # get parsed access by calling the exported golang function
        lo_access_result = self.m_libUplink.parse_access(ps_serialized_access)
        #
        # if error occurred
        if bool(lo_access_result.error):
            return lo_access_result, lo_access_result.error.contents.message.decode("utf-8")
        else:
            return lo_access_result, None

    """
    function serializes access grant into a string.
    pre-requisites: request_access_with_passphrase or parse_access function has been already called
    inputs: Access (Object)
    output: StringResult (Object), Error (String) if any else None
    """

    def access_serialize(self, po_access):
        #
        # ensure access object is valid
        if po_access is None:
            ls_error = "Invalid access object, please check parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.access_serialize.argtypes = [POINTER(Access)]
        self.m_libUplink.access_serialize.restype = StringResult
        #
        # get serialized access by calling the exported golang function
        lc_string_result = self.m_libUplink.access_serialize(po_access)
        #
        # if error occurred
        if bool(lc_string_result.error):
            return lc_string_result, lc_string_result.error.contents.message.decode("utf-8")
        else:
            return lc_string_result, None

    """
    function creates new access grant with specific permission. Permission will be applied to prefixes when defined.
    pre-requisites: request_access_with_passphrase or parse_access function has been already called
    inputs: Access (Object), Permission (Object), Share Prefix (Python List of Dictionaries)
    output: String Result (Object), Error (String) if any else None
    """

    def access_share(self, po_access, po_permission, po_shared_prefix):
        #
        # ensure access object is valid
        if po_access is None:
            ls_error = "Invalid access object, please check parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libUplink.access_share.argtypes = [POINTER(Access), Permission, POINTER(SharePrefix), c_size_t]
        self.m_libUplink.access_share.restype = AccessResult
        #
        # prepare the input for the function
        # check and create valid Permission parameter
        if po_permission is None:
            lo_permission = Permission()
        else:
            lo_permission = po_permission
        # check and create valid Share Prefix parameter
        # po_shared_prefix = [{"bucket": "bucketname01", "prefix": "uploadPath01/data"}]
        if po_shared_prefix is None:
            lo_shared_prefix = POINTER(SharePrefix)()
            lc_array_size = c_size_t(0)
        else:
            num_of_structs = len(po_shared_prefix)
            li_array_size = (SharePrefix * num_of_structs)()
            lo_array = cast(li_array_size, POINTER(SharePrefix))
            for i, val in enumerate(po_shared_prefix):
                lo_array[i] = SharePrefix(c_char_p(val['bucket'].encode('utf-8')),
                                          c_char_p(val['prefix'].encode('utf-8')))
            lo_shared_prefix = lo_array
            lc_array_size = c_size_t(num_of_structs)
        #
        # get shareable access by calling the exported golang function
        lo_access_result = self.m_libUplink.access_share(po_access, lo_permission, lo_shared_prefix,
                                                         lc_array_size)
        #
        # if error occurred
        if bool(lo_access_result.error):
            return lo_access_result, lo_access_result.error.contents.message.decode("utf-8")
        else:
            return lo_access_result, None
