# pylint: disable=too-few-public-methods, too-many-arguments
"""Python Binding's Uplink Module for Storj (V3)"""

import ctypes
import os
import sysconfig

from uplink_python.access import Access
from uplink_python.errors import _storj_exception, LibUplinkSoError
from uplink_python.module_def import _AccessResult, _ConfigStruct
from uplink_python.module_classes import Config, Bucket, Object, SystemMetadata, \
    CustomMetadataEntry, CustomMetadata


class Uplink:
    """
    Python Storj Uplink class to initialize and get access grant to Storj (V3)"

    ...

    Attributes
    ----------
    m_libuplink : CDLL
        Instance to the libuplinkc.so.

    Methods
    -------
    object_from_result(object_=object_result.object):
        Object
    bucket_from_result(bucket=bucket_result.bucket):
        Bucket
    """

    __instance = None

    def __init__(self):
        """Constructs all the necessary attributes for the Uplink object."""
        # private members of PyStorj class with reference objects
        # include the golang exported libuplink library functions
        if Uplink.__instance is None:
            so_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libuplinkc.so')
            if os.path.exists(so_path):
                self.m_libuplink = ctypes.CDLL(so_path)
            else:
                new_path = os.path.join(sysconfig.get_paths()['purelib'], "uplink_python",
                                        'libuplinkc.so')
                if os.path.exists(new_path):
                    self.m_libuplink = ctypes.CDLL(so_path)
                else:
                    raise LibUplinkSoError
            Uplink.__instance = self
        else:
            self.m_libuplink = Uplink.__instance.m_libuplink

    @classmethod
    def object_from_result(cls, object_):
        """Converts ctypes structure _ObjectStruct to python class object."""

        system = SystemMetadata(created=object_.contents.system.created,
                                expires=object_.contents.system.expires,
                                content_length=object_.contents.system.content_length)

        array_size = object_.contents.custom.count
        entries = list()
        for i in range(array_size):
            if bool(object_.contents.custom.entries[i]):
                entries_obj = object_.contents.custom.entries[i]
                entries.append(CustomMetadataEntry(key=entries_obj.key.decode("utf-8"),
                                                   key_length=entries_obj.key_length,
                                                   value=entries_obj.value.decode("utf-8"),
                                                   value_length=entries_obj.value_length))
            else:
                entries.append(CustomMetadataEntry())

        return Object(key=object_.contents.key.decode("utf-8"),
                      is_prefix=object_.contents.is_prefix,
                      system=system,
                      custom=CustomMetadata(entries=entries,
                                            count=object_.contents.custom.count))

    @classmethod
    def bucket_from_result(cls, bucket_):
        """Converts ctypes structure _BucketStruct to python class object."""

        return Bucket(name=bucket_.contents.name.decode("utf-8"),
                      created=bucket_.contents.created)

    #
    def request_access_with_passphrase(self, satellite: str, api_key: str, passphrase: str):
        """
        RequestAccessWithPassphrase generates a new access grant using a passhprase.
        It must talk to the Satellite provided to get a project-based salt for deterministic
        key derivation.

        Note: this is a CPU-heavy function that uses a password-based key derivation
        function (Argon2). This should be a setup-only step.
        Most common interactions with the library should be using a serialized access grant
        through ParseAccess directly.

        Parameters
        ----------
        satellite : str
        api_key : str
        passphrase : str

        Returns
        -------
        Access
        """
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.uplink_request_access_with_passphrase.argtypes = [ctypes.c_char_p,
                                                                           ctypes.c_char_p,
                                                                           ctypes.c_char_p]
        self.m_libuplink.uplink_request_access_with_passphrase.restype = _AccessResult
        #
        # prepare the input for the function
        satellite_ptr = ctypes.c_char_p(satellite.encode('utf-8'))
        api_key_ptr = ctypes.c_char_p(api_key.encode('utf-8'))
        passphrase_ptr = ctypes.c_char_p(passphrase.encode('utf-8'))

        # get access to Storj by calling the exported golang function
        access_result = self.m_libuplink.uplink_request_access_with_passphrase(satellite_ptr,
                                                                               api_key_ptr,
                                                                               passphrase_ptr)
        #
        # if error occurred
        if bool(access_result.error):
            raise _storj_exception(access_result.error.contents.code,
                                   access_result.error.contents.message.decode("utf-8"))
        return Access(access_result.access, self)

    def config_request_access_with_passphrase(self, config: Config, satellite: str, api_key: str,
                                              passphrase: str):
        """
        RequestAccessWithPassphrase generates a new access grant using a passhprase and
        custom configuration.
        It must talk to the Satellite provided to get a project-based salt for deterministic
        key derivation.

        Note: this is a CPU-heavy function that uses a password-based key derivation
        function (Argon2). This should be a setup-only step.
        Most common interactions with the library should be using a serialized access grant
        through ParseAccess directly.

        Parameters
        ----------
        config: Config
        satellite : str
        api_key : str
        passphrase : str

        Returns
        -------
        Access
        """

        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.uplink_config_request_access_with_passphrase.argtypes = [_ConfigStruct,
                                                                                  ctypes.c_char_p,
                                                                                  ctypes.c_char_p,
                                                                                  ctypes.c_char_p]
        self.m_libuplink.uplink_config_request_access_with_passphrase.restype = _AccessResult
        #
        # prepare the input for the function
        if config is None:
            config_obj = _ConfigStruct()
        else:
            config_obj = config.get_structure()
        satellite_ptr = ctypes.c_char_p(satellite.encode('utf-8'))
        api_key_ptr = ctypes.c_char_p(api_key.encode('utf-8'))
        phrase_ptr = ctypes.c_char_p(passphrase.encode('utf-8'))

        # get access to Storj by calling the exported golang function
        access_result = self.m_libuplink.uplink_config_request_access_with_passphrase(config_obj,
                                                                                      satellite_ptr,
                                                                                      api_key_ptr,
                                                                                      phrase_ptr)
        #
        # if error occurred
        if bool(access_result.error):
            raise _storj_exception(access_result.error.contents.code,
                                   access_result.error.contents.message.decode("utf-8"))
        return Access(access_result.access, self)

    def parse_access(self, serialized_access: str):
        """
        ParseAccess parses a serialized access grant string.

        This should be the main way to instantiate an access grant for opening a project.
        See the note on RequestAccessWithPassphrase

        Parameters
        ----------
        serialized_access : str

        Returns
        -------
        Access
        """

        #
        # prepare the input for the function
        serialized_access_ptr = ctypes.c_char_p(serialized_access.encode('utf-8'))
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.uplink_parse_access.argtypes = [ctypes.c_char_p]
        self.m_libuplink.uplink_parse_access.restype = _AccessResult
        #

        # get parsed access by calling the exported golang function
        access_result = self.m_libuplink.uplink_parse_access(serialized_access_ptr)
        #
        # if error occurred
        if bool(access_result.error):
            raise _storj_exception(access_result.error.contents.code,
                                   access_result.error.contents.message.decode("utf-8"))
        return Access(access_result.access, self)
