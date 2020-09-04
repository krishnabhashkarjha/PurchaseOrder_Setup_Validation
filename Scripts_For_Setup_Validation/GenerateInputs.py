import AppResources.ElementLocators as Element
from AppResources import ElementLocator_For_PurchaseOrder_SetUp
from selenium import webdriver
from helium import *
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilites.ExcelOperations import ExcelOperations
from selenium.webdriver.common.by import By
import time
Config.implicit_wait_secs = 30
import os
import tkinter as tk
from tkinter import messagebox
import sys

class Generate_Inputs:
    def __init__(self, driver, wait, erp,supplier_name, retailer_name, Start_Date, No_of_Parcels):
        self.driver = driver
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
        self.No_of_Parcels = No_of_Parcels
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.attributes("-topmost", True)

    def Login(self):
        self.driver.maximize_window()
        self.driver.get('https://commerce.spscommerce.com/auth/login/')
        wait_until(Button('Sign in').exists)
        write(Element.username, into='Email Address')
        write(Element.password, into='Password')
        click('Sign in')

    def TTSearch(self):
        click('Transaction Tracker')
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(0))
        
        #select RETAILER
        self.wait.until(EC.element_to_be_clickable((By.XPATH, Element.COMPANY_SEARCH_INPUTBOX))).send_keys(self.retailer_name)
        dropdown_company_xpath = Element.Select_company_Part1 + self.retailer_name + Element.Select_company_Part2
        self.wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_company_xpath))).click()
        
        #select SUPPLIER
        self.wait.until(EC.element_to_be_clickable((By.XPATH, Element.TRADING_SEARCH_INPUTBOX))).send_keys(self.supplier_name)
        dropdown_tradingpartner_xpath = Element.Select_tradingpartner_Part1 + self.supplier_name + Element.Select_tradingpartner_Part2
        self.wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_tradingpartner_xpath))).click()
        
        #Select Accepted Status
        self.wait.until(EC.element_to_be_clickable((By.XPATH, Element.Status_dropdown))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, Element.Status_Accepted))).click()
        
        write(self.Start_Date, into='Start date')
        press(ENTER)
        write('850', into='Document Type')
        #self.driver.find_element_by_xpath(Element.TT_Search).click()
        self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_xpath(Element.TT_Search))

    def DownloadInput(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, Element.parcels_ids)))
        self.Parcels_list = []
        self.Parcels = self.driver.find_elements_by_xpath(Element.parcels_ids)
        
        #Get Parcels list
        for self.Parcel in self.Parcels:
            self.Parcels_list.append(self.Parcel.text) 
        self.Parcels_list = self.Parcels_list[:self.No_of_Parcels]
        print('Accepted Parcels are ',self.Parcels_list)
        
        #self.Download_directory = "C:/Users/" + getpass.getuser() + "/Downloads/"
        curr_parcel_count = 0
        for i in range(len(self.Parcels_list)):
            if curr_parcel_count==0:
                self.driver.execute_script("window.open('about:blank', 'tab2');")
                self.driver.switch_to.window("tab2")
        
                self.driver.get('https://commerce.spscommerce.com/transaction-tracker/prod/transactions/'+self.Parcels_list[i])
                time.sleep(5)
                self.wait.until(EC.frame_to_be_available_and_switch_to_it(0))
                #self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.driver.find_element_by_xpath(Element.Input_Download_selector)))
                self.wait.until(EC.element_to_be_clickable((By.XPATH, Element.Input_Download_selector))).click()
                self.wait.until(EC.element_to_be_clickable((By.XPATH, Element.Input_Download))).click()                
                click('SIP 7.0 PurchaseOrder')
                #self.wait.until(EC.frame_to_be_available_and_switch_to_it(0))
                self.wait.until(EC.presence_of_element_located((By.XPATH, Element.Get_TPID)))
                self.TPID = self.driver.find_element_by_xpath(Element.Get_TPID).text
                self.TPID = str(self.TPID.split('>')[1].split('<')[0])
                print(self.TPID)
                #time.sleep(4)  
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            else:
                self.driver.execute_script("window.open('about:blank', 'tab2');")
                self.driver.switch_to.window("tab2")
                
                self.driver.get('https://commerce.spscommerce.com/transaction-tracker/prod/transactions/'+self.Parcels_list[i])
                time.sleep(4)
                self.wait.until(EC.frame_to_be_available_and_switch_to_it(0))
                #self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.driver.find_element_by_xpath(Element.Input_Download_selector)))
                self.wait.until(EC.element_to_be_clickable((By.XPATH, Element.Input_Download_selector))).click()
                self.wait.until(EC.element_to_be_clickable((By.XPATH, Element.Input_Download))).click()
                time.sleep(3)
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            curr_parcel_count += 1
        
        #Wait for files to download and get their paths
        self.file_paths = WebDriverWait(self.driver, 120, 1).until(self.every_downloads_chrome)
        print('Downloaded files are ', self.file_paths)    
        
    def every_downloads_chrome(self, driver):
        time.sleep(3)
        if not driver.current_url.startswith("chrome://downloads"):
            driver.get("chrome://downloads/")
        return driver.execute_script("""
            return document.querySelector('downloads-manager')
            .shadowRoot.querySelector('#downloadsList')
            .items.filter(e => e.state === 'COMPLETE')
            .map(e => e.filePath || e.file_path || e.fileUrl || e.file_url);
            """)
            
    def DeleteDupliacteFiles(self):
        #find duplicate files
        files_to_be_deleted = [str for str in self.file_paths if
             any(sub in str for sub in ['(',')'])]
        #delete duplicate files
        try:
            for i in files_to_be_deleted:
                os.remove(i)
        except FileNotFoundError:
            pass
        #Remaining files to be processed
        self.file_paths = [i for i in self.file_paths if i not in files_to_be_deleted]
        print('Final Files to be processed', self.file_paths)
        
        if not self.file_paths:
            messagebox.showinfo("Downloading Files Error",'There already exist same files in directory, please delete them and try again.', parent=self.root)
            self.driver.quit()
            sys.exit('Downloading Files Error')
            
    def EdiValidations(self):
        i = 1
        self.SDQ_present_Flag = False
        for self.file_path in self.file_paths:        
            with open(self.file_path) as f:               #Count lines present in file
                line_count = 0
                for line in f:
                    line_count += 1
            
            if line_count == 1:                           #if only one line present in file then read the file as data and unwanted symbols by new line 
                file1 = open(self.file_path, "r")
                data = file1.read()
                tilt = data.partition('GS')[0:-1][0][-1]  #get the unwanted symbol(tilt)
                data = data.replace(tilt, "\n")
                file1.close()
            
                file1 = open(self.file_path, "w")
                file1.write(data)
                file1.close()
                print("-> Successfully removed tilts/unwanted symbols from file ", i)
            ####################################################################################    
            #get delimeter (* symbol)
            TestData = open(self.file_path)
            test_data = TestData.readlines()
            self.delimeter = test_data[0][3]
            #####################################################################################
            #ST to SE lines count Validation
            
            print("-> ST to SE line Count Validation")
            file = open(self.file_path, 'r')
            linelist = file.readlines()
            file.close()
            if len(linelist) <= 2:
                with open(self.file_path, 'r') as f:
                    for line in f.readlines():
                        first_line = line.split("GS")[0]
                        # print(first_line)
                        delemitor = first_line.split("ISA")[1][0:1]
            else:
                f = open(self.file_path, 'r')
                first_line = f.readline()
                delemitor = first_line.split("ISA")[1][0:1]
            with open(self.file_path, 'r') as fii:
                j = 1
                for line in fii:
                    # print(line)
                    if line.startswith('SE'):
                        # print(line)  # output: SE*39*113986
                        for ch in [delemitor]:
                            if ch in line:
                                y = line.split(delemitor)
                        SE_at_second_position = y[1]
                        # print(SE_at_second_position)
                        break
                    j += 1
                # print("SE is present at line no : ", j)
            fii.close()
            line_no_at_which_SE_is_present = j
            no_of_lines_between_ST_and_SE = line_no_at_which_SE_is_present - 2
            print(f"       Number of Line between ST and SE are : {str(no_of_lines_between_ST_and_SE)}")  # output 39
            print(f"       SE at second positins : {str(SE_at_second_position)}")  # output 39

            if str(SE_at_second_position) == str(no_of_lines_between_ST_and_SE):
                print("       Lines difference between ST and SE segments are correct")
            else:
                print("       Lines difference between ST and SE segments is not correct")
                self.Validation_Error_Process_Stop("Lines difference between ST and SE segments is not correct\n Process stopped")
            
            #####################################################################################
            #ST and GE Count Validation
            
            print("-> ST and GE count validation")
            with open(self.file_path, 'r') as fi:
                k = 0
                for line in fi:
                    # print(line)
                    if line.startswith('ST'):
                        # print(line)  # output: ST*850*113986
                        k += 1
                print(f"       Number of Time ST is present : {k}")
                ST_Count = str(k)
            fi.close()
            with open(self.file_path, 'r') as fii:
                j = 1
                for line in fii:
                    if line.startswith('GE'):
                        # print(line)
                        GE_line = line
                        break
                    j += 1
                # print("GE is present at line Number :", j)
            fii.close()
            GE_count = str(GE_line.split(self.delimeter)[1])
            print(f"       GE count number is : {GE_count}")
            if ST_Count == GE_count:
                print("       GE count is equal to count of ST segment present in the file.")
            else:
                print("       GE count and ST count did not match")
                self.Validation_Error_Process_Stop("GE count and ST count did not match, Process stopped")
            #k += 1
            print("_____________________________________________________________________")
            
            #####################################################################################
            #Check for SDQ segment in file
            
            if self.SDQ_present_Flag == False:
                with open(self.file_path, 'r') as read_obj:
                    for line in read_obj:
                        if 'SDQ' in line:
                            self.SDQ_present_Flag = True                

            i = i + 1                
        return self.SDQ_present_Flag 
    
    def Validation_Error_Process_Stop(self, message):        
        messagebox.showinfo("Validation Error",message, parent=self.root)
        self.driver.quit()
        sys.exit('Valdations Falied')
    
    def GetIDs(self):
        TestData = open(self.file_paths[0])
        test_data = TestData.readlines()
        self.delimeter = test_data[0][3]

        Retailer_Qual = str(test_data[0].split(self.delimeter)[5])
        Retailer_ISA_ID = str(test_data[0].split(self.delimeter)[6]).strip()
        Retailer_ISA_ID = str(Retailer_Qual)+':'+str(Retailer_ISA_ID)
        ExcelOperations.set_value_to_cell(ElementLocator_For_PurchaseOrder_SetUp.INPUT_FILE_PATH, 2, 7, Retailer_ISA_ID)

        Retailer_Group_ID = str(test_data[1].split(self.delimeter)[2]).strip()
        ExcelOperations.set_value_to_cell(ElementLocator_For_PurchaseOrder_SetUp.INPUT_FILE_PATH, 2, 8,Retailer_Group_ID)
        
        Supplier_Qual = str(test_data[0].split(self.delimeter)[7])
        Supplier_ISA_ID = str(test_data[0].split(self.delimeter)[8]).strip()
        Supplier_ISA_ID = str(Supplier_Qual)+':'+str(Supplier_ISA_ID)
        ExcelOperations.set_value_to_cell(ElementLocator_For_PurchaseOrder_SetUp.INPUT_FILE_PATH, 2, 5, Supplier_ISA_ID)

        Supplier_Group_ID = str(test_data[1].split(self.delimeter)[3]).strip()
        ExcelOperations.set_value_to_cell(ElementLocator_For_PurchaseOrder_SetUp.INPUT_FILE_PATH, 2, 6,Supplier_Group_ID)
        
        TPID = self.TPID
        print(TPID)
        print('Retailer ', Retailer_ISA_ID, Retailer_Group_ID)
        print('Supplier', Supplier_ISA_ID, Supplier_Group_ID)
        return self.file_paths
        
        
        
            
            
            
            
            