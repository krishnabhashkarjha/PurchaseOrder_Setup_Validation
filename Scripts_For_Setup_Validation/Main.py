import time
import pandas as pd
from selenium import webdriver
import AppResources.ElementLocators as Element
from Scripts_For_Setup_Validation.FTPUploadOperations import FTP_Upload
from Scripts_For_Setup_Validation.GenerateInputs import Generate_Inputs
from Scripts_For_Setup_Validation.TT_Parcel_Download import TT_Parcel_Download
from helium import *
from selenium.webdriver.support.ui import WebDriverWait
from Utilites.ExcelOperations import ExcelOperations

class Main_Executor():
    def __init__(self):
        self.df_InputFile = pd.read_excel(Element.INPUT_FILE_PATH, sheet_name='ParcelsFromTT')
        #self.driver = webdriver.Chrome('chromedriver.exe')
        self.driver = start_chrome()
        self.wait = WebDriverWait(self.driver, 70)
        self.erp = self.df_InputFile.iloc[0][0]
        self.supplier_name = self.df_InputFile.iloc[0][1]               #get supplier name from input file
        self.retailer_name = self.df_InputFile.iloc[0][2]               #get retailer name from input file
        self.Start_Date = self.df_InputFile.iloc[0][3]
        self.No_of_Parcels = self.df_InputFile.iloc[0][4]
        self.No_of_Parcels = int(self.No_of_Parcels)
    
    def Execute_GenerateInputs(self):
        generatingInput = Generate_Inputs(self.driver, self.wait, self.erp,self.supplier_name, self.retailer_name, self.Start_Date, self.No_of_Parcels)
        generatingInput.Login()
        generatingInput.TTSearch()
        generatingInput.DownloadInput()
        generatingInput.DeleteDupliacteFiles()
        
        self.SDQ_present_Flag = generatingInput.EdiValidations()
        self.filepaths = generatingInput.GetIDs()
        print('SDQ present in file ?', self.SDQ_present_Flag)
        ExcelOperations.set_value_to_cell(Element.Output_File_Path,5,2,self.SDQ_present_Flag)
        print('In Main file', self.filepaths)

    def Execute_FTP_Upload(self):
        upload = FTP_Upload(self.driver, self.filepaths)
        upload.Login_FTP()
        upload.Upload_files()

    def Accept_Parecl_validation(self):
        self.driver.execute_script("window.open('about:blank', 'tab2');")
        self.driver.switch_to.window("tab2")
        time.sleep(5)
        parcel = TT_Parcel_Download(self.driver, self.wait, self.erp,self.supplier_name, self.retailer_name, self.Start_Date)
        parcel.search_parcel()
        parcel.DownloadInput()
        
         