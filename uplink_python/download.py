"""Module with Download class and dowload methods to work with object download"""
# pylint: disable=too-many-arguments
import ctypes
import os

from uplink_python.module_def import _DownloadStruct, _ReadResult, _ProjectStruct,\
    _ObjectResult, _Error
from uplink_python.errors import _storj_exception

_WINDOWS = os.name == 'nt'
COPY_BUFSIZE = 1024 * 1024 if _WINDOWS else 64 * 1024


class Download:
    """
    Download is a download from Storj Network.

    ...

    Attributes
    ----------
    download : int
        Download _handle returned from libuplinkc download_result.download
    uplink : Uplink
        uplink object used to get access
    project : Project
        project object used to create upload
    bucket_name : Str
        bucket_name to which upload is being processed
    storj_path : Str
        storj_path on which upload is to be done

    Methods
    -------
    read():
        Int
    read_file():
        None
    file_size():
        Int
    close():
        None
    info():
        Object
    """

    def __init__(self, download, uplink, project, bucket_name, storj_path):
        """Constructs all the necessary attributes for the Download object."""

        self.download = download
        self.project = project
        self.bucket_name = bucket_name
        self.storj_path = storj_path
        self.uplink = uplink

    def read(self, size_to_read: int):
        """
        function downloads up to len size_to_read bytes from the object's data stream.
        It returns the data_read in bytes and number of bytes read

        Parameters
        ----------
        size_to_read : int

        Returns
        -------
        bytes, int
        """
        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_download_read.argtypes = [ctypes.POINTER(_DownloadStruct),
                                                                 ctypes.POINTER(ctypes.c_uint8),
                                                                 ctypes.c_size_t]
        self.uplink.m_libuplink.uplink_download_read.restype = _ReadResult
        #
        # prepare the inputs for the function
        data_size = ctypes.c_int32(size_to_read)
        data_to_write = [0]
        data_to_write = (ctypes.c_uint8 * data_size.value)(*data_to_write)
        data_to_write_ptr = ctypes.cast(data_to_write, ctypes.POINTER(ctypes.c_uint8))
        size_to_read = ctypes.c_size_t(size_to_read)

        # read data from Storj by calling the exported golang function
        read_result = self.uplink.m_libuplink.uplink_download_read(self.download, data_to_write_ptr,
                                                                   size_to_read)
        #
        # if error occurred
        if bool(read_result.error):
            raise _storj_exception(read_result.error.contents.code,
                                   read_result.error.contents.message.decode("utf-8"))

        data_read = bytes()
        if int(read_result.bytes_read) != 0:
            #
            # --------------------------------------------
            # data conversion to type python readable form
            # conversion of LP_c_ubyte to python readable data variable
            data_read = ctypes.string_at(data_to_write_ptr, int(read_result.bytes_read))
        return data_read, int(read_result.bytes_read)

    def read_file(self, file_handle, buffer_size: int = 0):
        """
        function downloads complete object from it's data stream and writes it to the file whose
        handle is passed as parameter. After the download is complete it closes the download stream.

        Note: File handle should be a BinaryIO, i.e. file should be opened using 'w+b" flag.
        e.g.: file_handle = open(DESTINATION_FULL_FILENAME, 'w+b')
        Remember to close the object stream on storj and also close the local file handle
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
        file_size = self.file_size()
        if buffer_size > file_size:
            buffer_size = file_size
        while file_size:
            buf, bytes_read = self.read(buffer_size)
            if buf:
                file_handle.write(buf)
            file_size -= bytes_read

    def file_size(self):
        """
        function returns the size of object on Storj network for which download has been created.

        Returns
        -------
        int
        """

        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_stat_object.argtypes = [ctypes.POINTER(_ProjectStruct),
                                                               ctypes.c_char_p, ctypes.c_char_p]
        self.uplink.m_libuplink.uplink_stat_object.restype = _ObjectResult
        #
        # get object information by calling the exported golang function
        object_result = self.uplink.m_libuplink.uplink_stat_object(self.project, self.bucket_name,
                                                                   self.storj_path)
        # if error occurred
        if bool(object_result.error):
            raise _storj_exception(object_result.error.contents.code,
                                   object_result.error.contents.message.decode("utf-8"))
        # find object size
        return int(object_result.object.contents.system.content_length)

    def close(self):
        """
        function closes the download.

        Returns
        -------
        None
        """
        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_close_download.argtypes = [ctypes.POINTER(_DownloadStruct)]
        self.uplink.m_libuplink.uplink_close_download.restype = ctypes.POINTER(_Error)
        #
        # close downloader by calling the exported golang function
        error = self.uplink.m_libuplink.uplink_close_download(self.download)
        #
        # if error occurred
        if bool(error):
            raise _storj_exception(error.contents.code,
                                   error.contents.message.decode("utf-8"))

    def info(self):
        """
        function returns information about the downloaded object.

        Returns
        -------
        Object
        """
        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_download_info.argtypes = [ctypes.POINTER(_DownloadStruct)]
        self.uplink.m_libuplink.uplink_download_info.restype = _ObjectResult
        #
        # get last download info by calling the exported golang function
        object_result = self.uplink.m_libuplink.uplink_download_info(self.download)
        #
        # if error occurred
        if bool(object_result.error):
            raise _storj_exception(object_result.error.contents.code,
                                   object_result.error.contents.message.decode("utf-8"))
        return self.uplink.object_from_result(object_result.object)
