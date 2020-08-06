# pylint: disable=missing-docstring
import unittest

from .helper import TestPy


class ProjectTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_py = TestPy()
        cls.access = cls.test_py.get_access()

    def test1_open_project(self):
        project = self.access.open_project()
        self.assertIsNotNone(project, "open_project failed")


if __name__ == '__main__':
    unittest.main()
