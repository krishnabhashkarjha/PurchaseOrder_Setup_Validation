import time
import pandas
from Utilites.ExcelOperations import ExcelOperations
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from AppResources import ElementLocator_For_PurchaseOrder_SetUp as Element
from Scripts_For_Setup_Validation.Setup_Methods import setup_methods
from AppResources import ElementLocators as file


class Extention_Verification:

    def __init__(self,driver, log, seleniumOperation):
        self.driver = driver
        self.log = log
        self.seleniumOperation = seleniumOperation
        self.wait = WebDriverWait(self.driver, 10)
        self.input_file = pandas.read_excel(Element.INPUT_FILE_PATH, sheet_name='Nexus_Input')
        self.supplier_name = self.input_file.at[0, 'Supplier Name']
        self.retailer_name = self.input_file.at[0, 'Retailer Name']
        self.df_IDs = pandas.DataFrame(
            columns=['Supplier ISA ID', 'Supplier Group ID', 'Retailer ISA ID', 'Retailer Group ID', 'Sender TPID',
                     'Receiver Profile ID'], dtype=object)
        self.df_retailer_version = pandas.DataFrame(columns=['Doctype','Service','Version'])

    def receiver_search(self):
        try:
            time.sleep(15)
            self.log.log_to_file(self, "INFO", " Start Searching in Receiver Side ! ")
            self.driver.execute_script("window.open('about:blank', 'tab2');")
            self.driver.switch_to.window("tab2")
            self.driver.get(Element.nexus_relation_link)
            time.sleep(10)
            self.wait.until(EC.frame_to_be_available_and_switch_to_it(0))
            # self.seleniumOperation.click_element_by_xpath(Element.Network)
            # self.seleniumOperation.click_element_by_xpath(Element.relationships_tab)
            self.seleniumOperation.click_element_by_xpath(Element.advance_search)
            # for sender selection
            self.seleniumOperation.click_element_by_xpath(Element.sender_search_selcetor)
            self.seleniumOperation.click_element_by_xpath(Element.sender_exact_match)
            self.seleniumOperation.send_text_by_xpath(Element.sender_name_box, self.supplier_name)
            time.sleep(3)
            # for receiver selection
            self.seleniumOperation.click_element_by_xpath(Element.receiver_search_selecetor)
            self.seleniumOperation.click_element_by_xpath(Element.receiver_exact_match)
            self.seleniumOperation.send_text_by_xpath(Element.receiver_name_box, self.retailer_name)
            time.sleep(3)
            self.seleniumOperation.click_element_by_xpath(Element.search_click)
            time.sleep(3)
            # self.seleniumOperation.click_element_by_xpath(Element.toggle_compact_view)
        except Exception as e:
            self.log.log_to_file(self, "ERROR", " ERROR in receiver_search in Extention_verification" + str(e))

    def ExtractIDs(self):
        time.sleep(4)
        self.log.log_to_file(self, "INFO", " Extracting TDs from Receiver Side ! ")
        self.supplier_ISA_IDs_list = []
        self.supplier_ISA_IDs = self.driver.find_elements_by_xpath(Element.supplier_ISA_IDs_path)
        for self.supplier_ISA_ID in self.supplier_ISA_IDs:
            self.supplier_ISA_IDs_list.append(self.supplier_ISA_ID.text)

        self.supplier_Group_IDs_list = []
        self.supplier_Group_IDs = self.driver.find_elements_by_xpath(Element.supplier_Group_IDs_path)
        for self.supplier_Group_ID in self.supplier_Group_IDs:
            self.supplier_Group_IDs_list.append(self.supplier_Group_ID.text)

        self.retailer_ISA_IDs_list = []
        self.retailer_ISA_IDs = self.driver.find_elements_by_xpath(Element.retailer_ISA_IDs_path)
        for self.retailer_ISA_ID in self.retailer_ISA_IDs:
            self.retailer_ISA_IDs_list.append(self.retailer_ISA_ID.text)

        self.retailer_Group_IDs_list = []
        self.retailer_Group_IDs = self.driver.find_elements_by_xpath(Element.retailer_Group_IDs_path)
        for self.retailer_Group_ID in self.retailer_Group_IDs:
            self.retailer_Group_IDs_list.append(self.retailer_Group_ID.text)

        self.sender_TPID_list = []
        self.sender_TPID = self.driver.find_elements_by_xpath(Element.sender_TPID)
        for self.sender_TPID_name in self.sender_TPID:
            self.sender_TPID_list.append(self.sender_TPID_name.text)

        self.receiver_profile_ID_list = []
        self.receiver_profile_IDs = self.driver.find_elements_by_xpath(Element.receiver_profile_ID)
        for self.receiver_profile_ID in self.receiver_profile_IDs:
            self.receiver_profile_ID_list.append(self.receiver_profile_ID.text)

    def SaveIDs(self):
        self.ExtractIDs()

        self.df_IDs['Supplier ISA ID'] = self.supplier_ISA_IDs_list
        self.df_IDs['Supplier Group ID'] = self.supplier_Group_IDs_list
        self.df_IDs['Retailer ISA ID'] = self.retailer_ISA_IDs_list
        self.df_IDs['Retailer Group ID'] = self.retailer_Group_IDs_list
        self.df_IDs['Sender TPID'] = self.sender_TPID_list
        self.df_IDs['Receiver Profile ID'] = self.receiver_profile_ID_list

        profile_click = self.Setup_IDs_validator()
        self.seleniumOperation.click_element_by_xpath(f".//*[contains(text(),'{str(profile_click)}')]")

    def Setup_IDs_validator(self):
        self.log.log_to_file(self, "INFO", " Setup_IDs_validation in Receiver Side ! ")

        supplier_ISA_id = self.input_file.at[0, 'Supplier ISA ID']
        supplier_group_id = self.input_file.at[0, 'Supplier Group ID']
        retailer_ISA_id = self.input_file.at[0, 'Retailer ISA ID']
        retailer_group_id = self.input_file.at[0, 'Retailer Group ID']

        self.df_IDs = self.df_IDs.loc[(self.df_IDs['Supplier ISA ID'] == str(supplier_ISA_id)) &
                                      (self.df_IDs['Supplier Group ID'] == str(supplier_group_id))]
        print(self.df_IDs)
        if self.df_IDs.empty:
            print("Supplier ISA ID and Group ID is not Matched")
        else:
            print("Supplier ISA ID and Group ID is Matched")
            pass

        self.df_IDs = self.df_IDs.loc[(self.df_IDs['Retailer ISA ID'] == str(retailer_ISA_id))]

        print(self.df_IDs)
        if self.df_IDs.empty:
            print("Retailer ISA ID and Group ID is not Matched")
        else:
            print("Retailer ISA ID and Group ID is Matched")
            pass

        self.df_IDs = self.df_IDs.loc[(self.df_IDs['Sender TPID'].str.contains("ALL", "850"))]
        try:
            self.df_IDs = self.df_IDs[~self.df_IDs['Sender TPID'].str.contains("TNC", na=False)]
            self.df_IDs = self.df_IDs[~self.df_IDs['Sender TPID'].str.contains("TnC", na=False)]
        except:
            pass
        print(self.df_IDs)
        if self.df_IDs.empty:
            print(" Sender TPID is not Matched")
        else:
            print("Sender TPID is Matched")
            profileID = self.df_IDs['Receiver Profile ID'].iloc[0]
            return profileID
            pass

    def Extensions_validation(self):
        self.log.log_to_file(self, "INFO", " Start Extension_validation in Receiver Side ! ")

        self.extension = pandas.read_excel(Element.Extention_File_Path, sheet_name="Sheet1")
        self.extension = self.extension[self.extension.Extensions.str.contains('MapExtension')]
        self.extension['Extensions'] = self.extension['Extensions'].str.split(' ').str[1]
        if self.extension['Extensions'].str.contains('split').any() == True:
            self.splitter = ExcelOperations.get_value(file.Output_File_Path,5,2)
            # print(self.splitter)
            if self.splitter == True:
                print("Splitter Map is present")
                self.log.log_to_file(self, "INFO", " Splitter Map is present in Receiver Side ! ")
                # ExcelOperations.set_value_to_cell(file.Output_File_Path, 5, 2, 'TRUE')
                # setup_methods.Warning(self, 'cancel', 'Splitter Map is present')
        else:
            if self.splitter == True:
                print("Splitter Map is not There")
                self.log.log_to_file(self, "INFO", " Splitter Map is NOT present in Receiver Side ! ")
                # ExcelOperations.set_value_to_cell(file.Output_File_Path, 5, 2, 'FALSE')
                setup_methods.Warning(self, 'cancel', 'SDQ Segment is there but Splitter Map is not There !')
        self.extension = self.extension[self.extension.Extensions.str.contains('conversion')]
        print(self.extension)
        # extension = self.extension.values.tolist()
        # print(extension)

    def retailer_version_extraction(self):
        self.log.log_to_file(self, "INFO", " Start Extracting Retailer_version in Receiver Side ! ")
        time.sleep(4)
        self.doctype_list = []
        self.doctypes = self.driver.find_elements_by_xpath(Element.doctype_click)
        for self.doctype in self.doctypes:
            self.doctype_list.append(self.doctype.text)

        self.service_list = []
        self.services = self.driver.find_elements_by_xpath(Element.service_click)
        for self.service in self.services:
            self.service_list.append(self.service.text)

        self.Datatype_version_list = []
        self.versions = self.driver.find_elements_by_xpath(Element.version_click)
        for self.version in self.versions:
            self.Datatype_version_list.append(self.version.text)

        self.df_retailer_version['Doctype'] = self.doctype_list
        self.df_retailer_version['Service'] = self.service_list
        self.df_retailer_version['Version'] = self.Datatype_version_list

        self.df_retailer_version = self.df_retailer_version.loc[(self.df_retailer_version['Doctype'] == "850") &
                                                                (self.df_retailer_version['Service'] != "DoNotRoute")]
        print(self.df_retailer_version)
        retailer_version = self.df_retailer_version['Version'].iloc[0]
        print(retailer_version)

    def map_extension_validation(self):
        self.log.log_to_file(self, "INFO", " Map Extension Validation in Receiver Side ! ")
        self.Map_sheet = pandas.read_excel(Element.INPUT_FILE_PATH, sheet_name='850 maps')
        self.Map_sheet = self.Map_sheet.loc[(self.Map_sheet['Supplier'] == float('7.6')) & (self.Map_sheet['Retailer'] == float('7'))]
        # print(self.Map_sheet['Map'].iloc[0])
        self.Map_sheet = (self.Map_sheet.set_index(self.Map_sheet.columns.drop('Map', 1).tolist()).Map.str.
                         split(',',expand=True).stack().reset_index().rename(columns={0: 'Map'}).loc[:, self.Map_sheet.columns])
        # print(Map_sheet)
        self.Map_sheet = self.Map_sheet['Map']
        self.df_Map = pandas.DataFrame(columns=['Extensions'])
        self.df_Map['Extensions'] = self.Map_sheet
        print(self.df_Map)

        if self.df_Map.equals(self.extension):
            print("Matched")
            ExcelOperations.set_value_to_cell(file.Output_File_Path, 10, 2, 'MATCHED')
            ExcelOperations.set_value_to_cell(file.Output_File_Path, 6, 2, 'PASS')
            setup_methods.Warning(self,'cancel','Map Extension is Matched')
        else:
            print("Not Matched.")
            ExcelOperations.set_value_to_cell(file.Output_File_Path, 10, 2, 'NOT MATCHED')
            ExcelOperations.set_value_to_cell(file.Output_File_Path, 6, 2, 'FAIL')
            setup_methods.Warning(self, 'cancel', 'Map Extension is Not Matched')




