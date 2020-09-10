# pylint: disable=missing-docstring
import unittest

from uplink_python.module_classes import ListObjectsOptions
from .helper import TestPy


class ObjectListTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_py = TestPy()
        cls.access = cls.test_py.get_access()
        cls.project = cls.test_py.get_project()
        cls.object_names = ["alpha/one", "beta", "delta", "gamma", "iota", "kappa",
                            "lambda", "alpha/two"]

    def test1_ensure_bucket(self):
        bucket = self.project.ensure_bucket("py-unit-test")
        self.assertIsNotNone(bucket, "ensure_bucket failed")

    def test2_upload_objects(self):
        for name in self.object_names:
            data_bytes = bytes("hello", 'utf-8')
            #
            upload = self.project.upload_object("py-unit-test", name)
            self.assertIsNotNone(upload, "upload_object failed")
            #
            _ = upload.write(data_bytes, len(data_bytes))
            #
            upload.commit()

    def test3_list_objects(self):
        # enlist all the objects in given bucket
        object_list = self.project.list_objects("py-unit-test")
        self.assertIsNotNone(object_list, "list_objects failed")

        expected_names = ["alpha/", "beta", "delta", "gamma", "iota", "kappa", "lambda"]

        retrieved_object_names = list()
        for item in object_list:
            retrieved_object_names.append(item.key)
        #
        self.assertTrue(all(item in retrieved_object_names for item in expected_names),
                        "Not all objects found in object list")

    def test4_list_objects_with_prefix(self):
        # set list options before calling list objects (optional)
        list_option = ListObjectsOptions(prefix="alpha/")

        # enlist all the objects in given bucket
        object_list = self.project.list_objects("py-unit-test", list_option)
        self.assertIsNotNone(object_list, "list_objects failed")

        expected_names = ["alpha/one", "alpha/two"]

        retrieved_object_names = list()
        for item in object_list:
            retrieved_object_names.append(item.key)
        #
        self.assertTrue(all(item in retrieved_object_names for item in expected_names),
                        "Not all objects found in object list")

    def test5_delete_objects(self):
        for name in self.object_names:
            object_ = self.project.delete_object("py-unit-test", name)
            self.assertIsNotNone(object_, "delete_object failed")

    def test6_delete_bucket(self):
        bucket = self.project.delete_bucket("py-unit-test")
        self.assertIsNotNone(bucket, "delete_bucket failed")

    def test7_close_project(self):
        self.project.close()


if __name__ == '__main__':
    unittest.main()
