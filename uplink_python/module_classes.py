"""Classes for input and output interface of parameters and returns from uplink."""
# pylint: disable=too-few-public-methods, too-many-arguments
import ctypes

from uplink_python.module_def import _ConfigStruct, _PermissionStruct, _SharePrefixStruct,\
    _BucketStruct, _DownloadOptionsStruct, _SystemMetadataStruct, _CustomMetadataStruct,\
    _UploadOptionsStruct, _ObjectStruct, _ListObjectsOptionsStruct, _ListBucketsOptionsStruct,\
    _CustomMetadataEntryStruct


class Config:
    """
    Config defines configuration for using uplink library.

    ...

    Attributes
    ----------
    user_agent : str
    dial_timeout_milliseconds : int
        DialTimeout defines how long client should wait for establishing a connection to peers.
    temp_directory : str
        temp_directory specifies where to save data during downloads to use less memory.

    Methods
    -------
    get_structure():
        _ConfigStruct
    """

    def __init__(self, user_agent: str = "", dial_timeout_milliseconds: int = 0,
                 temp_directory: str = ""):
        """Constructs all the necessary attributes for the Config object."""

        self.user_agent = user_agent
        self.dial_timeout_milliseconds = dial_timeout_milliseconds
        self.temp_directory = temp_directory

    def get_structure(self):
        """Converts python class object to ctypes structure _ConfigStruct"""

        return _ConfigStruct(ctypes.c_char_p(self.user_agent.encode('utf-8')),
                             ctypes.c_int32(self.dial_timeout_milliseconds),
                             ctypes.c_char_p(self.temp_directory.encode('utf-8')))


class Permission:
    """
    Permission defines what actions can be used to share.

    ...

    Attributes
    ----------
    allow_download : bool
        allow_download gives permission to download the object's content. It
        allows getting object metadata, but it does not allow listing buckets.
    allow_upload : bool
        allow_upload gives permission to create buckets and upload new objects.
        It does not allow overwriting existing objects unless allow_delete is
        granted too.
    allow_list : bool
        allow_list gives permission to list buckets. It allows getting object
        metadata, but it does not allow downloading the object's content.
    allow_delete : bool
        allow_delete gives permission to delete buckets and objects. Unless
        either allow_download or allow_list is granted too, no object metadata and
        no error info will be returned for deleted objects.
    not_before : int
        NotBefore restricts when the resulting access grant is valid for.
        If set, the resulting access grant will not work if the Satellite
        believes the time is before NotBefore.
        If set, this value should always be before NotAfter.
        disabled when 0.
    not_after : int
        NotAfter restricts when the resulting access grant is valid till.
        If set, the resulting access grant will not work if the Satellite
        believes the time is after NotAfter.
        If set, this value should always be after NotBefore.
        disabled when 0.

    Methods
    -------
    get_structure():
        _PermissionStruct
    """

    def __init__(self, allow_download: bool = False, allow_upload: bool = False,
                 allow_list: bool = False, allow_delete: bool = False,
                 not_before: int = 0, not_after: int = 0):
        """Constructs all the necessary attributes for the Permission object."""

        self.allow_download = allow_download
        self.allow_upload = allow_upload
        self.allow_list = allow_list
        self.allow_delete = allow_delete
        self.not_before = not_before
        self.not_after = not_after

    def get_structure(self):
        """Converts python class object to ctypes structure _PermissionStruct"""

        return _PermissionStruct(ctypes.c_bool(self.allow_download),
                                 ctypes.c_bool(self.allow_upload),
                                 ctypes.c_bool(self.allow_list),
                                 ctypes.c_bool(self.allow_delete),
                                 ctypes.c_int64(self.not_before),
                                 ctypes.c_int64(self.not_after))


class SharePrefix:
    """
    SharePrefix defines a prefix that will be shared.

    ...

    Attributes
    ----------
    bucket : str
    prefix : str
        Prefix is the prefix of the shared object keys.

        Note: that within a bucket, the hierarchical key derivation scheme is
        delineated by forward slashes (/), so encryption information will be
        included in the resulting access grant to decrypt any key that shares
        the same prefix up until the last slash.

    Methods
    -------
    get_structure():
        _SharePrefixStruct
    """

    def __init__(self, bucket: str = "", prefix: str = ""):
        """Constructs all the necessary attributes for the SharePrefix object."""

        self.bucket = bucket
        self.prefix = prefix

    def get_structure(self):
        """Converts python class object to ctypes structure _SharePrefixStruct"""

        return _SharePrefixStruct(ctypes.c_char_p(self.bucket.encode('utf-8')),
                                  ctypes.c_char_p(self.prefix.encode('utf-8')))


class Bucket:
    """
    Bucket contains information about the bucket.

    ...

    Attributes
    ----------
    name : str
    created : int

    Methods
    -------
    get_structure():
        _BucketStruct
    get_dict():
        converts python class object to python dictionary
    """

    def __init__(self, name: str = "", created: int = 0):
        """Constructs all the necessary attributes for the Bucket object."""

        self.name = name
        self.created = created

    def get_structure(self):
        """Converts python class object to ctypes structure _BucketStruct"""

        return _BucketStruct(ctypes.c_char_p(self.name.encode('utf-8')),
                             ctypes.c_int64(self.created))

    def get_dict(self):
        """Converts python class object to python dictionary"""

        return {"name": self.name, "created": self.created}


class SystemMetadata:
    """
    SystemMetadata contains information about the object that cannot be changed directly.

    ...

    Attributes
    ----------
    created : int
    expires : int
    content_length : int

    Methods
    -------
    get_structure():
        _SystemMetadataStruct
    get_dict():
        converts python class object to python dictionary
    """

    def __init__(self, created: int = 0, expires: int = 0, content_length: int = 0):
        """Constructs all the necessary attributes for the SystemMetadata object."""

        self.created = created
        self.expires = expires
        self.content_length = content_length

    def get_structure(self):
        """Converts python class object to ctypes structure _SystemMetadataStruct"""

        return _SystemMetadataStruct(ctypes.c_int64(self.created),
                                     ctypes.c_int64(self.expires),
                                     ctypes.c_int64(self.content_length))

    def get_dict(self):
        """Converts python class object to python dictionary"""

        return {"created": self.created, "expires": self.expires,
                "content_length": self.content_length}


class CustomMetadataEntry:
    """
    CustomMetadata contains custom user metadata about the object.

    When choosing a custom key for your application start it with a prefix "app:key",
    as an example application named"Image Board" might use a key "image-board:title".

    ...

    Attributes
    ----------
    key : str
    key_length : int
    value : str
    value_length : int

    Methods
    -------
    get_structure():
        _CustomMetadataEntryStruct
    get_dict():
        converts python class object to python dictionary
    """

    def __init__(self, key: str = "", key_length: int = 0, value: str = "", value_length: int = 0):
        """Constructs all the necessary attributes for the CustomMetadataEntry object."""

        self.key = key
        self.key_length = key_length
        self.value = value
        self.value_length = value_length

    def get_structure(self):
        """Converts python class object to ctypes structure _CustomMetadataEntryStruct"""

        return _CustomMetadataEntryStruct(ctypes.c_char_p(self.key.encode('utf-8')),
                                          ctypes.c_size_t(self.key_length),
                                          ctypes.c_char_p(self.value.encode('utf-8')),
                                          ctypes.c_size_t(self.value_length))

    def get_dict(self):
        """Converts python class object to python dictionary"""

        return {"key": self.key, "key_length": self.key_length, "value": self.value,
                "value_length": self.value_length}


class CustomMetadata:
    """
    CustomMetadata contains a list of CustomMetadataEntry about the object.

    ...

    Attributes
    ----------
    entries : list of CustomMetadataEntry
    count : int

    Methods
    -------
    get_structure():
        _CustomMetadataStruct
    get_dict():
        converts python class object to python dictionary
    """

    def __init__(self, entries: [CustomMetadataEntry] = None, count: int = 0):
        """Constructs all the necessary attributes for the CustomMetadata object."""

        self.entries = entries
        self.count = count

    def get_structure(self):
        """Converts python class object to ctypes structure _CustomMetadataStruct"""

        if self.entries is None or self.count == 0:
            self.count = 0
            entries = ctypes.POINTER(_CustomMetadataEntryStruct)()
        else:
            li_array_size = (_CustomMetadataEntryStruct * self.count)()
            entries = ctypes.cast(li_array_size, ctypes.POINTER(_CustomMetadataEntryStruct))
            for i, val in enumerate(self.entries):
                entries[i] = val.get_structure()

        return _CustomMetadataStruct(entries, ctypes.c_size_t(self.count))

    def get_dict(self):
        """Converts python class object to python dictionary"""

        entries = self.entries
        if entries is None or self.count == 0:
            self.count = 0
            entries = [CustomMetadataEntry()]
        return {"entries": [entry.get_dict() for entry in entries], "count": self.count}


class Object:
    """
    Object contains information about an object.

    ...

    Attributes
    ----------
    key : str
    is_prefix : bool
        is_prefix indicates whether the Key is a prefix for other objects.
    system : SystemMetadata
    custom : CustomMetadata

    Methods
    -------
    get_structure():
        _ObjectStruct
    get_dict():
        converts python class object to python dictionary
    """

    def __init__(self, key: str = "", is_prefix: bool = False, system: SystemMetadata = None,
                 custom: CustomMetadata = None):
        """Constructs all the necessary attributes for the Object object."""

        self.key = key
        self.is_prefix = is_prefix
        self.system = system
        self.custom = custom

    def get_structure(self):
        """Converts python class object to ctypes structure _ObjectStruct"""

        if self.system is None:
            system = _SystemMetadataStruct()
        else:
            system = self.system.get_structure()

        if self.custom is None:
            custom = _CustomMetadataStruct()
        else:
            custom = self.custom.get_structure()

        return _ObjectStruct(ctypes.c_char_p(self.key.encode('utf-8')),
                             ctypes.c_bool(self.is_prefix), system, custom)

    def get_dict(self):
        """Converts python class object to python dictionary"""

        system = self.system
        custom = self.custom
        if system is None:
            system = SystemMetadata()
        if custom is None:
            custom = CustomMetadata()
        return {"key": self.key, "is_prefix": self.is_prefix, "system": system.get_dict(),
                "custom": custom.get_dict()}


class ListObjectsOptions:
    """
    ListObjectsOptions defines object listing options.

    ...

    Attributes
    ----------
    prefix : str
        prefix allows to filter objects by a key prefix. If not empty,
        it must end with slash.
    cursor : str
        cursor sets the starting position of the iterator.
        The first item listed will be the one after the cursor.
    recursive : bool
        recursive iterates the objects without collapsing prefixes.
    system : bool
        system includes SystemMetadata in the results.
    custom : bool
        custom includes CustomMetadata in the results.

    Methods
    -------
    get_structure():
        _ListObjectsOptionsStruct
    """

    def __init__(self, prefix: str = "", cursor: str = "", recursive: bool = False,
                 system: bool = False, custom: bool = False):
        """Constructs all the necessary attributes for the ListObjectsOptions object."""

        self.prefix = prefix
        self.cursor = cursor
        self.recursive = recursive
        self.system = system
        self.custom = custom

    def get_structure(self):
        """Converts python class object to ctypes structure _ListObjectsOptionsStruct"""

        return _ListObjectsOptionsStruct(ctypes.c_char_p(self.prefix.encode('utf-8')),
                                         ctypes.c_char_p(self.cursor.encode('utf-8')),
                                         ctypes.c_bool(self.recursive),
                                         ctypes.c_bool(self.system),
                                         ctypes.c_bool(self.custom))


class ListBucketsOptions:
    """
    ListBucketsOptions defines bucket listing options.

    ...

    Attributes
    ----------
    cursor : str
        Cursor sets the starting position of the iterator.
        The first item listed will be the one after the cursor.

    Methods
    -------
    get_structure():
        _ListBucketsOptionsStruct
    """

    def __init__(self, cursor: str = ""):
        """Constructs all the necessary attributes for the ListBucketsOptions object."""

        self.cursor = cursor

    def get_structure(self):
        """Converts python class object to ctypes structure _ListBucketsOptionsStruct"""

        return _ListBucketsOptionsStruct(ctypes.c_char_p(self.cursor.encode('utf-8')))


class UploadOptions:
    """
    UploadOptions contains additional options for uploading.

    ...

    Attributes
    ----------
    expires : int
        When expires is 0 or negative, it means no expiration.

    Methods
    -------
    get_structure():
        _UploadOptionsStruct
    """

    def __init__(self, expires: int):
        """Constructs all the necessary attributes for the UploadOptions object."""

        self.expires = expires

    def get_structure(self):
        """Converts python class object to ctypes structure _UploadOptionsStruct"""

        return _UploadOptionsStruct(ctypes.c_int64(self.expires))


class DownloadOptions:
    """
    DownloadOptions contains additional options for downloading.

    ...

    Attributes
    ----------
    offset : int
    length : int
        When length is negative, it will read until the end of the blob.

    Methods
    -------
    get_structure():
        _DownloadOptionsStruct
    """

    def __init__(self, offset: int, length: int):
        """Constructs all the necessary attributes for the DownloadOptions object."""

        self.offset = offset
        self.length = length

    def get_structure(self):
        """Converts python class object to ctypes structure _DownloadOptionsStruct"""

        return _DownloadOptionsStruct(ctypes.c_int64(self.offset),
                                      ctypes.c_int64(self.length))
