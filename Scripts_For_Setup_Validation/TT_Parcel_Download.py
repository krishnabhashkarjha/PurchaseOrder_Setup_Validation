from helium import *
from AppResources import ElementLocator_For_PurchaseOrder_SetUp
import AppResources.ElementLocators as Element
from Utilites.ExcelOperations import ExcelOperations
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
Config.implicit_wait_secs = 30

class TT_Parcel_Download:

    def __init__(self,driver,wait,erp,supplier_name,retailer_name,Start_Date):
        self.driver = driver
        self.driver.get(Element.TT_url)
        self.wait = wait
        self.erp = erp
        ExcelOperations.set_value_to_cell(ElementLocator_For_PurchaseOrder_SetUp.INPUT_FILE_PATH, 2, 4, self.erp)
        self.supplier_name = supplier_name
        ExcelOperations.set_value_to_cell(ElementLocator_For_PurchaseOrder_SetUp.INPUT_FILE_PATH, 2, 1,
                                          self.supplier_name)
        self.retailer_name = retailer_name
        ExcelOperations.set_value_to_cell(ElementLocator_For_PurchaseOrder_SetUp.INPUT_FILE_PATH, 2, 2,
                                          self.retailer_name)
        self.Start_Date = Start_Date


    def search_parcel(self):
        # click('Transaction Tracker')
        time.sleep(5)
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(0))

        # select RETAILER
        self.wait.until(EC.element_to_be_clickable((By.XPATH, Element.COMPANY_SEARCH_INPUTBOX))).send_keys(
            self.retailer_name)
        dropdown_company_xpath = Element.Select_company_Part1 + self.retailer_name + Element.Select_company_Part2
        self.wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_company_xpath))).click()

        # select SUPPLIER
        self.wait.until(EC.element_to_be_clickable((By.XPATH, Element.TRADING_SEARCH_INPUTBOX))).send_keys(
            self.supplier_name)
        dropdown_tradingpartner_xpath = Element.Select_tradingpartner_Part1 + self.supplier_name + Element.Select_tradingpartner_Part2
        self.wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_tradingpartner_xpath))).click()

        # Select Accepted Status
        self.wait.until(EC.element_to_be_clickable((By.XPATH, Element.Status_dropdown))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, Element.Status_Accepted))).click()

        write(self.Start_Date, into='Start date')
        press(ENTER)
        write('850', into='Document Type')
        # self.driver.find_element_by_xpath(Element.TT_Search).click()
        self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_xpath(Element.TT_Search))

    def DownloadInput(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, Element.parcels_ids)))
        self.Parcels_list = []
        self.Parcels = self.driver.find_elements_by_xpath(Element.parcels_ids)

        # Get Parcels list
        for self.Parcel in self.Parcels:
            self.Parcels_list.append(self.Parcel.text)
        self.Parcels_list = self.Parcels_list[:3]
        print('Accepted Parcels are ', self.Parcels_list)

        # self.Download_directory = "C:/Users/" + getpass.getuser() + "/Downloads/"
        self.output = []
        for i in range(len(self.Parcels_list)):
            self.driver.execute_script("window.open('about:blank', 'tab2');")
            self.driver.switch_to.window("tab2")

            self.driver.get('https://commerce.spscommerce.com/transaction-tracker/preprod/transactions/' + self.Parcels_list[i])
            time.sleep(5)
            self.wait.until(EC.frame_to_be_available_and_switch_to_it(0))
            self.driver.find_element_by_xpath(Element.plus_click).click()
            self.output.append(self.driver.find_element_by_xpath(Element.file_url).text)

        for i in range(len(self.output)):
            a = self.output.__getitem__(i)
            self.output[i] = a.partition('u01')[2]
        print(self.output)

        for i in range(len(self.output)):
            self.driver.execute_script("window.open('about:blank', 'tab2');")
            self.driver.switch_to.window("tab2")

            self.driver.get('https://commshare.spspreprod.in/#/' + self.output[i])
            time.sleep(8)
        # self.driver.close()
