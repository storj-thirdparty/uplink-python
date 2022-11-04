"""Module with Project class and project methods to work with buckets and objects"""
import ctypes

from uplink_python.module_classes import ListBucketsOptions, ListObjectsOptions,\
    UploadOptions, DownloadOptions
from uplink_python.module_def import _BucketStruct, _ObjectStruct, _ListObjectsOptionsStruct,\
    _ObjectResult, _ListBucketsOptionsStruct, _UploadOptionsStruct, _DownloadOptionsStruct,\
    _ProjectStruct, _BucketResult, _BucketIterator, _ObjectIterator, _DownloadResult,\
    _UploadResult, _Error
from uplink_python.upload import Upload
from uplink_python.download import Download
from uplink_python.errors import _storj_exception


class Project:
    """
    Project provides access to managing buckets and objects.

    ...

    Attributes
    ----------
    project : int
        Project _handle returned from libuplinkc project_result.project
    uplink : Uplink
        uplink object used to get access

    Methods
    -------
    create_bucket():
        Bucket
    ensure_bucket():
        Bucket
    stat_bucket():
        Bucket
    list_buckets():
        list of Bucket
    delete_bucket():
        Bucket
    stat_object():
        Object
    list_objects():
        list of Object
    delete_object():
        Object
    close():
        None
    upload_object():
        Upload
    download_object():
        Download
    """

    def __init__(self, project, uplink):
        """Constructs all the necessary attributes for the Project object."""

        self.project = project
        self.uplink = uplink

    def create_bucket(self, bucket_name: str):
        """
        function creates a new bucket.
        When bucket already exists it throws BucketAlreadyExistError exception.

        Parameters
        ----------
        bucket_name : str

        Returns
        -------
        Bucket
        """

        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_create_bucket.argtypes = [ctypes.POINTER(_ProjectStruct),
                                                                 ctypes.c_char_p]
        self.uplink.m_libuplink.uplink_create_bucket.restype = _BucketResult
        self.uplink.m_libuplink.uplink_free_bucket.argtypes = [_BucketResult]
        #
        # prepare the input for the function
        bucket_name_ptr = ctypes.c_char_p(bucket_name.encode('utf-8'))

        # create bucket by calling the exported golang function
        bucket_result = self.uplink.m_libuplink.uplink_create_bucket(self.project, bucket_name_ptr)

        _unwrapped_bucket = self.uplink.unwrap_bucket_result(bucket_result)
        bucket = self.uplink.bucket_from_result(_unwrapped_bucket)

        self.uplink.m_libuplink.uplink_free_bucket_result(bucket_result)

        return bucket

    def ensure_bucket(self, bucket_name: str):
        """
        function ensures that a bucket exists or creates a new one.

        When bucket already exists it returns a valid Bucket and no error

        Parameters
        ----------
        bucket_name : str

        Returns
        -------
        Bucket
        """

        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_ensure_bucket.argtypes = [ctypes.POINTER(_ProjectStruct),
                                                                 ctypes.c_char_p]
        self.uplink.m_libuplink.uplink_ensure_bucket.restype = _BucketResult
        #
        # prepare the input for the function
        bucket_name_ptr = ctypes.c_char_p(bucket_name.encode('utf-8'))

        # open bucket if doesn't exist by calling the exported golang function
        bucket_result = self.uplink.m_libuplink.uplink_ensure_bucket(self.project, bucket_name_ptr)

        return self.check_bucket_result(bucket_result)

    def stat_bucket(self, bucket_name: str):
        """
        function returns information about a bucket.

        Parameters
        ----------
        bucket_name : str

        Returns
        -------
        Bucket
        """

        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_stat_bucket.argtypes = [ctypes.POINTER(_ProjectStruct),
                                                               ctypes.c_char_p]
        self.uplink.m_libuplink.uplink_stat_bucket.restype = _BucketResult
        #
        # prepare the input for the function
        bucket_name_ptr = ctypes.c_char_p(bucket_name.encode('utf-8'))

        # get bucket information by calling the exported golang function
        bucket_result = self.uplink.m_libuplink.uplink_stat_bucket(self.project, bucket_name_ptr)

        return self.check_bucket_result(bucket_result)

    def check_bucket_result(self, bucket_result):
        if bool(bucket_result.error):
            error_code = bucket_result.error.contents.code
            error_msg = bucket_result.error.contents.message.decode("utf-8")

            self.uplink.m_libuplink.uplink_free_bucket_result.argtypes = [_BucketResult]
            self.uplink.m_libuplink.uplink_free_bucket_result(bucket_result)

            raise _storj_exception(error_code, error_msg)

        return self.uplink.bucket_from_result(bucket_result.bucket)

    def list_buckets(self, list_bucket_options: ListBucketsOptions = None):
        """
        function returns a list of buckets with all its information.

        Parameters
        ----------
        list_bucket_options : ListBucketsOptions (optional)

        Returns
        -------
        list of Bucket
        """

        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_list_buckets.argtypes =\
            [ctypes.POINTER(_ProjectStruct), ctypes.POINTER(_ListBucketsOptionsStruct)]
        self.uplink.m_libuplink.uplink_list_buckets.restype =\
            ctypes.POINTER(_BucketIterator)
        self.uplink.m_libuplink.uplink_free_bucket_iterator.argtypes=\
            [ctypes.POINTER(_BucketIterator)]
        #
        self.uplink.m_libuplink.uplink_bucket_iterator_item.argtypes =\
            [ctypes.POINTER(_BucketIterator)]
        self.uplink.m_libuplink.uplink_bucket_iterator_item.restype =\
            ctypes.POINTER(_BucketStruct)
        self.uplink.m_libuplink.uplink_free_bucket.argtypes =\
            [ctypes.POINTER(_BucketStruct)]
        #
        self.uplink.m_libuplink.uplink_bucket_iterator_err.argtypes =\
            [ctypes.POINTER(_BucketIterator)]
        self.uplink.m_libuplink.uplink_bucket_iterator_err.restype =\
            ctypes.POINTER(_Error)
        #
        self.uplink.m_libuplink.uplink_bucket_iterator_next.argtypes =\
            [ctypes.POINTER(_BucketIterator)]
        self.uplink.m_libuplink.uplink_bucket_iterator_next.restype =\
            ctypes.c_bool
        #
        # prepare the input for the function
        if list_bucket_options is None:
            list_bucket_options_obj = ctypes.POINTER(_ListBucketsOptionsStruct)()
        else:
            list_bucket_options_obj = ctypes.byref(list_bucket_options.get_structure())

        # get bucket list by calling the exported golang function
        bucket_iterator = self.uplink.m_libuplink.uplink_list_buckets(self.project,
                                                                      list_bucket_options_obj)

        bucket_iterator_err = self.uplink.m_libuplink.uplink_bucket_iterator_err(bucket_iterator)
        if bool(bucket_iterator_err):
            self.uplink.free_error_and_raise_exception(bucket_iterator_err)
        bucket_list = list()
        while self.uplink.m_libuplink.uplink_bucket_iterator_next(bucket_iterator):
            bucket = self.uplink.m_libuplink.uplink_bucket_iterator_item(bucket_iterator)
            bucket_list.append(self.uplink.bucket_from_result(bucket))
            self.uplink.m_libuplink.uplink_free_bucket(bucket)

        return bucket_list

    def delete_bucket(self, bucket_name: str):
        """
        function deletes a bucket.

        When bucket is not empty it throws BucketNotEmptyError exception.

        Parameters
        ----------
        bucket_name : str

        Returns
        -------
        Bucket
        """

        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_delete_bucket.argtypes = [ctypes.POINTER(_ProjectStruct),
                                                                 ctypes.c_char_p]
        self.uplink.m_libuplink.uplink_delete_bucket.restype = _BucketResult
        self.uplink.m_libuplink.uplink_free_bucket_result.argtypes = [_BucketResult]
        #
        # prepare the input for the function
        bucket_name_ptr = ctypes.c_char_p(bucket_name.encode('utf-8'))

        # delete bucket by calling the exported golang function
        bucket_result = self.uplink.m_libuplink.uplink_delete_bucket(self.project, bucket_name_ptr)
        #
        # if error occurred
        if bool(bucket_result.error):
            error_code = bucket_result.error.contents.code
            error_msg = bucket_result.error.contents.message.decode("utf-8")

            self.uplink.m_libuplink.uplink_free_bucket_result(bucket_result)

            raise _storj_exception(error_code, error_msg)

        bucket = self.uplink.bucket_from_result(bucket_result.bucket)

        return bucket

    def stat_object(self, bucket_name: str, storj_path: str):
        """
        function returns information about an object at the specific key.

        Parameters
        ----------
        bucket_name : str
        storj_path : str

        Returns
        -------
        Object
        """

        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_stat_object.argtypes = [ctypes.POINTER(_ProjectStruct),
                                                               ctypes.c_char_p, ctypes.c_char_p]
        self.uplink.m_libuplink.uplink_stat_object.restype = _ObjectResult
        self.uplink.m_libuplink.uplink_free_object_result.argtypes = [_ObjectResult]
        #
        # prepare the input for the function
        bucket_name_ptr = ctypes.c_char_p(bucket_name.encode('utf-8'))
        storj_path_ptr = ctypes.c_char_p(storj_path.encode('utf-8'))

        # get object information by calling the exported golang function
        object_result = self.uplink.m_libuplink.uplink_stat_object(self.project, bucket_name_ptr,
                                                                   storj_path_ptr)
        #
        # if error occurred
        if bool(object_result.error):
            error_code = object_result.error.contents.code
            error_msg = object_result.error.contents.message.decode("utf-8")

            self.uplink.m_libuplink.uplink_free_object_result(object_result)

            raise _storj_exception(error_code, error_msg)

        _object = self.uplink.object_from_result(object_result.object)

        return _object

    def list_objects(self, bucket_name: str, list_object_options: ListObjectsOptions = None):
        """
        function returns a list of objects with all its information.

        Parameters
        ----------
        bucket_name : str
        list_object_options : ListObjectsOptions (optional)

        Returns
        -------
        list of Object
        """

        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_list_objects.argtypes =\
            [ctypes.POINTER(_ProjectStruct), ctypes.c_char_p,
             ctypes.POINTER(_ListObjectsOptionsStruct)]
        self.uplink.m_libuplink.uplink_list_objects.restype =\
            ctypes.POINTER(_ObjectIterator)
        self.uplink.m_libuplink.uplink_free_object_iterator.argtypes =\
            [ctypes.POINTER(_ObjectIterator)]
        #
        self.uplink.m_libuplink.uplink_object_iterator_item.argtypes =\
            [ctypes.POINTER(_ObjectIterator)]
        self.uplink.m_libuplink.uplink_object_iterator_item.restype =\
            ctypes.POINTER(_ObjectStruct)
        self.uplink.m_libuplink.uplink_free_object.argtypes =\
            [ctypes.POINTER(_ObjectStruct)]
        #
        self.uplink.m_libuplink.uplink_object_iterator_err.argtypes =\
            [ctypes.POINTER(_ObjectIterator)]
        self.uplink.m_libuplink.uplink_object_iterator_err.restype =\
            ctypes.POINTER(_Error)
        #
        self.uplink.m_libuplink.uplink_object_iterator_next.argtypes =\
            [ctypes.POINTER(_ObjectIterator)]
        self.uplink.m_libuplink.uplink_object_iterator_next.restype =\
            ctypes.c_bool
        #
        # prepare the input for the function
        if list_object_options is None:
            list_object_options_obj = ctypes.POINTER(_ListObjectsOptionsStruct)()
        else:
            list_object_options_obj = ctypes.byref(list_object_options.get_structure())
        bucket_name_ptr = ctypes.c_char_p(bucket_name.encode('utf-8'))

        # get object list by calling the exported golang function
        object_iterator = self.uplink.m_libuplink.uplink_list_objects(self.project, bucket_name_ptr,
                                                                      list_object_options_obj)

        object_iterator_err = self.uplink.m_libuplink.uplink_object_iterator_err(object_iterator)
        if bool(object_iterator_err):
            raise _storj_exception(object_iterator_err.contents.code,
                                   object_iterator_err.contents.message.decode("utf-8"))

        object_list = []
        while self.uplink.m_libuplink.uplink_object_iterator_next(object_iterator):
            object_ = self.uplink.m_libuplink.uplink_object_iterator_item(object_iterator)
            object_list.append(self.uplink.object_from_result(object_))
            self.uplink.m_libuplink.uplink_free_object(object_)

        self.uplink.m_libuplink.uplink_free_object_iterator(object_iterator)
        return object_list

    def delete_object(self, bucket_name: str, storj_path: str):
        """
        function deletes the object at the specific key.

        Parameters
        ----------
        bucket_name : str
        storj_path : str

        Returns
        -------
        Object
        """

        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_delete_object.argtypes = [ctypes.POINTER(_ProjectStruct),
                                                                 ctypes.c_char_p, ctypes.c_char_p]
        self.uplink.m_libuplink.uplink_delete_object.restype = _ObjectResult
        self.uplink.m_libuplink.uplink_free_object_result.argtypes = [_ObjectResult]
        #
        # prepare the input for the function
        bucket_name_ptr = ctypes.c_char_p(bucket_name.encode('utf-8'))
        storj_path_ptr = ctypes.c_char_p(storj_path.encode('utf-8'))

        # delete object by calling the exported golang function
        object_result = self.uplink.m_libuplink.uplink_delete_object(self.project, bucket_name_ptr,
                                                                     storj_path_ptr)

        return self.uplink.unwrap_object_result(object_result)

    def close(self):
        """
        function closes the project and all associated resources.

        Returns
        -------
        None
        """
        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_close_project.argtypes = [ctypes.POINTER(_ProjectStruct)]
        self.uplink.m_libuplink.uplink_close_project.restype = ctypes.POINTER(_Error)
        #
        # close Storj project by calling the exported golang function
        error = self.uplink.m_libuplink.uplink_close_project(self.project)
        #
        # if error occurred
        if bool(error):
            self.uplink.free_error_and_raise_exception(error)

    def upload_object(self, bucket_name: str, storj_path: str,
                      upload_options: UploadOptions = None):
        """
        function starts an upload to the specified key.

        Parameters
        ----------
        bucket_name : str
        storj_path : str
        upload_options : UploadOptions (optional)

        Returns
        -------
        Upload
        """
        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_upload_object.argtypes =\
            [ctypes.POINTER(_ProjectStruct), ctypes.c_char_p, ctypes.c_char_p,
             ctypes.POINTER(_UploadOptionsStruct)]
        self.uplink.m_libuplink.uplink_upload_object.restype = _UploadResult
        self.uplink.m_libuplink.uplink_free_upload_result.argtypes = [_UploadResult]
        #
        # prepare the input for the function
        if upload_options is None:
            upload_options_obj = ctypes.POINTER(_UploadOptionsStruct)()
        else:
            upload_options_obj = ctypes.byref(upload_options.get_structure())

        bucket_name_ptr = ctypes.c_char_p(bucket_name.encode('utf-8'))
        storj_path_ptr = ctypes.c_char_p(storj_path.encode('utf-8'))

        # get uploader by calling the exported golang function
        upload_result = self.uplink.m_libuplink.uplink_upload_object(self.project, bucket_name_ptr,
                                                                     storj_path_ptr,
                                                                     upload_options_obj)

        _upload_result = self.uplink.unwrap_upload_object_result(upload_result)

        # _upload_result will be freed when committing or aborting upload.
        return Upload(_upload_result, self.uplink)

    def download_object(self, bucket_name: str, storj_path: str,
                        download_options: DownloadOptions = None):
        """
        function starts download to the specified key.

        Parameters
        ----------
        bucket_name : str
        storj_path : str
        download_options : DownloadOptions (optional)

        Returns
        -------
        Download
        """
        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_download_object.argtypes =\
            [ctypes.POINTER(_ProjectStruct), ctypes.c_char_p, ctypes.c_char_p,
             ctypes.POINTER(_DownloadOptionsStruct)]
        self.uplink.m_libuplink.uplink_download_object.restype = _DownloadResult
        self.uplink.m_libuplink.uplink_free_download_result.argtypes = [_DownloadResult]
        #
        # prepare the input for the function
        if download_options is None:
            download_options_obj = ctypes.POINTER(_DownloadOptionsStruct)()
        else:
            download_options_obj = ctypes.byref(download_options.get_structure())

        bucket_name_ptr = ctypes.c_char_p(bucket_name.encode('utf-8'))
        storj_path_ptr = ctypes.c_char_p(storj_path.encode('utf-8'))

        # get downloader by calling the exported golang function
        download_result = self.uplink.m_libuplink.uplink_download_object(self.project,
                                                                         bucket_name_ptr,
                                                                         storj_path_ptr,
                                                                         download_options_obj)
        #
        # if error occurred
        if bool(download_result.error):
            error_code = download_result.error.contents.code
            error_msg = download_result.error.contents.message.decode("utf-8")

            self.uplink.m_libuplink.uplink_free_download_result(download_result)

            raise _storj_exception(error_code, error_msg)

        return Download(download_result.download, self.uplink, self.project, bucket_name_ptr,
                        storj_path_ptr)
