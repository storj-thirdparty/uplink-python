# pylint: disable=missing-docstring
import unittest

from .helper import Uplink


class BucketListTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.uplink = Uplink()
        cls.access = cls.uplink.get_access()
        cls.project = cls.uplink.get_project()
        cls.bucket_names = ["alpha", "beta", "delta", "gamma", "iota", "kappa", "lambda"]

    def test1_ensure_buckets(self):
        # print("Bucket List: ", self.bucket_names)
        for bucket in self.bucket_names:
            _, error = self.uplink.ensure_bucket(self.project, bucket)
            self.assertTrue(error is None, error)

    def test2_list_buckets(self):
        # enlist all the buckets in given Storj project
        bucket_list, error = self.uplink.list_buckets(self.project, None)
        self.assertTrue(error is None, error)

        retrieved_bucket_names = list()
        for item in bucket_list:
            retrieved_bucket_names.append(item.contents.name.decode("utf-8"))
        # print("Retrieved Bucket List: ", retrieved_bucket_names)
        self.assertTrue(all(item in retrieved_bucket_names for item in self.bucket_names),
                        "Not all buckets found in bucket list")

    def test3_delete_buckets(self):
        for bucket in self.bucket_names:
            _, error = self.uplink.delete_bucket(self.project, bucket)
            self.assertTrue(error is None, error)

    def test4_close_project(self):
        error = self.uplink.close_project(self.project)
        self.assertTrue(error is None, error)


if __name__ == '__main__':
    unittest.main()
