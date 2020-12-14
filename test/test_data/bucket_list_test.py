# pylint: disable=missing-docstring
import unittest

from .helper import TestPy


class BucketListTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_py = TestPy()
        cls.access = cls.test_py.get_access()
        cls.project = cls.test_py.get_project()
        cls.bucket_names = ["alpha", "delta", "gamma", "iota", "kappa", "lambda"]

    def test1_ensure_buckets(self):
        # print("Bucket List: ", self.bucket_names)
        for name in self.bucket_names:
            bucket = self.project.ensure_bucket(name)
            self.assertIsNotNone(bucket, "ensure_buckets failed")

    def test2_list_buckets(self):
        # enlist all the buckets in given Storj project
        bucket_list = self.project.list_buckets()
        self.assertIsNotNone(bucket_list, "list_buckets failed")

        retrieved_bucket_names = list()
        for item in bucket_list:
            retrieved_bucket_names.append(item.name)
        # print("Retrieved Bucket List: ", retrieved_bucket_names)
        self.assertTrue(all(item in retrieved_bucket_names for item in self.bucket_names),
                        "Not all buckets found in bucket list")

    def test3_delete_buckets(self):
        for name in self.bucket_names:
            object_list = self.project.list_objects(name)
            if object_list is not None:
                for item in object_list:
                    self.project.delete_object(name, item.key)
            bucket = self.project.delete_bucket(name)
            self.assertIsNotNone(bucket, "delete_bucket failed")

    def test4_close_project(self):
        self.project.close()


if __name__ == '__main__':
    unittest.main()
