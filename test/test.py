import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bugbug import BugBug
import unittest

CHROME_DRIVER_PATH = os.environ["CHROME_DRIVER_PATH"]


class TestBugBug(unittest.TestCase):

    # The setup that runs before the tests are run: set up the Selenium webdriver
    def setUp(self):
        service = Service(executable_path=CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service)
        self.bug = BugBug(driver)
        self.bug.sign_in_to_bugbug()
        self.bug.add_new_project("Example New Project")


    def test_login_and_create_project(self):
        self.assertEqual("Example New Project", self.bug.list_newest_project())


    # Test for tests management: creation and list
    # Check how many tests there are when a new project is just created by listing them. There should be none.
    # Next, add 2 tests, then check if those tests are successfully added with correct corresponding title and
    # screen size setting.
    def test_insert_test(self):
        self.assertEqual(len(self.bug.list_test()), 0)

        self.bug.add_new_test("test1", "Mobile")
        self.bug.add_new_test("test2", "Desktop")

        updated_tests = self.bug.list_test()
        expected_test = {"test1": "Mobile", "test2": "Desktop"}
        self.assertEqual(updated_tests, expected_test)

    # Test for tests management: deletion and list
    # Add 3 tests to the project and make sure there are no other tests in the project. Now, delete a test
    # with test title "test1", then list out the tests to make sure that test is indeed gone.
    def test_delete_test(self):
        self.assertEqual(len(self.bug.list_test()), 0)
        self.bug.add_new_test("test1", "Mobile")
        self.bug.add_new_test("test2", "Desktop")
        self.bug.add_new_test("test3", "Mobile")
        updated_tests = self.bug.list_test()
        self.assertEqual(3, len(updated_tests))

        self.bug.delete_test("test1")
        updated_tests = self.bug.list_test()
        expected_test = {"test2": "Desktop", "test3": "Mobile"}
        self.assertEqual(expected_test, updated_tests)

    # Test for tests management: update and list
    # Add 3 tests to the project and make sure those are the only tests for that project. Now, update 2 of the test's
    # title and screen size setting, then list out all the test's details to check if they have been correctly modified.
    def test_update_test(self):
        self.assertEqual(len(self.bug.list_test()), 0)
        self.bug.add_new_test("test1", "Mobile")
        self.bug.add_new_test("test2", "Desktop")
        self.bug.add_new_test("test3", "Mobile")
        updated_tests = self.bug.list_test()
        self.assertEqual(3, len(updated_tests))

        self.bug.update_test("test1", "test1 New Title", "Desktop")
        self.bug.update_test("test2", "test2 New Title", "Mobile")
        updated_tests = self.bug.list_test()
        expected_test = {"test1 New Title": "Desktop", "test2 New Title": "Mobile", "test3": "Mobile"}
        self.assertEqual(expected_test, updated_tests)

    # Test for suite management: creation and list
    # Ensure there are only the initial suite in the project, then add 2 tests. Next, add a suite with
    # a suite name, "Auto add new tests" setting (True = Enabled, False = Disabled), "Auto-retry failed cloud tests"
    # setting (the number indicate the number of times, 0 means Disabled), and a list of tests that will be selected
    # for the test suite. After, list the suites out. There should be two suites, one with name "All tests", the
    # other with name "new suite".
    def test_add_new_suite(self):
        self.assertEqual(1, len(self.bug.list_suites()))
        self.bug.add_new_test("test1", "Mobile")
        self.bug.add_new_test("test2", "Desktop")
        self.bug.add_new_suite("new suite", True, 4, ["test1"])
        self.assertEqual(["new suite", "All tests"], self.bug.list_suites())

    # Test for suite management: deletion and list
    # Ensure there are only the initial suite in the project, then add 2 tests and 2 suites. Next, delete a suite
    # specified by the suite name. After that, list out the suites to make sure only the correct suite is deleted
    # and the remaining suite are still there.
    def test_delete_suite(self):
        self.assertEqual(1, len(self.bug.list_suites()))
        self.bug.add_new_test("test1", "Mobile")
        self.bug.add_new_test("test2", "Desktop")
        self.bug.add_new_suite("new suite", True, 4, ["test1"])
        self.bug.add_new_suite("new suite 2", False, 2, ["test2"])
        self.bug.delete_suite("new suite")
        self.assertEqual(["new suite 2", "All tests"], self.bug.list_suites())

    def test_update_suite(self):
        self.assertEqual(1, len(self.bug.list_suites()))
        self.bug.add_new_test("test1", "Mobile")
        self.bug.add_new_test("test2", "Desktop")
        self.bug.add_new_suite("new suite", True, 4, ["test1"])
        self.bug.update_suite("new suite", "new suite 2", False, 2, ["test2"])
        self.assertEqual(["new suite 2", "All tests"], self.bug.list_suites())

    def tearDown(self):
        self.bug.tear_down()

    if __name__ == "__main__":
        unittest.main()
