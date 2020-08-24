# uplink-python binding changelog

## [1.0.6] - 25-08-2020
### Changelog:
* Pinned to specific version of uplinkc - v1.0.5

## [1.0.4] - 06-08-2020
### Changelog:
* Changed overall structure of uplink-python.
* Added error classes for error handling.
* Added instruction to run unit test on local in Readme.
* Changed documentation.

## [1.0.3] - 19-07-2020
### Changelog:
* Update module to latest storj/uplink-c v1.0.5
* Added unittest
* Changed documentation
* import statements changed

## [1.0.2] - 02-06-2020
### Changelog:
* Migrated package on pip (pypi) from storj-python to uplink-python
* Linting done using pylint
* Changed file names according to snake_case python rule.
* Splitted LibUplinkPy class into two parts and two files: uplink and exchange.


## [1.0.1] - 06-05-2020
### Changelog:
* Migrated package on pip (pypi) from storjPython to storj-python
* Building libuplinkc.so is now handled by pip install.


## [1.0.1] - 19-04-2020
### Changelog:
* Changes made according to latest storj/uplink-c RC v1.0.1


## [0.12.0] - 30-01-2020
### Changelog:
* Changes made according to latest libuplinkc v0.31.6
* Added support for MacOS.


## [0.11.0] - 06-01-2020
### Changelog:
* Changes made according to latest libuplinkc v0.28.4
* Added get_file_size example function in helloStorj.py to check object size on storj to download.
* Added restrict_scope function.
* Added example for using scope key to access object on Storj in helloStorj.py


## [0.10.0] - 12-12-2019
### Changelog:
* Changes made according to latest libuplinkc v0.27.1
* Changed get_encryption_access return type from ctype pointer to string.
* Changed open_bucket parameters to take serializedEncryptionAccess as string instead of ctype pointer.
* Added functions related to access_scope.
* Added example for functions new_scope, parse_scope, etc in helloStorj.py


## [0.9.0] - 24-09-2019
