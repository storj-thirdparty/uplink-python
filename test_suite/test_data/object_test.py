# pylint: disable=missing-docstring
import ctypes as c
import random
import string
import unittest

from uplink_python.constants import ERROR_OBJECT_NOT_FOUND
from .helper import Uplink


class ObjectTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.uplink = Uplink()
        cls.access = cls.uplink.get_access()
        cls.project = cls.uplink.get_project()
        cls.data_len = 5 * 1024

    def test1_ensure_bucket(self):
        _, error = self.uplink.ensure_bucket(self.project, "alpha")
        self.assertTrue(error is None, error)

    def test2_basic_upload(self):

        data = ''.join(random.choices(string.ascii_uppercase +
                                      string.digits, k=self.data_len))
        data_bytes = bytes(data, 'utf-8')
        # print("Data to upload: ", data_bytes)
        #
        # call to get uploader handle
        upload_result, error = self.uplink.upload_object(self.project, "alpha", "data.txt",
                                                         None)
        self.assertTrue(error is None, error)

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
            # --------------------------------------------
            # data conversion to type required by function
            # get size of data in c type int32 variable
            # conversion of read bytes data to c type ubyte Array
            data_to_write = (c.c_uint8 * c.c_int32(len(data_to_write)).value)(*data_to_write)
            # conversion of c type ubyte Array to LP_c_ubyte required by upload write function
            data_to_write_ptr = c.cast(data_to_write, c.POINTER(c.c_uint8))
            # --------------------------------------------
            #
            # call to write data to Storj bucket
            write_result, error = self.uplink.upload_write(upload_result.upload, data_to_write_ptr,
                                                           size_to_write)
            self.assertTrue(error is None, error)
            #
            # exit while loop if nothing left to upload / unable to upload
            if int(write_result.bytes_written) == 0:
                break
            # update last read location
            uploaded_total += int(write_result.bytes_written)

        _, error = self.uplink.upload_info(upload_result.upload)
        self.assertTrue(error is None, error)

        # commit upload data to bucket
        error = self.uplink.upload_commit(upload_result.upload)
        self.assertTrue(error is None, error)

    def test3_basic_download(self):
        data_bytes = bytes()
        download_result, error = self.uplink.download_object(self.project, "alpha", "data.txt",
                                                             None)
        self.assertTrue(error is None, error)
        #
        # get size of file to be downloaded from storj
        file_size = self.data_len
        #
        # set packet size to be used while downloading
        size_to_read = 256
        # initialize local variables and start downloading packets of data
        downloaded_total = 0
        while True:
            # call to read data from Storj bucket
            data_read_ptr, read_result, error = self.uplink.download_read(download_result.download,
                                                                          size_to_read)
            self.assertTrue(error is None, error)
            #
            # file writing process from the last written position if new data is downloaded
            if int(read_result.bytes_read) != 0:
                #
                # --------------------------------------------
                # data conversion to type python readable form
                # conversion of LP_c_ubyte to python readable data variable
                data_read = c.string_at(data_read_ptr, int(read_result.bytes_read))
                # --------------------------------------------
                #
                data_bytes = data_bytes + data_read
            #
            # update last read location
            downloaded_total += int(read_result.bytes_read)
            #
            # break if download complete
            if downloaded_total == file_size:
                # print("Data downloaded: ", data_bytes)
                break

        _, error = self.uplink.download_info(download_result.download)
        self.assertTrue(error is None, error)
        #
        # close downloader and free downloader access
        error = self.uplink.close_download(download_result.download)
        self.assertTrue(error is None, error)

    def test4_stat_object(self):
        _, error = self.uplink.stat_object(self.project, "alpha", "data.txt")
        self.assertTrue(error is None, error)

    def test5_delete_existing_object(self):
        _, error = self.uplink.delete_object(self.project, "alpha", "data.txt")
        self.assertTrue(error is None, error)

    def test6_delete_missing_object(self):
        object_result, error = self.uplink.delete_object(self.project, "alpha", "data.txt")
        self.assertEqual(object_result.error.contents.code, ERROR_OBJECT_NOT_FOUND, error)

    def test7_delete_bucket(self):
        _, error = self.uplink.delete_bucket(self.project, "alpha")
        self.assertTrue(error is None, error)

    def test8_close_project(self):
        error = self.uplink.close_project(self.project)
        self.assertTrue(error is None, error)


if __name__ == '__main__':
    unittest.main()
