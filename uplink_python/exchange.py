# pylint: disable=wildcard-import, unused-wildcard-import, too-few-public-methods
"""
Python Binding's Exchange Module for Storj (V3)
"""
from ctypes import *
from os import path


# Various handle structures:
class Project(Structure):
    """ Project structure """
    _fields_ = [("_handle", c_size_t)]


class Download(Structure):
    """ Download structure """
    _fields_ = [("_handle", c_size_t)]


class Upload(Structure):
    """ Upload structure """
    _fields_ = [("_handle", c_size_t)]


# Various configuration structures:
class SystemMetadata(Structure):
    """ SystemMetadata structure """
    _fields_ = [("created", c_int64), ("expires", c_int64), ("content_length", c_int64)]


class CustomMetadataEntry(Structure):
    """ CustomMetadataEntry structure """
    _fields_ = [("key", c_char_p), ("key_length", c_size_t), ("value", c_char_p),
                ("value_length", c_size_t)]


class CustomMetadata(Structure):
    """ CustomMetadata structure """
    _fields_ = [("entries", POINTER(CustomMetadataEntry)), ("count", c_size_t)]


class Object(Structure):
    """ Object structure """
    _fields_ = [("key", c_char_p), ("is_prefix", c_bool), ("system", SystemMetadata),
                ("custom", CustomMetadata)]


class UploadOptions(Structure):
    """ UploadOptions structure """
    _fields_ = [("expires", c_int64)]


class DownloadOptions(Structure):
    """ DownloadOptions structure """
    _fields_ = [("offset", c_int64), ("length", c_int64)]


class Error(Structure):
    """ Error structure """
    _fields_ = [("code", c_int32), ("message", c_char_p)]


# Various result structures:
class ObjectResult(Structure):
    """ ObjectResult structure """
    _fields_ = [("object", POINTER(Object)), ("error", POINTER(Error))]


class UploadResult(Structure):
    """ UploadResult structure """
    _fields_ = [("upload", POINTER(Upload)), ("error", POINTER(Error))]


class DownloadResult(Structure):
    """ DownloadResult structure """
    _fields_ = [("download", POINTER(Download)), ("error", POINTER(Error))]


class WriteResult(Structure):
    """ WriteResult structure """
    _fields_ = [("bytes_written", c_size_t), ("error", POINTER(Error))]


class ReadResult(Structure):
    """ ReadResult structure """
    _fields_ = [("bytes_read", c_size_t), ("error", POINTER(Error))]


#########################################################
# Python Storj class with all Storj functions' bindings #
#########################################################

class DataExchange:
    """
    Python Storj Data Exchange class with all Storj Upload and Download functions' bindings
    """

    #
    def __init__(self):
        # private members of PyStorj class with reference objects
        # include the golang exported libuplink library functions
        so_path = path.join(path.dirname(path.abspath(__file__)), 'libuplinkc.so')
        self.m_libuplink = CDLL(so_path)

    def upload_object(self, project, bucket_name, storj_path, upload_options):
        """
        function starts an upload to the specified key.
        pre-requisites: open_project function has been already called
        inputs: Project (Object), Bucket Name (String), Object Key(String), Upload Options(Object)
        output: UploadResult (Object), Error (String) if any else None
        """
        #
        # ensure project object is valid
        if project is None:
            error = "Invalid project object, please check the parameter passed and try again."
            return None, error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.upload_object.argtypes = [POINTER(Project), c_char_p, c_char_p,
                                                   POINTER(UploadOptions)]
        self.m_libuplink.upload_object.restype = UploadResult
        #
        # prepare the input for the function
        if upload_options is None:
            upload_options_obj = POINTER(UploadOptions)()
        else:
            upload_options_obj = byref(upload_options)

        bucket_name_ptr = c_char_p(bucket_name.encode('utf-8'))
        storj_path_ptr = c_char_p(storj_path.encode('utf-8'))

        # get uploader by calling the exported golang function
        upload_result = self.m_libuplink.upload_object(project, bucket_name_ptr,
                                                       storj_path_ptr,
                                                       upload_options_obj)
        #
        # if error occurred
        if bool(upload_result.error):
            return upload_result, upload_result.error.contents.message.decode("utf-8")
        return upload_result, None

    def upload_write(self, upload, data_to_write_ptr, size_to_write):
        """
        function uploads bytes data passed as parameter to the object's data stream.
        pre-requisites: upload_object function has been already called
        inputs: Upload (Object), Bytes Data Stream(LP_c_ubyte) , Length (Integer)
        output: WriteResult (Object), Error (String) if any else None
        """
        #
        # ensure upload object is valid
        if upload is None:
            error = "Invalid upload object, please check the parameter passed and try again."
            return None, error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.upload_write.argtypes = [POINTER(Upload), POINTER(c_uint8), c_size_t]
        self.m_libuplink.upload_write.restype = WriteResult
        #
        # prepare the inputs for the function
        size_to_write_obj = c_size_t(size_to_write)

        # upload data by calling the exported golang function
        write_result = self.m_libuplink.upload_write(upload, data_to_write_ptr,
                                                     size_to_write_obj)
        #
        # if error occurred
        if bool(write_result.error):
            return write_result, write_result.error.contents.message.decode("utf-8")
        return write_result, None

    def upload_commit(self, upload):
        """
        function commits the uploaded data.
        pre-requisites: upload_object function has been already called
        inputs: Upload (Object)
        output: Error (Object) if any else None
        """
        #
        # ensure upload object is valid
        if upload is None:
            error = "Invalid upload object, please check the parameter passed and try again."
            return error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.upload_commit.argtypes = [POINTER(Upload)]
        self.m_libuplink.upload_commit.restype = POINTER(Error)
        #

        # upload commit by calling the exported golang function
        error = self.m_libuplink.upload_commit(upload)
        #
        # if error occurred
        if bool(error):
            return error
        return None

    def upload_abort(self, upload):
        """
        function aborts an ongoing upload.
        pre-requisites: upload_object function has been already called
        inputs: Upload (Object)
        output: Error (Object) if any else None
        """
        #
        # ensure upload object is valid
        if upload is None:
            error = "Invalid upload object, please check the parameter passed and try again."
            return error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.upload_abort.argtypes = [POINTER(Upload)]
        self.m_libuplink.upload_abort.restype = POINTER(Error)
        #

        # abort ongoing upload by calling the exported golang function
        error = self.m_libuplink.upload_abort(upload)
        #
        # if error occurred
        if bool(error):
            return error
        return None

    def upload_set_custom_metadata(self, upload, custom_metadata):
        """
        function to set custom meta information while uploading data
        pre-requisites: upload_object function has been already called
        inputs: Upload (Object), CustomMetadata (Object)
        output: Error (Object) if any else None
        """
        #
        # ensure upload object is valid
        if upload is None:
            error = "Invalid upload object, please check the parameter passed and try again."
            return error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.upload_set_custom_metadata.argtypes = [POINTER(Upload), CustomMetadata]
        self.m_libuplink.upload_set_custom_metadata.restype = POINTER(Error)
        #
        # prepare the input for the function
        if custom_metadata is None:
            custom_metadata = CustomMetadata()
        #
        # set custom metadata to upload by calling the exported golang function
        error = self.m_libuplink.upload_set_custom_metadata(upload, custom_metadata)
        #
        # if error occurred
        if bool(error):
            return error
        return None

    def download_info(self, download):
        """
        function returns information about the downloaded object.
        pre-requisites: download_object function has been already called
        inputs: Download (Object)
        output: Object Result (Object), Error (String) if any else None
        """
        #
        # ensure download object is valid
        if download is None:
            error = "Invalid download object, please check the parameter passed and try again."
            return error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.download_info.argtypes = [POINTER(Download)]
        self.m_libuplink.download_info.restype = ObjectResult
        #
        # get last download info by calling the exported golang function
        object_result = self.m_libuplink.download_info(download)
        #
        # if error occurred
        if bool(object_result.error):
            return object_result, object_result.error.contents.message.decode("utf-8")
        return object_result, None

    def upload_info(self, upload):
        """
        function returns the last information about the uploaded object.
        pre-requisites: upload_object function has been already called
        inputs: Upload (Object)
        output: Object Result (Object), Error (String) if any else None
        """
        #
        # ensure upload object is valid
        if upload is None:
            error = "Invalid upload object, please check the parameter passed and try again."
            return error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.upload_info.argtypes = [POINTER(Upload)]
        self.m_libuplink.upload_info.restype = ObjectResult
        #
        # get last upload info by calling the exported golang function
        object_result = self.m_libuplink.upload_info(upload)
        #
        # if error occurred
        if bool(object_result.error):
            return object_result, object_result.error.contents.message.decode("utf-8")
        return object_result, None

    def download_object(self, project, bucket_name, storj_path, download_options):
        """
        function starts download to the specified key.
        pre-requisites: open_project function has been already called
        inputs: Project (Object), Bucket Name(String), Object Key(String), Download Options(Object)
        output: DownloadResult (Object), Error (String) if any else None
        """
        #
        # ensure project object is valid
        if project is None:
            error = "Invalid project object, please check the parameter passed and try again."
            return None, error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.download_object.argtypes = [POINTER(Project), c_char_p, c_char_p,
                                                     POINTER(DownloadOptions)]
        self.m_libuplink.download_object.restype = DownloadResult
        #
        # prepare the input for the function
        if download_options is None:
            download_options_obj = POINTER(DownloadOptions)()
        else:
            download_options_obj = byref(download_options)

        bucket_name_ptr = c_char_p(bucket_name.encode('utf-8'))
        storj_path_ptr = c_char_p(storj_path.encode('utf-8'))

        # get downloader by calling the exported golang function
        download_result = self.m_libuplink.download_object(project, bucket_name_ptr,
                                                           storj_path_ptr,
                                                           download_options_obj)
        #
        # if error occurred
        if bool(download_result.error):
            return download_result, download_result.error.contents.message.decode("utf-8")
        return download_result, None

    def download_read(self, download, pi_size_to_read):
        """
        function downloads from object's data stream into bytes up to length amount.
        pre-requisites: download_object function has been already called
        inputs: Download (Object), Length(Integer)
        output: Data downloaded (LP_c_ubyte), ReadResult (Object), Error (String) if any else None
        """
        #
        # ensure download object is valid
        if download is None:
            error = "Invalid download object, please check the parameter passed and try again."
            return None, None, error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.download_read.argtypes = [POINTER(Download), POINTER(c_uint8), c_size_t]
        self.m_libuplink.download_read.restype = ReadResult
        #
        # prepare the inputs for the function
        data_size = c_int32(pi_size_to_read)
        data_to_write = [0]
        data_to_write = (c_uint8 * data_size.value)(*data_to_write)
        data_to_write_ptr = cast(data_to_write, POINTER(c_uint8))
        size_to_read = c_size_t(pi_size_to_read)

        # read data from Storj by calling the exported golang function
        read_result = self.m_libuplink.download_read(download, data_to_write_ptr,
                                                     size_to_read)
        #
        # if error occurred
        if bool(read_result.error):
            return data_to_write_ptr, read_result, \
                   read_result.error.contents.message.decode("utf-8")
        return data_to_write_ptr, read_result, None

    def close_download(self, download):
        """
        function closes the download.
        pre-requisites: download_object function has been already called
        inputs: Download (Object)
        output: Error (Object) if any else None
        """
        #
        # ensure download object is valid
        if download is None:
            error = "Invalid download object, please check the parameter passed and try again."
            return None, error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.close_download.argtypes = [POINTER(Download)]
        self.m_libuplink.close_download.restype = POINTER(Error)
        #
        # close downloader by calling the exported golang function
        error = self.m_libuplink.close_download(download)
        #
        # if error occurred
        if bool(error):
            return error
        return None
