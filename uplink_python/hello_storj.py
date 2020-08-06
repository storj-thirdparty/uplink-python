# pylint: disable=too-many-arguments
""" example project for storj-python binding shows how to use binding for various tasks. """

from datetime import datetime

from .errors import StorjException, BucketNotEmptyError, BucketNotFoundError
from .module_classes import ListObjectsOptions, Permission, SharePrefix
from .uplink import Uplink

if __name__ == "__main__":

    # Storj configuration information
    MY_API_KEY = "change-me-to-the-api-key-created-in-satellite-gui"
    MY_SATELLITE = "us-central-1.tardigrade.io:7777"
    MY_BUCKET = "my-first-bucket"
    MY_STORJ_UPLOAD_PATH = "(optional): path / (required): filename"
    # (path + filename) OR filename
    MY_ENCRYPTION_PASSPHRASE = "you'll never guess this"

    # Source and destination path and file name for testing
    SRC_FULL_FILENAME = "filename with extension of source file on local system"
    DESTINATION_FULL_FILENAME = "filename with extension to save on local system"

    # try-except block to catch any storj exception
    try:
        # create an object of Uplink class
        uplink = Uplink()

        # function calls
        # request access using passphrase
        print("\nRequesting Access using passphrase...")
        access = uplink.request_access_with_passphrase(MY_SATELLITE, MY_API_KEY,
                                                       MY_ENCRYPTION_PASSPHRASE)
        print("Request Access: SUCCESS!")
        #

        # open Storj project
        print("\nOpening the Storj project, corresponding to the parsed Access...")
        project = access.open_project()
        print("Desired Storj project: OPENED!")
        #

        # enlist all the buckets in given Storj project
        print("\nListing bucket's names and creation time...")
        bucket_list = project.list_buckets()
        for bucket in bucket_list:
            # as python class object
            print(bucket.name, " | ", datetime.fromtimestamp(bucket.created))
            # as python dictionary
            print(bucket.get_dict())
        print("Buckets listing: COMPLETE!")
        #

        # delete given bucket
        print("\nDeleting '" + MY_BUCKET + "' bucket...")
        try:
            bucket = project.delete_bucket(MY_BUCKET)
        # if delete bucket fails due to "not empty", delete all the objects and try again
        except BucketNotEmptyError as exception:
            print("Error while deleting bucket: ", exception.message)
            print("Deleting object's inside bucket and try to delete bucket again...")
            # list objects in given bucket recursively using ListObjectsOptions
            print("Listing and deleting object's inside bucket...")
            objects_list = project.list_objects(MY_BUCKET, ListObjectsOptions(recursive=True))
            # iterate through all objects path
            for obj in objects_list:
                # delete selected object
                print("Deleting '" + obj.key)
                _ = project.delete_object(MY_BUCKET, obj.key)
            print("Delete all objects inside the bucket : COMPLETE!")

            # try to delete given bucket
            print("Deleting '" + MY_BUCKET + "' bucket...")
            _ = project.delete_bucket(MY_BUCKET)
            print("Desired bucket: DELETED")
        except BucketNotFoundError as exception:
            print("Desired bucket delete error: ", exception.message)
        #

        # create bucket in given project
        print("\nCreating '" + MY_BUCKET + "' bucket...")
        _ = project.create_bucket(MY_BUCKET)
        print("Desired Bucket: CREATED!")

        # as an example of 'put' , lets read and upload a local file
        # upload file/object
        print("\nUploading data...")
        # get handle of file to be uploaded
        file_handle = open(SRC_FULL_FILENAME, 'r+b')
        # get upload handle to specified bucket and upload file path
        upload = project.upload_object(MY_BUCKET, MY_STORJ_UPLOAD_PATH)
        #
        # upload file on storj
        upload.write_file(file_handle)
        #
        # commit the upload
        upload.commit()
        # close file handle
        file_handle.close()
        print("Upload: COMPLETE!")
        #

        # list objects in given bucket with above options or None
        print("\nListing object's names...")
        objects_list = project.list_objects(MY_BUCKET, ListObjectsOptions(recursive=True,
                                                                          system=True))
        # print all objects path
        for obj in objects_list:
            print(obj.key, " | ", obj.is_prefix)  # as python class object
            print(obj.get_dict())  # as python dictionary
        print("Objects listing: COMPLETE!")
        #

        # as an example of 'get' , lets download an object and write it to a local file
        # download file/object
        print("\nDownloading data...")
        # get handle of file which data has to be downloaded
        file_handle = open(DESTINATION_FULL_FILENAME, 'w+b')
        # get download handle to specified bucket and object path to be downloaded
        download = project.download_object(MY_BUCKET, MY_STORJ_UPLOAD_PATH)
        #
        # download data from storj to file
        download.read_file(file_handle)
        #
        # close the download stream
        download.close()
        # close file handle
        file_handle.close()
        print("Download: COMPLETE!")
        #

        # as an example of how to create shareable Access for easy storj access without
        # API key and Encryption PassPhrase
        # create new Access with permissions
        print("\nCreating new Access...")
        # set permissions for the new access to be created
        permissions = Permission(allow_list=True, allow_delete=False)
        # set shared prefix as list of dictionaries for the new access to be created
        shared_prefix = [SharePrefix(bucket=MY_BUCKET, prefix="")]
        # create new access
        new_access = access.share(permissions, shared_prefix)
        print("New Access: CREATED!")
        #

        # generate serialized access to share
        print("\nGenerating serialized Access...")
        serialized_access = access.serialize()
        print("Serialized shareable Access: ", serialized_access)
        #

        #
        # close given project using handle
        print("\nClosing Storj project...")
        project.close()
        print("Project CLOSED!")
        #

        #
        # as an example of how to retrieve information from shareable Access for storj access
        # retrieving Access from serialized Access
        print("\nParsing serialized Access...")
        shared_access = uplink.parse_access(serialized_access)
        print("Parsing Access: COMPLETE")
        #

        # open Storj project
        print("\nOpening the Storj project, corresponding to the shared Access...")
        shared_project = shared_access.open_project()
        print("Desired Storj project: OPENED!")
        #

        # enlist all the buckets in given Storj project
        print("\nListing bucket's names and creation time...")
        bucket_list = shared_project.list_buckets()
        for bucket in bucket_list:
            # as python class object
            print(bucket.name, " | ", datetime.fromtimestamp(bucket.created))
            # as python dictionary
            print(bucket.get_dict())
        print("Buckets listing: COMPLETE!")
        #

        # list objects in given bucket with above options or None
        print("\nListing object's names...")
        objects_list = shared_project.list_objects(MY_BUCKET, ListObjectsOptions(recursive=True,
                                                                                 system=True))
        # print all objects path
        for obj in objects_list:
            print(obj.key, " | ", obj.is_prefix)  # as python class object
            print(obj.get_dict())  # as python dictionary
        print("Objects listing: COMPLETE!")
        #

        # try to delete given bucket
        print("\nTrying to delete '" + MY_STORJ_UPLOAD_PATH)
        try:
            _ = shared_project.delete_object(MY_BUCKET, MY_STORJ_UPLOAD_PATH)
            print("Desired object: DELETED")
        except StorjException as exception:
            print("Desired object: FAILED")
            print("Exception: ", exception.details)
        #

        #
        # close given project with shared Access
        print("\nClosing Storj project...")
        shared_project.close()
        print("Project CLOSED!")
        #
    except StorjException as exception:
        print("Exception Caught: ", exception.details)
