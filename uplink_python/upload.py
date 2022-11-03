"""Module with Upload class and upload methods to work with object upload"""
# pylint: disable=line-too-long
import ctypes
import os

from uplink_python.module_classes import CustomMetadata
from uplink_python.module_def import _UploadStruct, _WriteResult, _Error, _CustomMetadataStruct, _ObjectResult
from uplink_python.errors import _storj_exception

_WINDOWS = os.name == 'nt'
COPY_BUFSIZE = 1024 * 1024 if _WINDOWS else 64 * 1024


class Upload:
    """
    Upload is an upload to Storj Network.

    ...

    Attributes
    ----------
    upload : int
        Upload _handle returned from libuplinkc upload_result.upload
    uplink : Uplink
        uplink object used to get access

    Methods
    -------
    write():
        Int
    write_file():
        None
    commit():
        None
    abort():
        None
    set_custom_metadata():
        None
    info():
        Object
    """

    def __init__(self, upload, uplink):
        """Constructs all the necessary attributes for the Upload object."""

        self.upload = upload
        self.uplink = uplink

    def write(self, data_to_write: bytes, size_to_write: int):
        """
        function uploads bytes data passed as parameter to the object's data stream.

        Parameters
        ----------
        data_to_write : bytes
        size_to_write : int

        Returns
        -------
        int
        """

        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_upload_write.argtypes = [ctypes.POINTER(_UploadStruct),
                                                                ctypes.POINTER(ctypes.c_uint8),
                                                                ctypes.c_size_t]
        self.uplink.m_libuplink.uplink_upload_write.restype = _WriteResult
        self.uplink.m_libuplink.uplink_free_write_result.argtypes = [_WriteResult]
        #
        # prepare the inputs for the function
        # --------------------------------------------
        # data conversion to type required by function
        # get size of data in c type int32 variable
        # conversion of read bytes data to c type ubyte Array
        data_to_write = (ctypes.c_uint8 * ctypes.c_int32(len(data_to_write)).value)(*data_to_write)
        # conversion of c type ubyte Array to LP_c_ubyte required by upload write function
        data_to_write_ptr = ctypes.cast(data_to_write, ctypes.POINTER(ctypes.c_uint8))
        # --------------------------------------------
        size_to_write_obj = ctypes.c_size_t(size_to_write)

        # upload data by calling the exported golang function
        write_result = self.uplink.m_libuplink.uplink_upload_write(self.upload, data_to_write_ptr,
                                                                   size_to_write_obj)

        return self.uplink.unwrap_upload_write_result(write_result)

    def write_file(self, file_handle, buffer_size: int = 0):
        """
        function uploads complete file whose handle is passed as parameter to the
        object's data stream and commits the object after upload is complete.

        Note: File handle should be a BinaryIO, i.e. file should be opened using 'r+b" flag.
        e.g.: file_handle = open(SRC_FULL_FILENAME, 'r+b')
        Remember to commit the object on storj and also close the local file handle
        after this function exits.

        Parameters
        ----------
        file_handle : BinaryIO
        buffer_size : int

        Returns
        -------
        None
        """

        if not buffer_size:
            buffer_size = COPY_BUFSIZE
        while True:
            buf = file_handle.read(buffer_size)
            if not buf:
                break
            self.write(buf, len(buf))

    def commit(self):
        """
        function commits the uploaded data.

        Returns
        -------
        None
        """

        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_upload_commit.argtypes = [ctypes.POINTER(_UploadStruct)]
        self.uplink.m_libuplink.uplink_upload_commit.restype = ctypes.POINTER(_Error)
        #

        # upload commit by calling the exported golang function
        error = self.uplink.m_libuplink.uplink_upload_commit(self.upload)

        self.uplink.free_upload_struct(self.upload)
        #
        # if error occurred
        if bool(error):
            self.uplink.free_error_and_raise_exception(error)

    def abort(self):
        """
        function aborts an ongoing upload.

        Returns
        -------
        None
        """
        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_upload_abort.argtypes = [ctypes.POINTER(_UploadStruct)]
        self.uplink.m_libuplink.uplink_upload_abort.restype = ctypes.POINTER(_Error)
        #

        # abort ongoing upload by calling the exported golang function
        error = self.uplink.m_libuplink.uplink_upload_abort(self.upload)
        #
        # if error occurred
        self.uplink.free_upload_struct(self.upload)
        if bool(error):
            self.uplink.free_and_raise_error(error)


    def set_custom_metadata(self, custom_metadata: CustomMetadata = None):
        """
        function to set custom meta information while uploading data

        Parameters
        ----------
        custom_metadata : CustomMetadata

        Returns
        -------
        None
        """
        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_upload_set_custom_metadata.argtypes = [ctypes.POINTER(_UploadStruct),
                                                                              _CustomMetadataStruct]
        self.uplink.m_libuplink.uplink_upload_set_custom_metadata.restype = ctypes.POINTER(_Error)
        #
        # prepare the input for the function
        if custom_metadata is None:
            custom_metadata_obj = _CustomMetadataStruct()
        else:
            custom_metadata_obj = custom_metadata.get_structure()
        #
        # set custom metadata to upload by calling the exported golang function
        error = self.uplink.m_libuplink.uplink_upload_set_custom_metadata(self.upload, custom_metadata_obj)

        if bool(error):
            self.uplink.free_error_and_raise_exception(error)

    def info(self):
        """
        function returns the last information about the uploaded object.

        Returns
        -------
        Object
        """
        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_upload_info.argtypes = [ctypes.POINTER(_UploadStruct)]
        self.uplink.m_libuplink.uplink_upload_info.restype = _ObjectResult
        self.uplink.m_libuplink.uplink_free_object_result.argtypes = [_ObjectResult]
        #
        # get last upload info by calling the exported golang function
        object_result = self.uplink.m_libuplink.uplink_upload_info(self.upload)

        _unwrapped_object = self.uplink.unwrap_object_result(object_result)
        info = self.uplink.object_from_result(_unwrapped_object)
        self.uplink.m_libuplink.uplink_free_object(_unwrapped_object)
        return info
