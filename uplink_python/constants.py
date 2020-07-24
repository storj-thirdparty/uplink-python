""" Python Binding's Constants Module for Storj (V3) """

ERROR_INTERNAL = 0x02
ERROR_CANCELED = 0x03
ERROR_INVALID_HANDLE = 0x04
ERROR_TOO_MANY_REQUESTS = 0x05
ERROR_BANDWIDTH_LIMIT_EXCEEDED = 0x06

ERROR_BUCKET_NAME_INVALID = 0x10
ERROR_BUCKET_ALREADY_EXISTS = 0x11
ERROR_BUCKET_NOT_EMPTY = 0x12
ERROR_BUCKET_NOT_FOUND = 0x13

ERROR_OBJECT_KEY_INVALID = 0x20
ERROR_OBJECT_NOT_FOUND = 0x21
ERROR_UPLOAD_DONE = 0x22
"""Error defines"""

""" Error messages associated to Storj (v3) libuplink-c error constants """

ERROR_MESSAGES = {
    ERROR_INTERNAL: "internal error",
    ERROR_CANCELED: "operation canceled",
    ERROR_INVALID_HANDLE: "invalid handle",
    ERROR_TOO_MANY_REQUESTS: "too many requests",
    ERROR_BANDWIDTH_LIMIT_EXCEEDED: "bandwidth limit exceeded",

    ERROR_BUCKET_NAME_INVALID: "invalid bucket name",
    ERROR_BUCKET_ALREADY_EXISTS: "bucket already exists",
    ERROR_BUCKET_NOT_EMPTY: "bucket is not empty",
    ERROR_BUCKET_NOT_FOUND: "bucket not found",

    ERROR_OBJECT_KEY_INVALID: "invalid object key",
    ERROR_OBJECT_NOT_FOUND: "object not found",
    ERROR_UPLOAD_DONE: "upload completed",
}
"""Error messages"""
