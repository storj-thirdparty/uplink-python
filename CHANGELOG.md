# storj-python binding changelog

## [0.11] - 06-01-2020
### Changelog:
* Changess made according to latest libuplinkc v0.28.4
* Added get_file_size example function in helloStorj.py to check object size on storj to download.
* Added restrict_scope function.
* Added example for using scope key to access object on Storj in helloStorj.py


## [0.10] - 12-12-2019
### Changelog:
* Changess made according to latest libuplinkc v0.27.1
* Changed get_encryption_access return type from ctype pointer to string.
* Changed open_bucket parameters to take serializedEncryptionAccess as string instead of ctype pointer.
* Added functions related to access_scope.
* Added example for functions new_scope, parse_scope, etc in helloStorj.py


## [0.9] - 24-09-2019