# pylint: disable=missing-docstring
import unittest

from .helper import Uplink


class ProjectTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.uplink = Uplink()
        cls.access = cls.uplink.get_access()

    def test1_open_project(self):
        _, error = self.uplink.open_project(self.access)
        self.assertTrue(error is None, error)


if __name__ == '__main__':
    unittest.main()
