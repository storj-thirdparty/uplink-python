# pylint: disable=missing-docstring
import unittest

from uplink_python.errors import StorjException, ERROR_BUCKET_ALREADY_EXISTS, ERROR_BUCKET_NOT_FOUND
from .helper import TestPy


class BucketTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_py = TestPy()
        cls.access = cls.test_py.get_access()
        cls.project = cls.test_py.get_project()

    def test1_create_new_bucket(self):
        bucket = self.project.create_bucket("alpha")
        self.assertIsNotNone(bucket, "create_new_bucket failed")

    def test2_create_existing_bucket(self):
        try:
            _ = self.project.create_bucket("alpha")
        except StorjException as error:
            self.assertEqual(error.code, ERROR_BUCKET_ALREADY_EXISTS, error.details)

    def test3_ensure_new_bucket(self):
        bucket = self.project.ensure_bucket("beta")
        self.assertIsNotNone(bucket, "ensure_new_bucket failed")

    def test4_ensure_existing_bucket(self):
        bucket = self.project.ensure_bucket("alpha")
        self.assertIsNotNone(bucket, "ensure_existing_bucket failed")

    def test5_stat_existing_bucket(self):
        bucket = self.project.stat_bucket("alpha")
        self.assertIsNotNone(bucket, "stat_existing_bucket failed")

    def test6_stat_missing_bucket(self):
        try:
            _ = self.project.stat_bucket("missing")
        except StorjException as error:
            self.assertEqual(error.code, ERROR_BUCKET_NOT_FOUND, error.details)

    def test7_delete_existing_bucket(self):
        bucket = self.project.delete_bucket("alpha")
        self.assertIsNotNone(bucket, "delete_existing_bucket failed")

    def test8_delete_missing_bucket(self):
        try:
            _ = self.project.delete_bucket("missing")
        except StorjException as error:
            self.assertEqual(error.code, ERROR_BUCKET_NOT_FOUND, error.details)

    def test9_close_project(self):
        self.project.close()


if __name__ == '__main__':
    unittest.main()
