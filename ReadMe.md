**Instructions for Running Test Cases:**
1. Prerequisites: Ensure that Python, Selenium WebDriver, and Selenium ChromeDriver are installed on your system.
2. Clone the Repository: Clone the repository and open the project in PyCharm.
3. Install Dependencies: In PyCharm, install the necessary dependencies. For any unresolved imports (highlighted in red), click on the lightbulb icon that appears to resolve them automatically. 
4. Set Environment Variables: Set the following environment variables in the run configuration:
- CHROME_DRIVER_PATH: Path to ChromeDriver on your machine. 
- BUGBUG_EMAIL and BUGBUG_PASSWORD: Credentials for accessing relevant services.
5. Configure the Run Settings: In the run configuration, set the "Script" field to the file path of test/test.py. 
6. Run the Tests: After configuring the environment, the test cases should be ready to run within PyCharm.



**Some Limitations and Areas for Improvement of the tests:**
1. Test Coverage: The current tests do not cover all potential cases.

For Projects:

- Functionalities for deleting and updating projects have not been tested.
- The test for listing projects only verifies the most recent project. Tests still be added to verify that all projects and their details are listed.

For Create Tests:

- If a project name is not defined, it should be automatically generated. This functionality is not currently tested.
Screen size options include a third choice, “Change default screen sizes,” which also has not been tested.
- Tests for adding content, such as starting a recording, adding a new step manually, or inserting existing components, are missing.

For Delete Tests:
- When the “Are you sure you want to delete this test?” popup appears, clicking “Cancel” should prevent the deletion. This scenario has not been tested.

For Create Suites:
- Tests do not currently cover changing the "Parallel cloud run" and "Profile" settings during suite creation.
- Additional test coverage is needed for reordering selected tests, removing specific tests, and searching for tests during suite creation.

For List Suites:
- Currently, only suite names are listed in tests. The tests should also verify suite details, such as "auto add new tests" settings and test order.

2. Code Readability and Maintenance:
- Many functions currently use time.sleep(), which can result in slower test execution and is a bad practice. Using wait.until() would reduce execution time and improve reliability.
- The reason time.sleep() remains in the code is that removing it has introduced some bugs, and I have not yet identified and fixed all of them.
