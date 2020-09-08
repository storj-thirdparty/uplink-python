"""C-type Classes for input and output interaction with libuplinkc."""
# pylint: disable=too-few-public-methods
import ctypes


class _ConfigStruct(ctypes.Structure):
    """Config ctypes structure for internal processing."""

    _fields_ = [("user_agent", ctypes.c_char_p), ("dial_timeout_milliseconds", ctypes.c_int32),
                ("temp_directory", ctypes.c_char_p)]


class _AccessStruct(ctypes.Structure):
    """Access ctypes structure for internal processing."""

    _fields_ = [("_handle", ctypes.c_size_t)]


class _EncryptionKeyStruct(ctypes.Structure):
    """Project ctypes structure for internal processing."""

    _fields_ = [("_handle", ctypes.c_size_t)]


class _PermissionStruct(ctypes.Structure):
    """Permission ctypes structure for internal processing."""

    _fields_ = [("allow_download", ctypes.c_bool), ("allow_upload", ctypes.c_bool),
                ("allow_list", ctypes.c_bool), ("allow_delete", ctypes.c_bool),
                ("not_before", ctypes.c_int64), ("not_after", ctypes.c_int64)]


class _SharePrefixStruct(ctypes.Structure):
    """SharePrefix ctypes structure for internal processing."""

    _fields_ = [("bucket", ctypes.c_char_p), ("prefix", ctypes.c_char_p)]


class _BucketStruct(ctypes.Structure):
    """Bucket ctypes structure for internal processing."""

    _fields_ = [("name", ctypes.c_char_p), ("created", ctypes.c_int64)]


class _ProjectStruct(ctypes.Structure):
    """Project ctypes structure for internal processing."""

    _fields_ = [("_handle", ctypes.c_size_t)]


class _SystemMetadataStruct(ctypes.Structure):
    """SystemMetadata ctypes structure for internal processing."""

    _fields_ = [("created", ctypes.c_int64), ("expires", ctypes.c_int64),
                ("content_length", ctypes.c_int64)]


class _CustomMetadataEntryStruct(ctypes.Structure):
    """CustomMetadataEntry ctypes structure for internal processing."""

    _fields_ = [("key", ctypes.c_char_p), ("key_length", ctypes.c_size_t),
                ("value", ctypes.c_char_p), ("value_length", ctypes.c_size_t)]


class _CustomMetadataStruct(ctypes.Structure):
    """CustomMetadata ctypes structure for internal processing."""

    _fields_ = [("entries", ctypes.POINTER(_CustomMetadataEntryStruct)), ("count", ctypes.c_size_t)]


class _ObjectStruct(ctypes.Structure):
    """Object ctypes structure for internal processing."""

    _fields_ = [("key", ctypes.c_char_p), ("is_prefix", ctypes.c_bool),
                ("system", _SystemMetadataStruct), ("custom", _CustomMetadataStruct)]


class _ListObjectsOptionsStruct(ctypes.Structure):
    """ListObjectsOptions ctypes structure for internal processing."""

    _fields_ = [("prefix", ctypes.c_char_p), ("cursor", ctypes.c_char_p),
                ("recursive", ctypes.c_bool), ("system", ctypes.c_bool), ("custom", ctypes.c_bool)]


class _ListBucketsOptionsStruct(ctypes.Structure):
    """ListBucketsOptions ctypes structure for internal processing."""

    _fields_ = [("cursor", ctypes.c_char_p)]


class _ObjectIterator(ctypes.Structure):
    """ObjectIterator ctypes structure"""

    _fields_ = [("_handle", ctypes.c_size_t)]


class _BucketIterator(ctypes.Structure):
    """BucketIterator ctypes structure for internal processing"""

    _fields_ = [("_handle", ctypes.c_size_t)]


class _UploadStruct(ctypes.Structure):
    """Upload ctypes structure for internal processing."""

    _fields_ = [("_handle", ctypes.c_size_t)]


class _UploadOptionsStruct(ctypes.Structure):
    """UploadOptions ctypes structure for internal processing."""

    _fields_ = [("expires", ctypes.c_int64)]


class _DownloadStruct(ctypes.Structure):
    """Download ctypes structure for internal processing."""

    _fields_ = [("_handle", ctypes.c_size_t)]


class _DownloadOptionsStruct(ctypes.Structure):
    """DownloadOptions ctypes structure for internal processing."""

    _fields_ = [("offset", ctypes.c_int64), ("length", ctypes.c_int64)]


class _Error(ctypes.Structure):
    """Error ctypes structure for internal processing."""

    _fields_ = [("code", ctypes.c_int32), ("message", ctypes.c_char_p)]


class _ProjectResult(ctypes.Structure):
    """ProjectResult ctypes structure"""

    _fields_ = [("project", ctypes.POINTER(_ProjectStruct)), ("error", ctypes.POINTER(_Error))]


class _BucketResult(ctypes.Structure):
    """BucketResult ctypes structure"""

    _fields_ = [("bucket", ctypes.POINTER(_BucketStruct)), ("error", ctypes.POINTER(_Error))]


class _UploadResult(ctypes.Structure):
    """UploadResult ctypes structure"""

    _fields_ = [("upload", ctypes.POINTER(_UploadStruct)), ("error", ctypes.POINTER(_Error))]


class _DownloadResult(ctypes.Structure):
    """DownloadResult ctypes structure"""

    _fields_ = [("download", ctypes.POINTER(_DownloadStruct)), ("error", ctypes.POINTER(_Error))]


class _AccessResult(ctypes.Structure):
    """AccessResult ctypes structure"""

    _fields_ = [("access", ctypes.POINTER(_AccessStruct)), ("error", ctypes.POINTER(_Error))]


class _StringResult(ctypes.Structure):
    """StringResult ctypes structure"""

    _fields_ = [("string", ctypes.c_char_p), ("error", ctypes.POINTER(_Error))]


class _ObjectResult(ctypes.Structure):
    """ObjectResult ctypes structure"""

    _fields_ = [("object", ctypes.POINTER(_ObjectStruct)), ("error", ctypes.POINTER(_Error))]


class _WriteResult(ctypes.Structure):
    """WriteResult ctypes structure"""

    _fields_ = [("bytes_written", ctypes.c_size_t), ("error", ctypes.POINTER(_Error))]


class _ReadResult(ctypes.Structure):
    """ReadResult ctypes structure"""

    _fields_ = [("bytes_read", ctypes.c_size_t), ("error", ctypes.POINTER(_Error))]


class _EncryptionKeyResult(ctypes.Structure):
    """EncryptionKeyResult ctypes structure"""

    _fields_ = [("encryption_key", ctypes.POINTER(_EncryptionKeyStruct)),
                ("error", ctypes.POINTER(_Error))]
