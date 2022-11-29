"""Module with Access class and access methods to get access grant to access project"""
import ctypes
import hashlib

from uplink_python.module_classes import Permission, SharePrefix, Config
from uplink_python.module_def import _ConfigStruct, _PermissionStruct, _SharePrefixStruct, \
    _AccessStruct, _ProjectResult, _StringResult, _AccessResult, _EncryptionKeyResult,\
    _EncryptionKeyStruct
from uplink_python.project import Project


class Access:
    """
    An Access Grant contains everything to access a project and specific buckets.
    It includes a potentially-restricted API Key, a potentially-restricted set of encryption
    information, and information about the Satellite responsible for the project's metadata.

    ...

    Attributes
    ----------
    access : int
        Access _handle returned from libuplinkc access_result.access
    uplink : Uplink
        uplink object used to get access

    Methods
    -------
    derive_encryption_key()
        EncryptionKey
    override_encryption_key()
        None
    open_project():
        Project
    config_open_project():
        Project
    serialize():
        String
    share():
        Access
    """

    def __init__(self, access, uplink):
        """Constructs all the necessary attributes for the Access object."""

        self.access = access
        self.uplink = uplink

    def derive_encryption_key(self, passphrase: str, salt: str):
        """
        function derives a salted encryption key for passphrase using the salt.

        This function is useful for deriving a salted encryption key for users when
        implementing multitenancy in a single app bucket.

        Returns
        -------
        EncryptionKey
        """

        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_derive_encryption_key.argtypes = [ctypes.c_char_p,
                                                                         ctypes.c_void_p,
                                                                         ctypes.c_size_t]
        self.uplink.m_libuplink.uplink_derive_encryption_key.restype = _EncryptionKeyResult
        #
        # prepare the input for the function
        passphrase_ptr = ctypes.c_char_p(passphrase.encode('utf-8'))
        hash_value = hashlib.sha256()  # Choose SHA256 and update with bytes
        hash_value.update(bytes(salt))
        salt_ptr = ctypes.c_void_p(hash_value.hexdigest())
        length_ptr = ctypes.c_size_t(hash_value.digest_size)

        # salted encryption key by calling the exported golang function
        encryption_key_result = self.uplink.m_libuplink.uplink_derive_encryption_key(passphrase_ptr,
                                                                                     salt_ptr,
                                                                                     length_ptr)
        return self.uplink.unwrap_encryption_key_result(encryption_key_result)

    def override_encryption_key(self, bucket_name: str, prefix: str, encryption_key):
        """
        function overrides the root encryption key for the prefix in bucket with encryptionKey.

        This function is useful for overriding the encryption key in user-specific
        access grants when implementing multitenancy in a single app bucket.

        Returns
        -------
        None
        """

        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_access_override_encryption_key.argtypes =\
            [ctypes.POINTER(_AccessStruct), ctypes.c_char_p, ctypes.c_char_p,
             ctypes.POINTER(_EncryptionKeyStruct)]
        self.uplink.m_libuplink.uplink_access_override_encryption_key.restype =\
            _EncryptionKeyResult
        #
        # prepare the input for the function
        bucket_name_ptr = ctypes.c_char_p(bucket_name.encode('utf-8'))
        prefix_ptr = ctypes.c_char_p(prefix.encode('utf-8'))

        # salted encryption key by calling the exported golang function
        error_result = self.uplink.m_libuplink.\
            uplink_access_override_encryption_key(self.access, bucket_name_ptr, prefix_ptr,
                                                  encryption_key)
        #
        # if error occurred
        if bool(error_result):
            self.uplink.free_error_and_raise_exception(error_result)

    def open_project(self):
        """
        function opens Storj(V3) project using access grant.

        Returns
        -------
        Project
        """

        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_open_project.argtypes = [ctypes.POINTER(_AccessStruct)]
        self.uplink.m_libuplink.uplink_open_project.restype = _ProjectResult
        #
        # open project by calling the exported golang function
        project_result = self.uplink.m_libuplink.uplink_open_project(self.access)

        _unwrapped_project = self.uplink.unwrap_project_result(project_result)

        return Project(_unwrapped_project, self.uplink)

    def config_open_project(self, config: Config):
        """
        function opens Storj(V3) project using access grant and custom configuration.

        Parameters
        ----------
        config : Config

        Returns
        -------
        Project
        """

        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_config_open_project.argtypes =\
            [_ConfigStruct, ctypes.POINTER(_AccessStruct)]
        self.uplink.m_libuplink.uplink_config_open_project.restype = _ProjectResult
        self.uplink.m_libuplink.uplink_free_project_result.argtypes = [_ProjectResult]
        #
        # prepare the input for the function
        if config is None:
            config_obj = _ConfigStruct()
        else:
            config_obj = config.get_structure()
        #
        # open project by calling the exported golang function
        project_result = self.uplink.m_libuplink.uplink_config_open_project(config_obj, self.access)

        _unwrapped_project = self.uplink.unwrap_project_result(project_result)

        return Project(_unwrapped_project, self.uplink)


    def serialize(self):
        """
        function serializes an access grant such that it can be used later
        with ParseAccess or other tools.

        Returns
        -------
        String
        """

        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_access_serialize.argtypes = [ctypes.POINTER(_AccessStruct)]
        self.uplink.m_libuplink.uplink_access_serialize.restype = _StringResult
        self.uplink.m_libuplink.uplink_free_string_result.argtypes = [_StringResult]
        #
        # get serialized access by calling the exported golang function
        string_result = self.uplink.m_libuplink.uplink_access_serialize(self.access)

        _unwrapped_string = self.uplink.unwrap_string_result(string_result)

        serialized_access = _unwrapped_string.decode("utf-8")
        self.uplink.m_libuplink.uplink_free_string_result(string_result)
        return serialized_access

    def share(self, permission: Permission = None, shared_prefix: [SharePrefix] = None):
        """
        function Share creates a new access grant with specific permissions.

        Access grants can only have their existing permissions restricted, and the resulting
        access grant will only allow for the intersection of all previous Share calls in the
        access grant construction chain.

        Prefixes, if provided, restrict the access grant (and internal encryption information)
        to only contain enough information to allow access to just those prefixes.

        Parameters
        ----------
        permission : Permission
        shared_prefix : list of SharePrefix

        Returns
        -------
        Access
        """

        #
        # declare types of arguments and response of the corresponding golang function
        self.uplink.m_libuplink.uplink_access_share.argtypes = [ctypes.POINTER(_AccessStruct),
                                                                _PermissionStruct,
                                                                ctypes.POINTER(_SharePrefixStruct),
                                                                ctypes.c_size_t]
        self.uplink.m_libuplink.uplink_access_share.restype = _AccessResult
        self.uplink.m_libuplink.uplink_free_access_result.argtypes = [_AccessResult]
        #
        # prepare the input for the function
        # check and create valid _PermissionStruct parameter
        if permission is None:
            permission_obj = _PermissionStruct()
        else:
            permission_obj = permission.get_structure()

        # check and create valid Share Prefix parameter
        if shared_prefix is None:
            shared_prefix_obj = ctypes.POINTER(_SharePrefixStruct)()
            array_size = ctypes.c_size_t(0)
        else:
            num_of_structs = len(shared_prefix)
            li_array_size = (_SharePrefixStruct * num_of_structs)()
            array = ctypes.cast(li_array_size, ctypes.POINTER(_SharePrefixStruct))
            for i, val in enumerate(shared_prefix):
                array[i] = val.get_structure()
            shared_prefix_obj = array
            array_size = ctypes.c_size_t(num_of_structs)
        #
        # get shareable access by calling the exported golang function
        access_result = self.uplink.m_libuplink.uplink_access_share(self.access, permission_obj,
                                                                    shared_prefix_obj, array_size)

        _unwrapped_access = self.uplink.unwrap_access_result(access_result)
        return Access(_unwrapped_access, self.uplink)


    def __del__(self):
        """Free memory associated to this Access"""
        self.uplink.free_access_struct(self.access)
