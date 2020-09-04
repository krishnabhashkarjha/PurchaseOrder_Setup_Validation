
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.action_chains import ActionChains


class SeleniumOperations:

    def __init__(self, driver,lo):
        self.driver = driver
        self.lo = lo
    def explicit_wait(self, v_element_id, v_element_id_type):
        if v_element_id_type == "BY_ID":
            try:
                element = WebDriverWait(self.driver, 100).until(
                    EC.presence_of_element_located((By.ID, v_element_id))
                )
            except NoSuchElementException:
                self.lo.log_to_file("ERROR", "Error in SeleniumOperations.Explicit_wait(). Element not found for id")

                return False
            return True

        if v_element_id_type == "BY_XPATH":
            try:
                element = WebDriverWait(self.driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, v_element_id))
                )
            except NoSuchElementException:
                self.lo.log_to_file("ERROR", "Error in SeleniumOperations.Explicit_wait(). Element not found for XPATH")

                return False
            return True

        if v_element_id_type == "BY_NAME":
            try:
                element = WebDriverWait(self.driver, 100).until(
                    EC.presence_of_element_located((By.NAME, v_element_id))
                )
            except NoSuchElementException:
                self.lo.log_to_file("ERROR", "Error in SeleniumOperations.Explicit_wait(). Element not found for NAME")

                return False
            return True

        if v_element_id_type == "BY_LINK_TEXT":
            try:
                element = WebDriverWait(self.driver, 100).until(
                    EC.presence_of_element_located((By.LINK_TEXT, v_element_id))
                )
            except NoSuchElementException:
                self.lo.log_to_file("ERROR", "Error in SeleniumOperations.Explicit_wait(). Element not found for Link text")

                return False
            return True



    def send_text_by_id(self, v_element_id, v_text_value):

        if self.explicit_wait(v_element_id, 'BY_ID'):
            self.driver.find_element_by_id(v_element_id).clear()
            #pyperclip.copy(v_text_value)
            self.driver.find_element_by_id(v_element_id).send_keys(v_text_value)
        else:
            self.lo.log_to_file("ERROR", "Error in SeleniumOperations.send_text(). Element not found for id")
            return False

    def send_text_by_xpath(self, v_element_id, v_text_value):

        if self.explicit_wait(v_element_id, 'BY_XPATH'):
            self.driver.find_element_by_xpath(v_element_id).clear()
            #pyperclip.copy(v_text_value)
            self.driver.find_element_by_xpath(v_element_id).send_keys(v_text_value)
        else:
            self.lo.log_to_file("ERROR", "Error in SeleniumOperations.send_text(). Element not found for id")
            return False

    def send_text_by_name(self, v_element_id, v_text_value):

        if self.explicit_wait(v_element_id, 'BY_NAME'):
            self.driver.find_element_by_name(v_element_id).clear()
            #pyperclip.copy(v_text_value)
            self.driver.find_element_by_name(v_element_id).send_keys(v_text_value)
        else:
            self.lo.log_to_file("ERROR", "Error in SeleniumOperations.send_text(). Element not found for id")
            return False


    def click_element_by_id(self, v_element_id):

        if self.explicit_wait(v_element_id, 'BY_ID'):
            self.driver.find_element_by_id(v_element_id).click()
        else:
            self.lo.log_to_file("ERROR", "Error in SeleniumOperations.Click(). Element not found for Id")
            return False

    def click_element_by_xpath(self, v_element_id):

        if self.explicit_wait(v_element_id, 'BY_XPATH'):
            self.driver.find_element_by_xpath(v_element_id).click()
        else:
            self.lo.log_to_file("ERROR", "Error in SeleniumOperations.Click(). Element not found for Id")
            return False

    def click_element_by_name(self, v_element_id):

        if self.explicit_wait(v_element_id, 'BY_NAME'):
            self.driver.find_element_by_name(v_element_id).click()
        else:
            self.lo.log_to_file("ERROR", "Error in SeleniumOperations.Click(). Element not found for Id")
            return False

    def click_element_by_link_text(self, v_element_id):

        if self.explicit_wait(v_element_id, 'BY_LINK_TEXT'):
            self.driver.find_element_by_link_text(v_element_id).click()
        else:
            self.lo.log_to_file("ERROR", "Error in SeleniumOperations.Click(). Element not found for Id")
            return False

    def get_text_by_id(self, v_element_id):

        if self.explicit_wait(v_element_id, 'BY_ID'):
            result = self.driver.find_element_by_id(v_element_id).text
            return result
        else:
            self.lo.log_to_file("ERROR", "Error in SeleniumOperations.text(). Element not found for Id")
            return False

    def get_text_by_xpath(self, v_element_id):

        if self.explicit_wait(v_element_id, 'BY_XPATH'):
            result = self.driver.find_element_by_xpath(v_element_id).text
            return result
        else:
            self.lo.log_to_file("ERROR", "Error in SeleniumOperations.text(). Element not found for Id")
            return False

    def get_text_by_name(self, v_element_id):

        if self.explicit_wait(v_element_id, 'BY_NAME'):
            result = self.driver.find_element_by_name(v_element_id).text
            return result
        else:
            self.lo.log_to_file("ERROR", "Error in SeleniumOperations.text(). Element not found for Id")
            return False

    def get_attribute_value_by_id(self, v_element_id):

        if self.explicit_wait(v_element_id, 'BY_ID'):
            result = self.driver.find_element_by_id(v_element_id).get_attribute('value')
            return result
        else:
            self.lo.log_to_file("ERROR", "Error in SeleniumOperations.text(). Element not found for Id")
            return False

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def check_exists_by_name(self, name):
        try:
            self.driver.find_element_by_name(name)
        except NoSuchElementException:
            return False
        return True

    def check_exists_by_id(self, id):
        try:
            self.driver.find_element_by_id(id)
        except NoSuchElementException:
            return False
        return True

    def scroll_into_view_by_id(self, v_element_id):
        time.sleep(3)
        if self.explicit_wait(v_element_id, 'BY_ID'):
            element = self.driver.find_element_by_id(v_element_id)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        else:
            self.lo.log_to_file("ERROR", "Error in SeleniumOperations.scroll_into_view(). Element not found for Id")
            return False

    def scroll_into_view_by_xpath(self, v_element_id):
        time.sleep(3)
        if self.explicit_wait(v_element_id, 'BY_XPATH'):
            element = self.driver.find_element_by_xpath(v_element_id)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        else:
            self.lo.log_to_file("ERROR", "Error in SeleniumOperations.scroll_into_view(). Element not found for xpath")
            return False

    def scroll_into_view_by_name(self, v_element_id):
        time.sleep(3)
        if self.explicit_wait(v_element_id, 'BY_NAME'):
            element = self.driver.find_element_by_name(v_element_id)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        else:
            self.lo.log_to_file("ERROR", "Error in SeleniumOperations.scroll_into_view(). Element not found for name")
            return False

    def double_click_by_name(self, v_element_id):

        if self.explicit_wait(v_element_id, 'BY_NAME'):
            element = self.driver.find_element_by_name(v_element_id)
            actionchains = ActionChains(self.driver)
            actionchains.double_click(element).perform()
        else:
            self.lo.log_to_file("ERROR", "Error in SeleniumOperations.double_click(). Element not found for name")
            return False


    def double_click_by_xpath(self, v_element_id):

        if self.explicit_wait(v_element_id, 'BY_XPATH'):
            element = self.driver.find_element_by_xpath(v_element_id)
            actionchains = ActionChains(self.driver)
            actionchains.double_click(element).perform()
        else:
            self.lo.log_to_file("ERROR", "Error in SeleniumOperations.double_click(). Element not found for xpath")
            return False

    def double_click_by_id(self, v_element_id):

        if self.explicit_wait(v_element_id, 'BY_ID'):
            element = self.driver.find_element_by_id(v_element_id)
            actionchains = ActionChains(self.driver)
            actionchains.double_click(element).perform()
        else:
            self.lo.log_to_file("ERROR", "Error in SeleniumOperations.double_click(). Element not found for ID")
            return False