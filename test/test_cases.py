# pylint: disable=missing-docstring
import unittest

from .test_data.access_test import AccessTest
from .test_data.bucket_list_test import BucketListTest
from .test_data.bucket_test import BucketTest
from .test_data.helper import InitializationTest
from .test_data.object_list_test import ObjectListTest
from .test_data.object_test import ObjectTest
from .test_data.project_test import ProjectTest

if __name__ == '__main__':
    testList = [InitializationTest, AccessTest, ProjectTest, BucketTest, BucketListTest,
                ObjectTest, ObjectListTest]
    testLoad = unittest.TestLoader()

    TestList = []
    for testCase in testList:
        testSuite = testLoad.loadTestsFromTestCase(testCase)
        TestList.append(testSuite)

    newSuite = unittest.TestSuite(TestList)
    runner = unittest.TextTestRunner(verbosity=4)
    runner.run(newSuite)
