# pylint: disable=missing-docstring
import unittest

from uplink_python.uplink import LibUplinkPy


class Uplink(LibUplinkPy):
    """ Python Storj class objects with all Storj functions' bindings """

    def __init__(self):
        super().__init__()
        # method to get satellite, api key and passphrase
        file_handle = open("secret.txt", 'r')

        self.satellite = "us-central-1.tardigrade.io:7777"
        self.api_key = file_handle.read()
        self.encryption_phrase = "test"

        file_handle.close()

        self.access_result = None
        self.project_result = None

    def get_access(self):
        self.access_result, access_error = \
            self.request_access_with_passphrase(self.satellite,
                                                self.api_key,
                                                self.encryption_phrase)
        if access_error is None:
            return self.access_result.access
        return None

    def get_project(self):
        self.project_result, project_error = self.open_project(self.access_result.access)
        if project_error is None:
            return self.project_result.project
        return None


class InitializationTest(unittest.TestCase):

    def test1_initialize_uplink(self):
        uplink = Uplink()
        self.assertIsNotNone(uplink, "LibUplinkPy initialization failed.")


if __name__ == '__main__':
    unittest.main()
