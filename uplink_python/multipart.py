"""Module with MultipartUpload class and upload methods to work with multipart upload"""# pylint: disable=line-too-long
import ctypes
from inspect import _void
import os


from collections import namedtuple
from sqlite3 import Timestamp, TimestampFromTicks
from time import time

from uplink_python.module_classes import CustomMetadata
from uplink_python.module_def import _MultipartUploadCommitOptionsStruct, _MultipartUploadCommitResult, _PartUploadStruct, _ProjectStruct, _BeginUploadResult, _Error, _CustomMetadataStruct, _ObjectResult, _UploadPartInfoResult, _UploadPartResult, _WriteResult, _PartInfoStruct
from uplink_python.errors import _storj_exception


_WINDOWS = os.name == 'nt'
COPY_BUFSIZE = 1024 * 1024 if _WINDOWS else 64 * 1024

class MultipartUpload:
    """
    Multipart upload is a multipart upload in Storj Network

    ...

    Attributes
    ----------
    bucket_name : str
        bucket name of the multipart upload
    object_key: str
        object key of the multipart upload
    upload_id: str
        upload_id returned from libuplinkc multipart.uplink_begin_upload
    uplink : Uplink
        uplink object used to get access

    Methods
    -------
    begin_multipart_upload():
        Int
    commit_multipart_upload():
        None
    abort():
        None
    """

    def __init__(self, project, bucket_name, object_key, upload_id, uplink):
        """Constructs all the necessary attributes for the MultipartUpload."""

        self.uplink = uplink
        self.project = project
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.upload_id = upload_id

    def commit(self):

        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_commit_upload.argtypes = [ctypes.POINTER(_ProjectStruct),
                                                                ctypes.POINTER(ctypes.c_char),
                                                                ctypes.POINTER(ctypes.c_char),
                                                                ctypes.POINTER(ctypes.c_char),
                                                                ctypes.POINTER(_MultipartUploadCommitOptionsStruct)]
        self.uplink.m_libuplink.uplink_commit_upload.restype = _MultipartUploadCommitResult


        bucket_name_ptr = ctypes.c_char_p(self.bucket_name.encode('utf-8'))
        object_key_ptr = ctypes.c_char_p(self.object_key.encode('utf-8'))
        upload_id_ptr = ctypes.c_char_p(self.upload_id.encode('utf-8'))

        upload_commit_options_obj = ctypes.POINTER(_MultipartUploadCommitOptionsStruct)()

        commit_result = self.uplink.m_libuplink.uplink_commit_upload(self.project.project, bucket_name_ptr, object_key_ptr,
                                                                    upload_id_ptr,upload_commit_options_obj)
        print("commit result = ", commit_result)

        if bool(commit_result.error):
            raise _storj_exception(commit_result.error.contents.code,
                        commit_result.error.contents.message.decode("utf-8"))
        return self.uplink.object_from_result(commit_result.object)

    def upload_part(self, part_number: int = -1):

        self.uplink.m_libuplink.uplink_upload_part.argtypes = [ctypes.POINTER(_ProjectStruct),
                                                                ctypes.POINTER(ctypes.c_char),
                                                                ctypes.POINTER(ctypes.c_char),
                                                                ctypes.POINTER(ctypes.c_char),
                                                                ctypes.c_uint32]
        self.uplink.m_libuplink.uplink_upload_part.restype = _UploadPartResult

        bucket_name_ptr = ctypes.c_char_p(self.bucket_name.encode('utf-8'))
        object_key_ptr = ctypes.c_char_p(self.object_key.encode('utf-8'))
        upload_id_ptr = ctypes.c_char_p(self.upload_id.encode('utf-8'))

        upload_part_result = self.uplink.m_libuplink.uplink_upload_part(self.project.project, bucket_name_ptr, object_key_ptr,
                                                                    upload_id_ptr, part_number)
        if bool(upload_part_result.error):
            raise _storj_exception(upload_part_result.error.contents.code,
                        upload_part_result.error.contents.message.decode("utf-8"))



        return UploadPart(upload_part_result.part_upload, self.uplink)

# // uplink_list_upload_parts lists uploaded parts.
# extern UplinkPartIterator* uplink_list_upload_parts(UplinkProject* project, uplink_const_char* bucket_name, uplink_const_char* object_key, uplink_const_char* upload_id, UplinkListUploadPartsOptions* options);

# // uplink_part_iterator_next prepares next entry for reading.
# //
# // It returns false if the end of the iteration is reached and there are no more parts, or if there is an error.
# extern _Bool uplink_part_iterator_next(UplinkPartIterator* iterator);

# // uplink_part_iterator_err returns error, if one happened during iteration.
# extern UplinkError* uplink_part_iterator_err(UplinkPartIterator* iterator);

# // uplink_part_iterator_item returns the current entry in the iterator.
# extern UplinkPart* uplink_part_iterator_item(UplinkPartIterator* iterator);

    def list_parts(self):
        self.uplink.m_libuplink.uplink_list_upload_parts.argtypes = [ctypes.POINTER(_ProjectStruct),
                                                                ctypes.POINTER(ctypes.c_char),
                                                                ctypes.POINTER(ctypes.c_char),
                                                                ctypes.POINTER(ctypes.c_char),
                                                                ctypes.c_uint32]
        self.uplink.m_libuplink.uplink_list_upload_parts.restype = _UploadPartResult

        bucket_name_ptr = ctypes.c_char_p(self.bucket_name.encode('utf-8'))
        object_key_ptr = ctypes.c_char_p(self.object_key.encode('utf-8'))
        upload_id_ptr = ctypes.c_char_p(self.upload_id.encode('utf-8'))

        list_parts_result = self.uplink.m_libuplink.uplink_list_upload_parts(self.project.project, bucket_name_ptr, object_key_ptr,
                                                                    upload_id_ptr, part_number)

        if bool(list_parts_result.error):
            raise _storj_exception(list_parts_result.error.contents.code,
                        list_parts_result.error.contents.message.decode("utf-8"))



        return UploadPart(list_parts_result.part_upload, self.uplink)

# typedef struct UplinkPart {
#     uint32_t part_number;
#     size_t size; // plain size of a part.
#     int64_t modified;
#     char *etag;
#     size_t etag_length;
# } UplinkPart;

# class PartInfo(namedtuple):
#     part_number: int
#     size: int
#     modified: Timestamp
#     etag: str

class UploadPartInfo:
    def __init__(self, part_number: int, size: int, modified: Timestamp, etag: str):
        self.part_number = part_number
        self.size = size
        self.modified = modified
        self.etag = etag

class UploadPart:

    def __init__(self, uploadPartResult, uplink):
        self.uplink = uplink
        self.partUpload = uploadPartResult


    def commit(self):
        self.uplink.m_libuplink.uplink_part_upload_commit.argtypes = [ctypes.POINTER(_PartUploadStruct)]
        self.uplink.m_libuplink.uplink_part_upload_commit.restype =  ctypes.POINTER(_Error)

        commit_part_error = self.uplink.m_libuplink.uplink_part_upload_commit(self.partUpload)

        if bool(commit_part_error):
            raise _storj_exception(commit_part_error.code,
                    commit_part_error.message.decode("utf-8"))

    def abort(self):
        self.uplink.m_libuplink.uplink_part_upload_abort.argtypes = [ctypes.POINTER(_PartUploadStruct)]
        self.uplink.m_libuplink.uplink_part_upload_abort.restype =  ctypes.POINTER(_Error)

        abort_part_error = self.uplink.m_libuplink.uplink_part_upload_abort(self.partUpload)

        if bool(abort_part_error):
            raise _storj_exception(abort_part_error.code,
                    abort_part_error.message.decode("utf-8"))

    def write(self, bytes, length):
        self.uplink.m_libuplink.uplink_part_upload_write.argtypes = [ctypes.POINTER(_PartUploadStruct),
                                                                ctypes.POINTER(ctypes.c_int8),
                                                                ctypes.c_size_t]
        self.uplink.m_libuplink.uplink_part_upload_write.restype = _WriteResult

        data_to_write_ptr = ctypes.cast(bytes, ctypes.POINTER(ctypes.c_int8))
        size_to_write_obj = ctypes.c_size_t(length)

        part_write_result = self.uplink.m_libuplink.uplink_part_upload_write(self.partUpload,data_to_write_ptr, size_to_write_obj)

        if bool(part_write_result.error):
            self.uplink.m_libuplink.uplink_free_write_result.argtypes = [_PartUploadStruct]
            self.uplink.m_libuplink.uplink_free_write_result(part_write_result)

    def write_file(self, file_handle, buffer_size:int = 0):

        if not buffer_size:
            buffer_size = COPY_BUFSIZE
        while True:
            buf = file_handle.read(buffer_size)
            if not buf:
                break
            self.write(buf, len(buf))


    def setEtag(self, etag):
        self.uplink.m_libuplink.uplink_part_upload_set_etag.argtypes = [ctypes.POINTER(_PartUploadStruct),
                                                                        ctypes.POINTER(ctypes.c_char)]
        self.uplink.m_libuplink.uplink_part_upload_set_etag.restype =  ctypes.POINTER(_Error)

        etag_ptr = ctypes.c_char_p(etag.encode('utf-8'))

        set_etag_error = self.uplink.m_libuplink.uplink_part_upload_set_etag(self.partUpload, etag_ptr)

        if bool(set_etag_error):
           self.free_error_and_raise_exception(set_etag_error)

    def info(self):
        self.uplink.m_libuplink.uplink_part_upload_info.argtypes = [ctypes.POINTER(_PartUploadStruct)]
        self.uplink.m_libuplink.uplink_part_upload_info.restype =  _UploadPartInfoResult

        info_result = self.uplink.m_libuplink.uplink_part_upload_info(self.partUpload)

        part_number = info_result.part.contents.part_number
        etag = info_result.part.contents.etag.decode("utf-8")
        size = info_result.part.contents.size
        modified = TimestampFromTicks(info_result.part.contents.modified)

        if bool(info_result.error):


            errorCode = info_result.error.contents.code
            errorMsg = info_result.error.contents.message.decode("utf-8")

            self.uplink.m_libuplink.uplink_free_part_result.argtypes = [_UploadPartInfoResult]
            self.uplink.m_libuplink.uplink_free_part_result(info_result)

            raise _storj_exception(errorCode,errorMsg)


        self.uplink.m_libuplink.uplink_free_part_result.argtypes = [_UploadPartInfoResult]
        self.uplink.m_libuplink.uplink_free_part_result(info_result)

        return UploadPartInfo(part_number, size, modified, etag)

