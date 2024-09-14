import os
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

CHROME_DRIVER_PATH = os.environ["CHROME_DRIVER_PATH"]
BUGBUG_EMAIL = os.environ["BUGBUG_EMAIL"]
BUGBUG_PASSWORD = os.environ["BUGBUG_PASSWORD"]
BUGBUG_PATH = "https://app.bugbug.io/sign-in/"

class BugBug:
    def __init__(self, driver):
        self.driver = driver

    def sign_in_to_bugbug(self):
        self.driver.get(BUGBUG_PATH)
        wait = WebDriverWait(self.driver, 20)
        new_project_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="email"]')))
        new_project_button.send_keys(BUGBUG_EMAIL)
        new_project_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="password"]')))
        new_project_button.send_keys(BUGBUG_PASSWORD)
        button = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[1]/form/button')
        button.click()

    def add_new_project(self, project_name):
        wait = WebDriverWait(self.driver, 20)
        new_project_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="ProjectList.NewProjectButton"]')))
        new_project_button.click()
        project_name_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="name"]')))
        project_name_field.send_keys(project_name)
        homepage_url = self.driver.find_element(By.CSS_SELECTOR, '[name="homepageUrl"]')
        homepage_url.send_keys("https://app.bugbug.io/sign-in/")
        create_project_button = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div/form/div[2]/button[2]')
        create_project_button.click()
        cancel_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/form/div[2]/button[1]')))
        cancel_button.click()

    def list_newest_project(self):
        wait = WebDriverWait(self.driver, 20)
        bugbug_link = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/nav/div/a')
        bugbug_link.click()

        newest_project = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div[2]/div/a[1]/div[2]/p')))
        return newest_project.text

    def add_new_test(self, test_title, screen_size):
        wait = WebDriverWait(self.driver, 2)
        try:
            new_project_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="name"]')))
        except TimeoutException:
            test_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/aside/div/nav/li[1]/div/a')))
            test_button.click()
            add_new_test_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="app"]/div/div[2]/section/div/div/div/div/div[1]/header/div/div[2]/div/button')))
            add_new_test_button.click()
            new_project_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="name"]')))

        new_project_button.send_keys(test_title)
        screen_size_selector = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/form/div[1]/div[2]/div/button')))
        # test changing screen sizes
        screen_size_selector.click()
        if (screen_size == "Mobile"):
            mobile = wait.until(EC.element_to_be_clickable((By.XPATH,  '//*[@id="dropdown"]/div/div/button[2]/div[2]/span/div')))
            mobile.click()
        elif (screen_size == "Desktop"):
            desktop = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dropdown"]/div/div/button[1]')))
            desktop.click()
        create_test_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/form/div[2]/button[2]')))
        create_test_button.click()
        time.sleep(1)

    # Helper function for delete and update test

    def _wait_for_elements(self):
        wait = WebDriverWait(self.driver, 20)
        test_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/aside/div/nav/li[1]/div/a')))
        test_button.click()
        time.sleep(1)
        return self.driver.find_elements(By.XPATH,
                                         '//*[@id="app"]/div/div[2]/section/div/div/div/div/div[2]/div[2]/div/div/div/a')

    # Helper function for delete and update test
    def _hover_and_click(self, a_element, button_xpath):
        element_to_hover = a_element.find_element(By.XPATH, './/div[2]')
        actions = ActionChains(self.driver)
        actions.move_to_element(element_to_hover).perform()
        time.sleep(2)

        element_to_click = a_element.find_element(By.XPATH, button_xpath)
        element_to_click.click()

    def delete_test(self, test_title):
        a_elements = self._wait_for_elements()
        for a_element in a_elements:
            try:
                span_element = a_element.find_element(By.XPATH,
                                                      ".//div[2]/span[contains(text(), '{}')]".format(test_title))
                if span_element:
                    self._hover_and_click(a_element, './/div[5]/div/div[2]/div/button')
                    time.sleep(1)
                    delete_button = self.driver.find_element(By.XPATH, '//*[@id="dropdown"]/div/button[7]')
                    delete_button.click()
                    delete_confirm_button = self.driver.find_element(By.XPATH,
                                                                     '//*[@id="app"]/div/div[2]/div/div/div/div[2]/button[2]')
                    delete_confirm_button.click()
                    time.sleep(1)
                    break
            except NoSuchElementException:
                continue

    def update_test(self, old_test_title, new_test_title, screen_size):
        a_elements = self._wait_for_elements()
        for a_element in a_elements:
            try:
                span_element = a_element.find_element(By.XPATH,
                                                      ".//div[2]/span[contains(text(), '{}')]".format(old_test_title))
                if span_element:
                    self._hover_and_click(a_element, './/div[5]/div/div[2]/div/button')
                    time.sleep(1)
                    update_button = self.driver.find_element(By.XPATH, '//*[@id="dropdown"]/div/button[3]')
                    update_button.click()

                    new_project_button = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="name"]')))
                    new_project_button.send_keys(new_test_title)

                    screen_size_selector = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/form/div[1]/div[2]/div/button')))
                    screen_size_selector.click()
                    time.sleep(1)

                    if screen_size == "Mobile":
                        mobile = self.driver.find_element(By.XPATH,
                                                          '//*[@id="dropdown"]/div/div/button[2]/div[2]/span/div')
                        mobile.click()
                    elif screen_size == "Desktop":
                        desktop = self.driver.find_element(By.XPATH,
                                                           '//*[@id="dropdown"]/div/div/button[1]/div[2]/span/div')
                        desktop.click()

                    save_confirm_button = self.driver.find_element(By.XPATH,
                                                                   '//*[@id="app"]/div/div[2]/div/div/form/div[2]/button[2]')
                    save_confirm_button.click()
                    break
            except NoSuchElementException:
                continue

    def list_test(self):
        wait = WebDriverWait(self.driver, 20)
        time.sleep(1)
        test_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/aside/div/nav/li[1]/div/a')))
        test_button.click()
        list_of_tests = {}
        time.sleep(1)

        '//*[@id="app"]/div/div[2]/section/div/div/div/div/div[2]/div[2]/div/div/div/a[1]/div[3]/div/div'
        a_elements = self.driver.find_elements(By.XPATH,
                                          '//*[@id="app"]/div/div[2]/section/div/div/div/div/div[2]/div[2]/div/div/div/a')
        for a_element in a_elements:
            # Try to locate the <span> inside the <a> element
            try:
                span_element = a_element.find_element(By.XPATH,
                                                      ".//div[2]/span")
                screen_size = a_element.find_element(By.XPATH, ".//div[3]/div/div")
                list_of_tests[span_element.text] = screen_size.text
            except NoSuchElementException:
                # If the <span> element or the target div is not found inside this <a>, continue to the next one
                continue
        return list_of_tests

    def add_new_suite(self, suite_name, auto_add, auto_retry, tests):
        wait = WebDriverWait(self.driver, 20)
        suite_nav = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/aside/div/nav/li[2]/div/a')))
        suite_nav.click()
        time.sleep(1)
        create_new_suite_button = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section/div/div/div/div/div[1]/header/div/div/div/button')
        create_new_suite_button.click()
        suite_name_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="name"]')))
        suite_name_field.send_keys(suite_name)
        if auto_add:
            auto_add_new_test = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/form/div[1]/div/div[1]/div[2]/div/button')))
            auto_add_new_test.click()
            true_button = self.driver.find_element(By.XPATH, '//*[@id="dropdown"]/div/div/button[1]')
            true_button.click()
        auto_retry_selector = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/form/div[1]/div/div[1]/div[3]/div/button')
        auto_retry_selector.click()
        auto_retry_picker = self.driver.find_element(By.XPATH, f'//*[@id="dropdown"]/div/div/button[{auto_retry + 1}]')
        auto_retry_picker.click()
        for test in tests:
            test_divs = self.driver.find_elements(By.XPATH,
                                                       f'//*[@id="app"]/div/div[2]/div/div/form/div[1]/div/div[2]/div/div[1]/div[2]/div')
            for test_div in test_divs:
                try:
                    if test_div.find_element(By.XPATH, './/span').text == test:
                        button_element = test_div.find_element(By.XPATH, './/button')
                        button_element.click()

                except Exception as e:
                    print(f"An error occurred: {e}")

        submit_button = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/form/div[2]/button[2]')
        submit_button.click()
        time.sleep(2)

    def delete_suite(self, suite_name):
        wait = WebDriverWait(self.driver, 20)
        suite_nav_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/aside/div/nav/li[2]/div/a')))
        suite_nav_button.click()
        time.sleep(1)
        suites = self.driver.find_elements(By.XPATH, '//*[@id="app"]/div/div[2]/section/div/div/div/div/div[3]/div[2]/div/div/div/a')
        for suite in suites:
            try:
                span_element = suite.find_element(By.XPATH, ".//div[2]/span")
                if span_element.text == suite_name:
                    time.sleep(1)
                    suite.find_element(By.XPATH, ".//div[1]/div/div/input").click()
                    choice_button = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section/div/div/div/div/div[1]/header/div/div/div/div/button')
                    choice_button.click()
                    time.sleep(1)
                    delete_button = self.driver.find_element(By.XPATH, '//*[@id="dropdown"]/div/button[4]')
                    delete_button.click()
                    confirm_delete_button = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/button[2]')
                    confirm_delete_button.click()
                    time.sleep(1)
                    break
            except NoSuchElementException:
                print("No such suite")
                continue

    def update_suite(self, suite_name, new_suite_name, auto_add, auto_retry, tests):
        wait = WebDriverWait(self.driver, 20)
        suite_nav_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/aside/div/nav/li[2]/div/a')))
        suite_nav_button.click()
        time.sleep(1)
        suites = self.driver.find_elements(By.XPATH,
                                           '//*[@id="app"]/div/div[2]/section/div/div/div/div/div[3]/div[2]/div/div/div/a')
        print(len(suites))
        for suite in suites:
            try:
                span_element = suite.find_element(By.XPATH, ".//div[2]/span")
                print("span element text" + span_element.text)
                if span_element.text == suite_name:
                    print("Found" + suite_name)
                    time.sleep(1)
                    actions = ActionChains(self.driver)
                    actions.move_to_element(suite).click().perform()
                    wait.until(EC.element_to_be_clickable((By.XPATH, ".//div[5]/div/div[2]/div/button"))).click()
                    time.sleep(1)
                    self.driver.find_element(By.XPATH, '//*[@id="dropdown"]/div/button[3]').click()
                    time.sleep(1)
                    suite_name_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="name"]')))
                    suite_name_field.clear()
                    suite_name_field.send_keys(new_suite_name)
                    if auto_add:
                        auto_add_new_test = wait.until(EC.element_to_be_clickable(
                            (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/form/div[1]/div/div[1]/div[2]/div/button')))
                        auto_add_new_test.click()
                        true_button = self.driver.find_element(By.XPATH, '//*[@id="dropdown"]/div/div/button[1]')
                        true_button.click()
                    else:
                        auto_add_new_test = wait.until(EC.element_to_be_clickable(
                            (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/form/div[1]/div/div[1]/div[2]/div/button')))
                        auto_add_new_test.click()
                        false_button = self.driver.find_element(By.XPATH, '//*[@id="dropdown"]/div/div/button[2]')
                        false_button.click()
                    auto_retry_selector = self.driver.find_element(By.XPATH,
                                                                   '//*[@id="app"]/div/div[2]/div/div/form/div[1]/div/div[1]/div[3]/div/button')
                    auto_retry_selector.click()
                    auto_retry_picker = self.driver.find_element(By.XPATH,
                                                                 f'//*[@id="dropdown"]/div/div/button[{auto_retry + 1}]')
                    auto_retry_picker.click()
                    for test in tests:
                        test_divs = self.driver.find_elements(By.XPATH,
                                                              f'//*[@id="app"]/div/div[2]/div/div/form/div[1]/div/div[2]/div/div[1]/div[2]/div')
                        for test_div in test_divs:
                            try:
                                if test_div.find_element(By.XPATH, './/span').text == test:
                                    button_element = test_div.find_element(By.XPATH, './/button')
                                    button_element.click()

                            except Exception as e:
                                print(f"An error occurred: {e}")

                    submit_button = self.driver.find_element(By.XPATH,
                                                             '//*[@id="app"]/div/div[2]/div/div/form/div[2]/button[2]')
                    submit_button.click()
                    break
            except NoSuchElementException:
                print("No such suite")
                continue

    def list_suites(self):
        suite_names = []
        wait = WebDriverWait(self.driver, 20)
        suite_nav_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/aside/div/nav/li[2]/div/a')))
        suite_nav_button.click()
        time.sleep(1)
        suites = self.driver.find_elements(By.XPATH,
                                           '//*[@id="app"]/div/div[2]/section/div/div/div/div/div[3]/div[2]/div/div/div/a')
        print(len(suites))
        for suite in suites:
            try:
                span_element = suite.find_element(By.XPATH, ".//div[2]/span")
                suite_names.append(span_element.text)
            except NoSuchElementException:
                print("No such suite")
                continue
        return suite_names

    def tear_down(self):
        self.driver.close()