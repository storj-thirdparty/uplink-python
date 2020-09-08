# pylint: disable=missing-docstring, protected-access
import unittest

from uplink_python.errors import StorjException, ERROR_INTERNAL
from uplink_python.module_classes import Permission, SharePrefix
from .helper import TestPy


class AccessTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_py = TestPy()
        cls.access = cls.test_py.get_access()

    def test1_access_parse(self):
        serialized_access = self.access.serialize()
        self.assertIsNotNone(serialized_access, "serialized_access failed")
        access = self.test_py.uplink.parse_access(serialized_access)
        self.assertIsNotNone(access, "parse_access failed")

    def test2_request_access(self):
        access = self.test_py.uplink.request_access_with_passphrase(self.test_py.satellite,
                                                                    self.test_py.api_key,
                                                                    self.test_py.encryption_phrase)
        self.assertIsNotNone(access, "parse_access failed")

    def test3_access_share_no_data(self):
        try:
            _ = self.access.share(None, None)
        except StorjException as error:
            self.assertEqual(error.code, ERROR_INTERNAL, error.details)

    def test4_access_share_no_prefix(self):
        # set permissions for the new access to be created
        permissions = Permission(allow_list=True, allow_delete=False)
        # create new access
        access = self.access.share(permissions, None)
        self.assertTrue(access.access.contents._handle != 0, "got empty access")

    def test5_access_share(self):
        # set permissions for the new access to be created
        permissions = Permission(allow_list=True, allow_delete=False)
        # set shared prefix as list of dictionaries for the new access to be created
        shared_prefix = [SharePrefix(bucket="alpha", prefix="")]
        # create new access
        access = self.access.share(permissions, shared_prefix)
        self.assertIsNotNone(access, "access_share failed")


if __name__ == '__main__':
    unittest.main()
