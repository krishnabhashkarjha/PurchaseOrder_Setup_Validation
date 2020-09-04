
import time
import AppResources.ElementLocators as Element
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FTP_Upload():
    def __init__(self, driver, file_paths):
        self.driver = driver
        self.driver.maximize_window()
        self.driver.get('https://commshare.spspreprod.in/WebInterface/login.html')
        self.wait = WebDriverWait(self.driver, 50)
        self.file_paths = file_paths
        
    def Login_FTP(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, Element.ftp_username_path))).send_keys(Element.ftp_username)
        self.driver.find_element_by_xpath(Element.ftp_password_path).send_keys(Element.password)
        self.driver.find_element_by_xpath(Element.Remember_Me_path).click()
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, Element.ftp_login))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, Element.ftp_folder)))
        self.driver.get(Element.FTP_PREPROD_LINK)
        
    def Upload_files(self):
        time.sleep(3)
        #print(self.file_paths)
        for file_path in self.file_paths:
            #self.wait.until(EC.element_to_be_clickable((By.XPATH, Element.FTP_add_file))).send_keys("f"+file_path)
            self.driver.find_element_by_xpath(Element.FTP_add_file).send_keys(file_path)
            time.sleep(1)
        
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(2))
        # self.driver.find_element_by_xpath(Element.btn_upload).click()
        self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_xpath(Element.btn_upload))
        self.driver.switch_to.default_content()

        for i in range(3):
            time.sleep(4)
            self.driver.find_element_by_xpath(Element.FTP_Refresh).click()
            #break
        
    
    