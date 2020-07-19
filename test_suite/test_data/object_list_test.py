# pylint: disable=missing-docstring
import ctypes as c
import unittest

from uplink_python.uplink import ListObjectsOptions
from .helper import Uplink


class ObjectListTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.uplink = Uplink()
        cls.access = cls.uplink.get_access()
        cls.project = cls.uplink.get_project()
        cls.object_names = ["alpha/one", "beta", "delta", "gamma", "iota", "kappa",
                            "lambda", "alpha/two"]

    def test1_ensure_bucket(self):
        _, error = self.uplink.ensure_bucket(self.project, "py-unit-test")
        self.assertTrue(error is None, error)

    def test2_upload_objects(self):
        # print("Object List: ", self.object_names)

        for name in self.object_names:
            data_bytes = bytes("hello", 'utf-8')
            upload_result, error = self.uplink.upload_object(self.project, "py-unit-test", name,
                                                             None)
            self.assertTrue(error is None, error)

            data_to_write = (c.c_uint8 * c.c_int32(len(data_bytes)).value)(*data_bytes)
            # conversion of c type ubyte Array to LP_c_ubyte required by upload write function
            data_to_write_ptr = c.cast(data_to_write, c.POINTER(c.c_uint8))
            # --------------------------------------------]
            # call to write data to Storj bucket
            _, error = self.uplink.upload_write(upload_result.upload, data_to_write_ptr,
                                                len(data_bytes))
            self.assertTrue(error is None, error)

            error = self.uplink.upload_commit(upload_result.upload)
            self.assertTrue(error is None, error)

    def test3_list_objects(self):
        # enlist all the objects in given bucket
        object_list, error = self.uplink.list_objects(self.project, "py-unit-test", None)
        self.assertTrue(error is None, error)

        expected_names = ["alpha/", "beta", "delta", "gamma", "iota", "kappa", "lambda"]
        # print("Expected Object List: ", expected_names)

        retrieved_object_names = list()
        for item in object_list:
            retrieved_object_names.append(item.contents.key.decode('utf-8'))
        # print("Retrieved Object List: ", retrieved_object_names)
        self.assertTrue(all(item in retrieved_object_names for item in expected_names),
                        "Not all objects found in object list")

    def test4_list_objects_with_prefix(self):
        # set list options before calling list objects (optional)
        list_option = ListObjectsOptions()
        list_option.prefix = c.c_char_p(bytes("alpha/", 'utf-8'))

        # enlist all the objects in given bucket
        object_list, error = self.uplink.list_objects(self.project, "py-unit-test", list_option)
        self.assertTrue(error is None, error)

        expected_names = ["alpha/one", "alpha/two"]
        # print("Expected Object List: ", expected_names)

        retrieved_object_names = list()
        for item in object_list:
            retrieved_object_names.append(item.contents.key.decode('utf-8'))
        # print("Retrieved Object List: ", retrieved_object_names)
        self.assertTrue(all(item in retrieved_object_names for item in expected_names),
                        "Not all objects found in object list")

    def test5_delete_objects(self):
        for name in self.object_names:
            _, error = self.uplink.delete_object(self.project, "py-unit-test", name)
            self.assertTrue(error is None, error)

    def test6_delete_bucket(self):
        _, error = self.uplink.delete_bucket(self.project, "py-unit-test")
        self.assertTrue(error is None, error)

    def test7_close_project(self):
        error = self.uplink.close_project(self.project)
        self.assertTrue(error is None, error)


if __name__ == '__main__':
    unittest.main()
