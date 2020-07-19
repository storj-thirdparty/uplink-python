# pylint: disable=missing-docstring, protected-access
import unittest

from uplink_python.constants import ERROR_INTERNAL
from uplink_python.uplink import Permission
from .helper import Uplink


class AccessTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.uplink = Uplink()
        cls.access = cls.uplink.get_access()

    def test1_access_parse(self):
        serialized_access_result, error = self.uplink.access_serialize(self.access)
        self.assertTrue(error is None, error)
        _, error = self.uplink.parse_access(serialized_access_result.string)
        self.assertTrue(error is None, error)

    def test2_request_access(self):
        _, error = self.uplink.request_access_with_passphrase(self.uplink.satellite,
                                                              self.uplink.api_key,
                                                              self.uplink.encryption_phrase)
        self.assertTrue(error is None, error)

    def test3_access_share_no_data(self):
        access_result, error = self.uplink.access_share(self.access, None, None)
        self.assertEqual(access_result.error.contents.code, ERROR_INTERNAL, error)

    def test4_access_share_no_prefix(self):
        # set permissions for the new access to be created
        permissions = Permission()
        permissions.allow_list = True
        permissions.allow_delete = False
        # create new access
        access_result, _ = self.uplink.access_share(self.access, permissions, None)
        self.assertTrue(access_result.access.contents._handle != 0, "got empty access")

    def test5_access_share(self):
        # set permissions for the new access to be created
        permissions = Permission()
        permissions.allow_list = True
        permissions.allow_delete = False
        # set shared prefix as list of dictionaries for the new access to be created
        shared_prefix = [{"bucket": "alpha", "prefix": ""}]
        # create new access
        _, error = self.uplink.access_share(self.access, permissions, shared_prefix)
        self.assertTrue(error is None, error)


if __name__ == '__main__':
    unittest.main()
