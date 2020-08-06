# pylint: disable=missing-docstring
import unittest

from uplink_python.uplink import Uplink


class TestPy:
    """
    Python Storj class objects with all Storj functions' bindings
    """

    def __init__(self):
        super().__init__()
        # method to get satellite, api key and passphrase
        self.satellite = "us-central-1.tardigrade.io:7777"
        # self.api_key = open("secret.txt", 'r').read()
        self.encryption_phrase = "test"
        self.api_key = "13Yqdeo8kkCBBtkCvy8YTXi839RkgFk9qtxgo7hymbbtcNEDrG42K" \
                       "ygaunHYXfMRB1SyaXrXyA9u5ra6yLUndycqT34oDj3fdQiQs4d"

        self.uplink = Uplink()
        self.access = None
        self.project = None

    def get_access(self):
        self.access = self.uplink.request_access_with_passphrase(self.satellite,
                                                                 self.api_key,
                                                                 self.encryption_phrase)
        return self.access

    def get_project(self):
        self.project = self.access.open_project()
        return self.project


class InitializationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_py = TestPy()

    def test1_initialize_uplink(self):
        self.assertIsNotNone(self.test_py, "TestPy initialization failed.")

    # def test2_get_credentials(self):
    #     file_handle = open("secret.txt", 'r')
    #     self.assertIsNotNone(file_handle, "Credentials retrieval failed.")


if __name__ == '__main__':
    unittest.main()
