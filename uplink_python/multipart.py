"""Module with MultipartUpload class and upload methods to work with multipart upload"""# pylint: disable=line-too-long
import ctypes
import os

from uplink_python.module_classes import CustomMetadata
from uplink_python.module_def import _MultipartUploadCommitOptionsStruct, _MultipartUploadCommitResult, _PartUploadStruct, _ProjectStruct, _BeginUploadResult, _Error, _CustomMetadataStruct, _ObjectResult, _UploadPartResult, _WriteResult
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

        if bool(commit_result.error):
            raise _storj_exception(commit_result.error.contents.code,
                        commit_result.error.contents.message.decode("utf-8"))
        return self.uplink.object_from_result(commit_result.object)

    def upload_part(self, file_handle, buffer_size: int = 0, part_number: int = -1):

        if not buffer_size:
            buffer_size = COPY_BUFSIZE
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

        part_handle = upload_part_result.part_upload.contents._handle
        print("PART RESULT HANDLE = ", part_handle)

        while True:
            print("Buffer size = ", buffer_size)
            buf = file_handle.read(buffer_size)
            print("size of part data = ", len(buf))
            if not buf:
                break
            self.uplink.m_libuplink.uplink_part_upload_write.argtypes = [ctypes.POINTER(_PartUploadStruct),
                                                                ctypes.POINTER(ctypes.c_uint8),
                                                                ctypes.c_size_t]
            self.uplink.m_libuplink.uplink_part_upload_write.restype = _WriteResult

            #
            # prepare the inputs for the function
            # --------------------------------------------
            # data conversion to type required by function
            # get size of data in c type int32 variable
            # conversion of read bytes data to c type ubyte Array
            # data_to_write = (ctypes.c_uint8 * ctypes.c_int32(len(buf)).value)(*buf)
            # print("DATA to write = ", *data_to_write)
            # conversion of c type ubyte Array to LP_c_ubyte required by upload write function
            data_to_write_ptr = ctypes.cast(buf, ctypes.POINTER(ctypes.c_uint8))
            # --------------------------------------------
            size_to_write_obj = ctypes.c_size_t(len(buf))
            upload_commit_options_obj = _PartUploadStruct()
            upload_commit_options_obj.contents._handle = part_handle

            part_write_result = self.uplink.m_libuplink.uplink_part_upload_write(upload_commit_options_obj,data_to_write_ptr, size_to_write_obj)

            if bool(part_write_result.error):
                raise _storj_exception(part_write_result.error.contents.code,
                        part_write_result.error.contents.message.decode("utf-8"))
