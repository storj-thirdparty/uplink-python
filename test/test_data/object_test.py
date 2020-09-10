# pylint: disable=missing-docstring
import random
import string
import unittest

from uplink_python.errors import StorjException, ERROR_OBJECT_NOT_FOUND
from .helper import TestPy


class ObjectTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_py = TestPy()
        cls.access = cls.test_py.get_access()
        cls.project = cls.test_py.get_project()
        cls.data_len = 5 * 1024

    def test1_ensure_bucket(self):
        bucket = self.project.ensure_bucket("alpha")
        self.assertIsNotNone(bucket, "ensure_bucket failed")

    def test2_basic_upload(self):

        data = ''.join(random.choices(string.ascii_uppercase +
                                      string.digits, k=self.data_len))
        data_bytes = bytes(data, 'utf-8')
        #
        # call to get uploader handle
        upload = self.project.upload_object("alpha", "data.txt")
        self.assertIsNotNone(upload, "upload_object failed")

        # initialize local variables and start uploading packets of data
        uploaded_total = 0
        while uploaded_total < self.data_len:
            # set packet size to be used while uploading
            size_to_write = 256 if (self.data_len - uploaded_total > 256)\
                else self.data_len - uploaded_total
            #
            # exit while loop if nothing left to upload
            if size_to_write == 0:
                break
            #
            # data bytes reading process from the last read position
            data_to_write = data_bytes[uploaded_total:uploaded_total + size_to_write]
            #
            # call to write data to Storj bucket
            bytes_written = upload.write(data_to_write, size_to_write)
            # self.assertTrue(error is None, error)
            #
            # exit while loop if nothing left to upload / unable to upload
            if bytes_written == 0:
                break
            # update last read location
            uploaded_total += bytes_written

        object_ = upload.info()
        self.assertIsNotNone(object_, "upload_info failed")

        # commit upload data to bucket
        upload.commit()

    def test3_basic_download(self):
        data_bytes = bytes()
        download = self.project.download_object("alpha", "data.txt")
        self.assertIsNotNone(download, "download_object failed")
        #
        # get size of file to be downloaded from storj
        file_size = download.file_size()
        #
        # set packet size to be used while downloading
        size_to_read = 256
        # initialize local variables and start downloading packets of data
        downloaded_total = 0
        while True:
            # call to read data from Storj bucket
            data_read, bytes_read = download.read(size_to_read)
            #
            # file writing process from the last written position if new data is downloaded
            if bytes_read != 0:
                data_bytes = data_bytes + data_read
            #
            # update last read location
            downloaded_total += bytes_read
            #
            # break if download complete
            if downloaded_total == file_size:
                break

        object_ = download.info()
        self.assertIsNotNone(object_, "download_info failed")
        #
        # close downloader and free downloader access
        download.close()

    def test4_stat_object(self):
        object_ = self.project.stat_object("alpha", "data.txt")
        self.assertIsNotNone(object_, "stat_object failed")

    def test5_delete_existing_object(self):
        object_ = self.project.delete_object("alpha", "data.txt")
        self.assertIsNotNone(object_, "delete_object failed")

    def test6_delete_bucket(self):
        bucket = self.project.delete_bucket("alpha")
        self.assertIsNotNone(bucket, "delete_bucket failed")

    def test7_close_project(self):
        self.project.close()


if __name__ == '__main__':
    unittest.main()
