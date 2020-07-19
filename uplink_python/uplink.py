# pylint: disable=too-few-public-methods
""" Python Bindings for Storj (V3) """

from .exchange import DataExchange, Project, Error, c, ObjectResult, Object


# Structure classes for go structure objects #
# Various handle structures:
class Handle(c.Structure):

    """ Handle structure """
    _fields_ = [("_handle", c.c_size_t)]


class Access(c.Structure):

    """ Access structure """
    _fields_ = [("_handle", c.c_size_t)]


# Various configuration structures:
class Config(c.Structure):

    """ Config structure """
    _fields_ = [("user_agent", c.c_char_p), ("dial_timeout_milliseconds", c.c_int32),
                ("temp_directory", c.c_char_p)]


class Bucket(c.Structure):

    """ Bucket structure """
    _fields_ = [("name", c.c_char_p), ("created", c.c_int64)]


class ListObjectsOptions(c.Structure):

    """ ListObjectsOptions structure """
    _fields_ = [("prefix", c.c_char_p), ("cursor", c.c_char_p), ("recursive", c.c_bool),
                ("system", c.c_bool), ("custom", c.c_bool)]


class ListBucketsOptions(c.Structure):

    """ ListBucketsOptions structure """
    _fields_ = [("cursor", c.c_char_p)]


class ObjectIterator(c.Structure):

    """ ObjectIterator structure """
    _fields_ = [("_handle", c.c_size_t)]


class BucketIterator(c.Structure):

    """ BucketIterator structure """
    _fields_ = [("_handle", c.c_size_t)]


class Permission(c.Structure):

    """ Permission structure """
    _fields_ = [("allow_download", c.c_bool), ("allow_upload", c.c_bool), ("allow_list", c.c_bool),
                ("allow_delete", c.c_bool), ("not_before", c.c_int64), ("not_after", c.c_int64)]


class SharePrefix(c.Structure):

    """ SharePrefix structure """
    _fields_ = [("bucket", c.c_char_p), ("prefix", c.c_char_p)]


# Various result structures:
class AccessResult(c.Structure):

    """ AccessResult structure """
    _fields_ = [("access", c.POINTER(Access)), ("error", c.POINTER(Error))]


class ProjectResult(c.Structure):

    """ ProjectResult structure """
    _fields_ = [("project", c.POINTER(Project)), ("error", c.POINTER(Error))]


class BucketResult(c.Structure):

    """ BucketResult structure """
    _fields_ = [("bucket", c.POINTER(Bucket)), ("error", c.POINTER(Error))]


class StringResult(c.Structure):

    """ StringResult structure """
    _fields_ = [("string", c.c_char_p), ("error", c.POINTER(Error))]


#########################################################
# Python Storj class with all Storj functions' bindings #
#########################################################

class LibUplinkPy(DataExchange):

    """ Python Storj class with all Storj functions' bindings """

    #
    def request_access_with_passphrase(self, satellite, api_key, passphrase):
        """
        function requests satellite for a new access grant using a passphrase
        pre-requisites: none
        inputs: Satellite Address (String), API key (String) and Passphrase (String)
        output: AccessResult (Object), Error (String) if any else None
        """
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.request_access_with_passphrase.argtypes = [c.c_char_p, c.c_char_p,
                                                                    c.c_char_p]
        self.m_libuplink.request_access_with_passphrase.restype = AccessResult
        #
        # prepare the input for the function
        satellite_ptr = c.c_char_p(satellite.encode('utf-8'))
        api_key_ptr = c.c_char_p(api_key.encode('utf-8'))
        passphrase_ptr = c.c_char_p(passphrase.encode('utf-8'))

        # get access to Storj by calling the exported golang function
        access_result = self.m_libuplink.request_access_with_passphrase(satellite_ptr,
                                                                        api_key_ptr,
                                                                        passphrase_ptr)
        #
        # if error occurred
        if bool(access_result.error):
            return access_result, access_result.error.contents.message.decode("utf-8")
        return access_result, None

    def config_request_access_with_passphrase(self, po_config, satellite, api_key,
                                              passphrase):
        """
        function requests satellite for a new access grant using a passphrase and
                        custom configuration
        pre-requisites: none
        inputs: Config (Object), Satellite Address (String), API key (String) and
                Passphrase (String)
        output: AccessResult (Object), Error (String) if any else None
        """
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.config_request_access_with_passphrase.argtypes = [Config, c.c_char_p,
                                                                           c.c_char_p, c.c_char_p]
        self.m_libuplink.config_request_access_with_passphrase.restype = AccessResult
        #
        # prepare the input for the function
        if po_config is None:
            config = Config()
        else:
            config = po_config
        satellite_ptr = c.c_char_p(satellite.encode('utf-8'))
        api_key_ptr = c.c_char_p(api_key.encode('utf-8'))
        passphrase_ptr = c.c_char_p(passphrase.encode('utf-8'))

        # get access to Storj by calling the exported golang function
        access_result = self.m_libuplink.config_request_access_with_passphrase(config,
                                                                               satellite_ptr,
                                                                               api_key_ptr,
                                                                               passphrase_ptr)
        #
        # if error occurred
        if bool(access_result.error):
            return access_result, access_result.error.contents.message.decode("utf-8")
        return access_result, None

    def open_project(self, po_access):
        """
        function opens Storj(V3) project using access grant.
        pre-requisites: request_access_with_passphrase or parse_access function
                        has been already called
        inputs: Access (Object)
        output: ProjectResult (Object), Error (String) if any else None
        """
        #
        # ensure access object is already created
        if po_access is None:
            ls_error = "Invalid access object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.open_project.argtypes = [c.POINTER(Access)]
        self.m_libuplink.open_project.restype = ProjectResult
        #
        # open project by calling the exported golang function
        project_result = self.m_libuplink.open_project(po_access)
        #
        # if error occurred
        if bool(project_result.error):
            return project_result, project_result.error.contents.message.decode("utf-8")
        return project_result, None

    def config_open_project(self, config, access):
        """
        function opens Storj(V3) project using access grant and custom configuration.
        pre-requisites: request_access_with_passphrase or parse_access function
                        has been already called
        inputs: Config (Object), Access (Object)
        output: ProjectResult (Object), Error (String) if any else None
        """
        #
        # ensure access object is already created
        if access is None:
            ls_error = "Invalid access object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.config_open_project.argtypes = [Config, c.POINTER(Access)]
        self.m_libuplink.config_open_project.restype = ProjectResult
        #
        # prepare the input for the function
        if config is None:
            config = Config()
        #
        # open project by calling the exported golang function
        project_result = self.m_libuplink.config_open_project(config, access)
        #
        # if error occurred
        if bool(project_result.error):
            return project_result, project_result.error.contents.message.decode("utf-8")
        return project_result, None

    def ensure_bucket(self, project, bucket_name):
        """
        function creates a new bucket and ignores the error when it already exists
        pre-requisites: open_project function has been already called
        inputs: Project (Object) ,Bucket Name (String)
        output: BucketResult (Object), Error (String) if any else None
        """
        #
        # ensure project object is valid
        if project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.ensure_bucket.argtypes = [c.POINTER(Project), c.c_char_p]
        self.m_libuplink.ensure_bucket.restype = BucketResult
        #
        # prepare the input for the function
        bucket_name_ptr = c.c_char_p(bucket_name.encode('utf-8'))

        # open bucket if doesn't exist by calling the exported golang function
        bucket_result = self.m_libuplink.ensure_bucket(project, bucket_name_ptr)
        #
        # if error occurred
        if bool(bucket_result.error):
            return bucket_result, bucket_result.error.contents.message.decode("utf-8")
        return bucket_result, None

    def stat_bucket(self, project, bucket_name):
        """
        function returns information about a bucket.
        pre-requisites: open_project function has been already called
        inputs: Project (Object) ,Bucket Name (String)
        output: BucketResult (Object), Error (String) if any else None
        """
        #
        # ensure project object is valid
        if project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.stat_bucket.argtypes = [c.POINTER(Project), c.c_char_p]
        self.m_libuplink.stat_bucket.restype = BucketResult
        #
        # prepare the input for the function
        bucket_name_ptr = c.c_char_p(bucket_name.encode('utf-8'))

        # get bucket information by calling the exported golang function
        bucket_result = self.m_libuplink.stat_bucket(project, bucket_name_ptr)
        #
        # if error occurred
        if bool(bucket_result.error):
            return bucket_result, bucket_result.error.contents.message.decode("utf-8")
        return bucket_result, None

    def stat_object(self, project, bucket_name, storj_path):
        """
        function returns information about an object at the specific key.
        pre-requisites: open_project
        inputs: Project (Object) ,Bucket Name (String) , Object Key(String)
        output: ObjectResult (Object), Error (string) if any else None
        """
        #
        # ensure project object is valid
        if project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.stat_object.argtypes = [c.POINTER(Project), c.c_char_p, c.c_char_p]
        self.m_libuplink.stat_object.restype = ObjectResult
        #
        # prepare the input for the function
        bucket_name_ptr = c.c_char_p(bucket_name.encode('utf-8'))
        storj_path_ptr = c.c_char_p(storj_path.encode('utf-8'))

        # get object information by calling the exported golang function
        object_result = self.m_libuplink.stat_object(project, bucket_name_ptr,
                                                     storj_path_ptr)
        #
        # if error occurred
        if bool(object_result.error):
            return object_result, object_result.error.contents.message.decode("utf-8")
        return object_result, None

    def create_bucket(self, project, bucket_name):
        """
        function creates a new bucket.
        pre-requisites: open_project function has been already called
        inputs: Project (Object) ,Bucket Name (String)
        output: BucketResult (Object), Error (String) if any else None
        """
        #
        # ensure project object is valid
        if project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.create_bucket.argtypes = [c.POINTER(Project), c.c_char_p]
        self.m_libuplink.create_bucket.restype = BucketResult
        #
        # prepare the input for the function
        bucket_name_ptr = c.c_char_p(bucket_name.encode('utf-8'))

        # create bucket by calling the exported golang function
        bucket_result = self.m_libuplink.create_bucket(project, bucket_name_ptr)
        #
        # if error occurred
        if bool(bucket_result.error):
            return bucket_result, bucket_result.error.contents.message.decode("utf-8")
        return bucket_result, None

    def close_project(self, project):
        """
        function closes the Storj(V3) project.
        pre-requisites: open_project function has been already called
        inputs: Project (Object)
        output: Error (Object) if any else None
        """
        #
        # ensure project object is valid
        if project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.close_project.argtypes = [c.POINTER(Project)]
        self.m_libuplink.close_project.restype = c.POINTER(Error)
        #
        # close Storj project by calling the exported golang function
        error = self.m_libuplink.close_project(project)
        #
        # if error occurred
        if bool(error):
            return error
        return None

    def list_buckets(self, project, list_bucket_options):
        """
        function lists buckets
        pre-requisites: open_project function has been already called
        inputs: Project (Object), ListBucketsOptions (Object)
        output: Bucket List (Python List), Error (String) if any else None
        """
        #
        # ensure project object is valid
        if project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.list_buckets.argtypes = [c.POINTER(Project), c.POINTER(ListBucketsOptions)]
        self.m_libuplink.list_buckets.restype = c.POINTER(BucketIterator)
        #
        self.m_libuplink.bucket_iterator_item.argtypes = [c.POINTER(BucketIterator)]
        self.m_libuplink.bucket_iterator_item.restype = c.POINTER(Bucket)
        #
        self.m_libuplink.bucket_iterator_next.argtypes = [c.POINTER(BucketIterator)]
        self.m_libuplink.bucket_iterator_next.restype = c.c_bool
        #
        # prepare the input for the function
        if list_bucket_options is None:
            list_bucket_options_obj = c.POINTER(ListBucketsOptions)()
        else:
            list_bucket_options_obj = c.byref(list_bucket_options)

        # get bucket list by calling the exported golang function
        bucket_iterator = self.m_libuplink.list_buckets(project, list_bucket_options_obj)
        bucket_list = list()
        while self.m_libuplink.bucket_iterator_next(bucket_iterator):
            bucket_list.append(self.m_libuplink.bucket_iterator_item(bucket_iterator))

        #
        # if error occurred
        if len(bucket_list) == 0:
            return None, "No bucket found!"
        return bucket_list, None

    def list_objects(self, project, bucket_name, list_object_options):
        """
        function lists objects
        pre-requisites: open_project function has been already called
        inputs: Project (Object), Bucket Name (String), ListObjectsOptions (Object)
        output: Bucket List (Python List), Error (String) if any else None
        """
        #
        # ensure project object is valid
        if project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.list_objects.argtypes = [c.POINTER(Project), c.c_char_p,
                                                  c.POINTER(ListObjectsOptions)]
        self.m_libuplink.list_objects.restype = c.POINTER(ObjectIterator)
        #
        self.m_libuplink.object_iterator_item.argtypes = [c.POINTER(ObjectIterator)]
        self.m_libuplink.object_iterator_item.restype = c.POINTER(Object)
        #
        self.m_libuplink.object_iterator_next.argtypes = [c.POINTER(ObjectIterator)]
        self.m_libuplink.object_iterator_next.restype = c.c_bool
        #
        # prepare the input for the function
        if list_object_options is None:
            list_object_options_obj = c.POINTER(ListObjectsOptions)()
        else:
            list_object_options_obj = c.byref(list_object_options)
        bucket_name_ptr = c.c_char_p(bucket_name.encode('utf-8'))

        # get object list by calling the exported golang function
        object_iterator = self.m_libuplink.list_objects(project, bucket_name_ptr,
                                                        list_object_options_obj)
        object_list = list()
        while self.m_libuplink.object_iterator_next(object_iterator):
            object_list.append(self.m_libuplink.object_iterator_item(object_iterator))

        #
        # if error occurred
        if len(object_list) == 0:
            return None, "No object found!"
        return object_list, None

    def delete_bucket(self, project, bucket_name):
        """
        function deletes a bucket.
        pre-requisites: open_project function has been already called
        inputs: Project (Object), Bucket Name (String)
        output: BucketResult (Object), Error (String) if any else None
        """
        #
        # ensure project handle and encryption handles are valid
        if project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.delete_bucket.argtypes = [c.POINTER(Project), c.c_char_p]
        self.m_libuplink.delete_bucket.restype = BucketResult
        #
        # prepare the input for the function
        bucket_name_ptr = c.c_char_p(bucket_name.encode('utf-8'))

        # delete bucket by calling the exported golang function
        bucket_result = self.m_libuplink.delete_bucket(project, bucket_name_ptr)
        #
        # if error occurred
        if bool(bucket_result.error):
            return bucket_result, bucket_result.error.contents.message.decode("utf-8")
        return bucket_result, None

    def delete_object(self, project, bucket_name, storj_path):
        """
        function deletes an object.
        pre-requisites: open_project function has been already called
        inputs: Project (Object), Bucket Name (String), Object Key (String)
        output: ObjectResult (Object), Error (String) if any else None
        """
        #
        # ensure project handle and encryption handles are valid
        if project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.delete_object.argtypes = [c.POINTER(Project), c.c_char_p, c.c_char_p]
        self.m_libuplink.delete_object.restype = ObjectResult
        #
        # prepare the input for the function
        bucket_name_ptr = c.c_char_p(bucket_name.encode('utf-8'))
        storj_path_ptr = c.c_char_p(storj_path.encode('utf-8'))

        # delete object by calling the exported golang function
        object_result = self.m_libuplink.delete_object(project, bucket_name_ptr,
                                                       storj_path_ptr)
        #
        # if error occurred
        if bool(object_result.error):
            return object_result, object_result.error.contents.message.decode("utf-8")
        return object_result, None

    def parse_access(self, serialized_access):
        """
        function to parses serialized access grant string
        pre-requisites: none
        inputs: Serialized Access (String)
        output: AccessResult (Object), Error (String) if any else None
        """
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.parse_access.argtypes = [c.c_char_p]
        self.m_libuplink.parse_access.restype = AccessResult
        #

        # get parsed access by calling the exported golang function
        access_result = self.m_libuplink.parse_access(serialized_access)
        #
        # if error occurred
        if bool(access_result.error):
            return access_result, access_result.error.contents.message.decode("utf-8")
        return access_result, None

    def access_serialize(self, access):
        """
        function serializes access grant into a string.
        pre-requisites: request_access_with_passphrase or parse_access function
                        has been already called
        inputs: Access (Object)
        output: StringResult (Object), Error (String) if any else None
        """
        #
        # ensure access object is valid
        if access is None:
            ls_error = "Invalid access object, please check parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.access_serialize.argtypes = [c.POINTER(Access)]
        self.m_libuplink.access_serialize.restype = StringResult
        #
        # get serialized access by calling the exported golang function
        string_result = self.m_libuplink.access_serialize(access)
        #
        # if error occurred
        if bool(string_result.error):
            return string_result, string_result.error.contents.message.decode("utf-8")
        return string_result, None

    def access_share(self, access, permission, shared_prefix):
        """
        function creates new access grant with specific permission. Permission will
                        be applied to prefixes when defined.
        pre-requisites: request_access_with_passphrase or parse_access function has
                        been already called
        inputs: Access (Object), Permission (Object), Share Prefix (Python List of Dictionaries)
        output: String Result (Object), Error (String) if any else None
        """
        #
        # ensure access object is valid
        if access is None:
            ls_error = "Invalid access object, please check parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.access_share.argtypes = [c.POINTER(Access), Permission,
                                                  c.POINTER(SharePrefix), c.c_size_t]
        self.m_libuplink.access_share.restype = AccessResult
        #
        # prepare the input for the function
        # check and create valid Permission parameter
        if permission is None:
            permission = Permission()

        # check and create valid Share Prefix parameter
        # shared_prefix = [{"bucket": "bucket01", "prefix": "uploadPath01/data"}]
        if shared_prefix is None:
            shared_prefix = c.POINTER(SharePrefix)()
            array_size = c.c_size_t(0)
        else:
            num_of_structs = len(shared_prefix)
            li_array_size = (SharePrefix * num_of_structs)()
            array = c.cast(li_array_size, c.POINTER(SharePrefix))
            for i, val in enumerate(shared_prefix):
                array[i] = SharePrefix(c.c_char_p(val['bucket'].encode('utf-8')),
                                       c.c_char_p(val['prefix'].encode('utf-8')))
            shared_prefix = array
            array_size = c.c_size_t(num_of_structs)
        #
        # get shareable access by calling the exported golang function
        access_result = self.m_libuplink.access_share(access, permission, shared_prefix,
                                                      array_size)
        #
        # if error occurred
        if bool(access_result.error):
            return access_result, access_result.error.contents.message.decode("utf-8")
        return access_result, None
