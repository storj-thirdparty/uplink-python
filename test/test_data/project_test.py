# pylint: disable=missing-docstring
import unittest
from uplink_python.errors import BucketAlreadyExistError, PermissionDeniedError
from uplink_python.module_classes import Permission, SharePrefix

from .helper import TestPy


class ProjectTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_py = TestPy()
        cls.access = cls.test_py.get_access()

    def test1_open_project(self):
        project = self.access.open_project()
        self.assertIsNotNone(project, "open_project failed")


    def test2_revoke_access(self):
        # sanity check current credentials
        project = self.access.open_project()
        self.assertIsNotNone(project, "open_project failed")
        try:
            _ = project.create_bucket("alpha")
        except BucketAlreadyExistError:
           pass
        test_access_availability(project)

        # create derived credentials to be revoked
        permissions = Permission(allow_list=True, allow_download=True, allow_upload=True, allow_delete=True)
        shared_prefix = [SharePrefix(bucket="alpha", prefix="")]
        access = self.access.share(permissions, shared_prefix)
        self.assertTrue(access.access.contents._handle != 0, "got empty access")
        self.assertIsNotNone(access, "access_share failed")

        # sanity check derived credentials
        project2 = access.open_project()
        self.assertIsNotNone(project2, "open_project2 failed")
        test_access_availability(project2)

        # revoke derived credentials
        project.revoke_access(access)

        #expect derived credentials to fail
        with self.assertRaises(PermissionDeniedError) as context:
            test_access_availability(project2)

def test_access_availability(project):
        data_bytes = bytes("!" * 1024  , 'utf-8')
        upload = project.upload_object("alpha", "test_object")
        _ = upload.write(data_bytes, len(data_bytes))
        upload.commit()

if __name__ == '__main__':
    unittest.main()
