"""Python user-defined exceptions for uplink errors"""

ERROR_INTERNAL = 0x02
ERROR_CANCELED = 0x03
ERROR_INVALID_HANDLE = 0x04
ERROR_TOO_MANY_REQUESTS = 0x05
ERROR_BANDWIDTH_LIMIT_EXCEEDED = 0x06
ERROR_STORAGE_LIMIT_EXCEEDED = 0x07
ERROR_SEGMENTS_LIMIT_EXCEEDED = 0x08
ERROR_PERMISSION_DENIED = 0x09

ERROR_BUCKET_NAME_INVALID = 0x10
ERROR_BUCKET_ALREADY_EXISTS = 0x11
ERROR_BUCKET_NOT_EMPTY = 0x12
ERROR_BUCKET_NOT_FOUND = 0x13

ERROR_OBJECT_KEY_INVALID = 0x20
ERROR_OBJECT_NOT_FOUND = 0x21
ERROR_UPLOAD_DONE = 0x22

ERROR_AUTH_DIAL_FAILED = 0x30
ERROR_REGISTER_ACCESS_FAILED = 0x31

ERROR_LIBUPLINK_SO_NOT_FOUND = 0x9999
"""_Error defines"""


class StorjException(Exception):
    """Base class for other exceptions

    Attributes:
        code -- error code
        message -- error message
        details -- error message from uplink-c
    """

    def __init__(self, message, code, details):
        self.message = message
        self.code = code
        self.details = details
        super(StorjException, self).__init__()

    def __str__(self):
        return repr(self.message)


class InternalError(StorjException):
    """Exception raised if internal error occurred.

    Attributes:
        details -- error message from uplink-c
    """

    def __init__(self, details):
        super().__init__("internal error", ERROR_INTERNAL, details)


class CancelledError(StorjException):
    """Exception raised if operation cancelled.

    Attributes:
        details -- error message from uplink-c
    """

    def __init__(self, details):
        super().__init__("operation canceled", ERROR_CANCELED, details)


class InvalidHandleError(StorjException):
    """Exception raised if handle is invalid.

    Attributes:
        details -- error message from uplink-c
    """

    def __init__(self, details):
        super().__init__("invalid handle", ERROR_INVALID_HANDLE, details)


class TooManyRequestsError(StorjException):
    """Exception raised if too many requests performed.

    Attributes:
        details -- error message from uplink-c
    """

    def __init__(self, details):
        super().__init__("too many requests", ERROR_TOO_MANY_REQUESTS, details)


class BandwidthLimitExceededError(StorjException):
    """Exception raised if allowed bandwidth limit exceeded.

    Attributes:
        details -- error message from uplink-c
    """

    def __init__(self, details):
        super().__init__("bandwidth limit exceeded", ERROR_BANDWIDTH_LIMIT_EXCEEDED, details)


class StorageLimitExceededError(StorjException):
    """Exception raised if allowed storage limit exceeded.

    Attributes:
        details -- error message from uplink-c
    """

    def __init__(self, details):
        super().__init__("storage limit exceeded", ERROR_STORAGE_LIMIT_EXCEEDED, details)

class SegmentsLimitExceededError(StorjException):
    """Exception raised if allowed segments limit exceeded.

    Attributes:
        details -- error message from uplink-c
    """

    def __init__(self, details):
        super().__init__("segments limit exceeded", ERROR_SEGMENTS_LIMIT_EXCEEDED, details)


class PermissionDeniedError(StorjException):
    """Exception raised if permission denied.

    Attributes:
        details -- error message from uplink-c
    """

    def __init__(self, details):
        super().__init__("permission denied", ERROR_PERMISSION_DENIED, details)


class BucketNameInvalidError(StorjException):
    """Exception raised if bucket name is invalid.

    Attributes:
        details -- error message from uplink-c
    """

    def __init__(self, details):
        super().__init__("invalid bucket name", ERROR_BUCKET_NAME_INVALID, details)


class BucketAlreadyExistError(StorjException):
    """Exception raised if bucket already exist.

    Attributes:
        details -- error message from uplink-c
    """

    def __init__(self, details):
        super().__init__("bucket already exists", ERROR_BUCKET_ALREADY_EXISTS, details)


class BucketNotEmptyError(StorjException):
    """Exception raised if bucket is not empty.

    Attributes:
        details -- error message from uplink-c
    """

    def __init__(self, details):
        super().__init__("bucket is not empty", ERROR_BUCKET_NOT_EMPTY, details)


class BucketNotFoundError(StorjException):
    """Exception raised if bucket not found.

    Attributes:
        details -- error message from uplink-c
    """

    def __init__(self, details):
        super().__init__("bucket not found", ERROR_BUCKET_NOT_FOUND, details)


class ObjectKeyInvalidError(StorjException):
    """Exception raised if object key is invalid.

    Attributes:
        details -- error message from uplink-c
    """

    def __init__(self, details):
        super().__init__("invalid object key", ERROR_OBJECT_KEY_INVALID, details)


class ObjectNotFoundError(StorjException):
    """Exception raised if object not found.

    Attributes:
        details -- error message from uplink-c
    """

    def __init__(self, details):
        super().__init__("object not found", ERROR_OBJECT_NOT_FOUND, details)


class UploadDoneError(StorjException):
    """Exception raised if upload is complete.

    Attributes:
        details -- error message from uplink-c
    """

    def __init__(self, details):
        super().__init__("upload completed", ERROR_UPLOAD_DONE, details)


class AuthDialFailedError(StorjException):
    """Exception raised if failure to dial the Auth Service.

    Attributes:
        details -- error message from uplink-c
    """

    def __init__(self, details):
        super().__init__("Auth dial failed", ERROR_AUTH_DIAL_FAILED, details)

class RegisterAccessFailedError(StorjException):
    """Exception raised if failure to register access grant with Auth Service.

    Attributes:
        details -- error message from uplink-c
    """

    def __init__(self, details):
        super().__init__("register accees failed", ERROR_REGISTER_ACCESS_FAILED, details)


class LibUplinkSoError(StorjException):
    """Exception raised if reason is unknown.

    Attributes:
        code -- error code
        details -- error message from uplink-c
    """

    def __init__(self):
        super().__init__("libuplinkc.so not found", ERROR_LIBUPLINK_SO_NOT_FOUND,
                         "Please follow \"https://github.com/storj-thirdparty"
                         "/uplink-python#option-2\" "
                         "to build libuplinkc.so manually.")


def _storj_exception(code, details):
    switcher = {
        ERROR_INTERNAL: InternalError,
        ERROR_CANCELED: CancelledError,
        ERROR_INVALID_HANDLE: InvalidHandleError,
        ERROR_TOO_MANY_REQUESTS: TooManyRequestsError,
        ERROR_BANDWIDTH_LIMIT_EXCEEDED: BandwidthLimitExceededError,
        ERROR_STORAGE_LIMIT_EXCEEDED:StorageLimitExceededError,
        ERROR_SEGMENTS_LIMIT_EXCEEDED:SegmentsLimitExceededError,
        ERROR_PERMISSION_DENIED:PermissionDeniedError,
        ERROR_BUCKET_NAME_INVALID: BucketNameInvalidError,
        ERROR_BUCKET_ALREADY_EXISTS: BucketAlreadyExistError,
        ERROR_BUCKET_NOT_EMPTY: BucketNotEmptyError,
        ERROR_BUCKET_NOT_FOUND: BucketNotFoundError,
        ERROR_OBJECT_KEY_INVALID: ObjectKeyInvalidError,
        ERROR_OBJECT_NOT_FOUND: ObjectNotFoundError,
        ERROR_UPLOAD_DONE: UploadDoneError,
        ERROR_AUTH_DIAL_FAILED:AuthDialFailedError,
        ERROR_REGISTER_ACCESS_FAILED:RegisterAccessFailedError,
    }
    return switcher.get(code, StorjException)(details=details)
