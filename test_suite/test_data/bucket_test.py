# pylint: disable=missing-docstring
import unittest

from uplink_python.constants import ERROR_BUCKET_ALREADY_EXISTS, ERROR_BUCKET_NOT_FOUND
from .helper import Uplink


class BucketTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.uplink = Uplink()
        cls.access = cls.uplink.get_access()
        cls.project = cls.uplink.get_project()

    def test1_create_new_bucket(self):
        _, error = self.uplink.create_bucket(self.project, "alpha")
        self.assertTrue(error is None, error)

    def test2_create_existing_bucket(self):
        bucket_result, error = self.uplink.create_bucket(self.project, "alpha")
        self.assertEqual(bucket_result.error.contents.code, ERROR_BUCKET_ALREADY_EXISTS, error)

    def test3_ensure_new_bucket(self):
        _, error = self.uplink.ensure_bucket(self.project, "beta")
        self.assertTrue(error is None, error)

    def test4_ensure_existing_bucket(self):
        _, error = self.uplink.ensure_bucket(self.project, "alpha")
        self.assertTrue(error is None, error)

    def test5_stat_existing_bucket(self):
        _, error = self.uplink.stat_bucket(self.project, "alpha")
        self.assertTrue(error is None, error)

    def test6_stat_missing_bucket(self):
        bucket_result, error = self.uplink.stat_bucket(self.project, "missing")
        self.assertEqual(bucket_result.error.contents.code, ERROR_BUCKET_NOT_FOUND, error)

    def test7_delete_existing_bucket(self):
        _, error = self.uplink.delete_bucket(self.project, "alpha")
        self.assertTrue(error is None, error)

    def test8_delete_missing_bucket(self):
        bucket_result, error = self.uplink.delete_bucket(self.project, "missing")
        self.assertEqual(bucket_result.error.contents.code, ERROR_BUCKET_NOT_FOUND, error)

    def test9_close_project(self):
        error = self.uplink.close_project(self.project)
        self.assertTrue(error is None, error)


if __name__ == '__main__':
    unittest.main()
