import time
import pandas
import tkinter as tk
import numpy
from tkinter import messagebox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilites.ExcelOperations import ExcelOperations
from AppResources import ElementLocator_For_PurchaseOrder_SetUp as Element
from AppResources import ElementLocators as file
from openpyxl.styles import PatternFill


class setup_methods:

    def __init__(self, driver, log, seleniumOperation):
        self.df_IDs = pandas.DataFrame(
            columns=['Supplier ISA ID', 'Supplier Group ID', 'Retailer ISA ID', 'Retailer Group ID', 'Sender TPID',
                     'Sender Profile ID'], dtype=object)
        self.df_datatypes = pandas.DataFrame(columns=['DataTypes','Version', 'Doctype', 'Service', 'CapId'])
        self.df_extension = pandas.DataFrame(columns=['Extensions'],dtype=object)
        self.input_file = pandas.read_excel(Element.INPUT_FILE_PATH, sheet_name='Nexus_Input')
        self.supplier_name = self.input_file.at[0, 'Supplier Name']
        self.retailer_name = self.input_file.at[0, 'Retailer Name']
        self.ERP_name = self.input_file.at[0, 'ERP']
        self.ERP_sheet = pandas.read_excel(Element.INPUT_FILE_PATH, sheet_name="ERP", dtype=object)
        self.driver = driver
        self.log = log
        self.seleniumOperation = seleniumOperation
        self.wait = WebDriverWait(self.driver, 10)

    def Warning(self, type, message):
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        if type == "cancel":
            user_choice = messagebox.askokcancel(f"User Alert", message, parent=root)
            if not user_choice:
                self.driver.close()
        elif type == "warning":
            messagebox.showwarning(f"User Alert", {message}, parent=root)

    def Login(self):
        try:
            print("In Login.")
            self.driver.get(Element.login_link)
            self.wait.until(EC.frame_to_be_available_and_switch_to_it(0))
            self.seleniumOperation.send_text_by_xpath(Element.Login_Email_Xpath, Element.Launchpad_username)
            self.seleniumOperation.send_text_by_xpath(Element.Login_Password_Xpath, Element.Launchpad_password)
            time.sleep(2)
            self.seleniumOperation.click_element_by_xpath(Element.Login_Button)
        except Exception as e:
            self.log.log_to_file(self, "ERROR", "Error in Login." + str(e))

    def Nexus(self):
        try:
            print("In Nexus to Starting Nexus.")
            self.log.log_to_file(self, "INFO", " In Nexus to Starting Nexus! ")
            self.wait.until(EC.frame_to_be_available_and_switch_to_it(0))
            self.seleniumOperation.click_element_by_xpath(Element.Nexus_tile)
            self.wait.until(EC.frame_to_be_available_and_switch_to_it(0))
            self.seleniumOperation.click_element_by_xpath(Element.Dropdown_selector)
            self.seleniumOperation.click_element_by_xpath(Element.Pre_Production_selctor)
        except Exception as e:
            self.log.log_to_file(self, "ERROR", "Error in Nexus Method." + str(e))

    def search_relationships(self):
        self.log.log_to_file(self, "INFO", " Starting searching for Relationshilp in Supplier Side! ")
        self.seleniumOperation.click_element_by_xpath(Element.Network)
        self.seleniumOperation.click_element_by_xpath(Element.relationships_tab)
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
        self.seleniumOperation.click_element_by_xpath(Element.toggle_compact_view)

    def ExtractIDs(self):
        time.sleep(4)
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

        self.sender_profile_ID_list = []
        self.sender_profile_IDs = self.driver.find_elements_by_xpath(Element.sender_profile_ID)
        for self.sender_profile_ID in self.sender_profile_IDs:
            self.sender_profile_ID_list.append(self.sender_profile_ID.text)

    def SaveIDs(self):
        self.ExtractIDs()

        self.df_IDs['Supplier ISA ID'] = self.supplier_ISA_IDs_list
        self.df_IDs['Supplier Group ID'] = self.supplier_Group_IDs_list
        self.df_IDs['Retailer ISA ID'] = self.retailer_ISA_IDs_list
        self.df_IDs['Retailer Group ID'] = self.retailer_Group_IDs_list
        self.df_IDs['Sender TPID'] = self.sender_TPID_list
        self.df_IDs['Sender Profile ID'] = self.sender_profile_ID_list

        profile_click = self.Setup_IDs_validator()
        self.seleniumOperation.click_element_by_xpath(f".//*[contains(text(),'{str(profile_click)}')]")

    def Setup_IDs_validator(self):
        self.log.log_to_file(self, "INFO", " Starting Setup_ID_validation in Supplier Side! ")
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

        self.df_IDs = self.df_IDs.loc[(self.df_IDs['Retailer ISA ID'] == str(retailer_ISA_id))]  # &
        # (self.df_IDs['Retailer Group ID'] == str(retailer_group_id))]
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
            profileID = self.df_IDs['Sender Profile ID'].iloc[0]
            return profileID
            pass

    def Extract_capability(self):
        time.sleep(4)
        self.datatype_list = []
        self.datatypes = self.driver.find_elements_by_xpath(Element.datatype_click)
        for self.datatype in self.datatypes:
            self.datatype_list.append(self.datatype.text)

        self.version_list = []
        self.versions = self.driver.find_elements_by_xpath(Element.version_click)
        for self.version in self.versions:
            self.version_list.append(self.version.text)

        self.doctype_list = []
        self.doctypes = self.driver.find_elements_by_xpath(Element.doctype_click)
        for self.doctype in self.doctypes:
            self.doctype_list.append(self.doctype.text)

        self.service_list = []
        self.services = self.driver.find_elements_by_xpath(Element.service_click)
        for self.service in self.services:
            self.service_list.append(self.service.text)

        self.capId_list = []
        self.capIds = self.driver.find_elements_by_xpath(Element.capid)
        for self.capId in self.capIds:
            self.capId_list.append(self.capId.text)


    def Save_capability(self):
        self.Extract_capability()

        self.df_datatypes['DataTypes'] = self.datatype_list
        self.df_datatypes['Version'] = self.version_list
        self.df_datatypes['Service'] = self.service_list
        self.df_datatypes['Doctype'] = self.doctype_list
        self.df_datatypes['CapId'] = self.capId_list

        self.Setup_capability_validator()
        return

    def Setup_capability_validator(self):
        self.log.log_to_file(self, "INFO", " Starting Setup capability validation in Supplier Side! ")
        self.ERP_sheet = self.ERP_sheet.loc[(self.ERP_sheet['ERP'] == self.ERP_name)]
        datatype_name = self.ERP_sheet['DataTypeName'].iloc[0]
        service_name = self.ERP_sheet['Services'].iloc[0]
        doctype_name = self.ERP_sheet['Document'].iloc[0]
        # ExcelOperations.set_value_to_cell(file.Output_File_Path,1,2,doctype_name)
        # status = "ACTIVE"

        self.df_datatypes = self.df_datatypes.loc[(self.df_datatypes['Service'] == str(service_name)) &
                                                  (self.df_datatypes['Doctype'] == str(doctype_name))]
        print(self.df_datatypes)
        if self.df_datatypes.empty:
            print("Capability service and Doctype is not Matched")
            ExcelOperations.set_value_to_cell(file.Output_File_Path, 1, 2,'NOT MATCHED')
        else:
            print("Capability service and Doctype is Matched")
            ExcelOperations.set_value_to_cell(file.Output_File_Path, 1, 2, 'MATCHED')
            pass

        self.df_datatypes_test = self.df_datatypes.loc[(self.df_datatypes['DataTypes'] == str(datatype_name))]
        # ExcelOperations.set_value_to_cell(file.Output_File_Path, 3, 2, self.df_datatypes['DataTypes'])
        if self.df_datatypes_test.empty:
            print(self.df_datatypes_test)
            print("Capability datatype is not Matched")
            ExcelOperations.set_value_to_cell(file.Output_File_Path, 3, 2,'NOT MATCHED')
            time.sleep(5)
            data_type = self.df_datatypes['DataTypes'].iloc[0]
            self.CapID = self.df_datatypes['CapId'].iloc[0]
            self.Warning("cancel", str(f" This Datatype {data_type} is not MATCHED with input Datatype you want to "
                                       f"continue with DOCUMENT type and SERVICE"))
            self.extreact_extension()
            self.seleniumOperation.click_element_by_xpath(f".//*[contains(text(),'{str(self.CapID)}')]")
            pass
        else:
            print(self.df_datatypes_test)
            print("Capability datatype is Matched")
            ExcelOperations.set_value_to_cell(file.Output_File_Path, 3, 2, 'MATCHED')
            self.CapID = self.df_datatypes_test['CapId'].iloc[0]
            self.extreact_extension()
            self.seleniumOperation.click_element_by_xpath(f".//*[contains(text(),'{str(self.CapID)}')]")
            pass

    def extreact_extension(self):
        self.seleniumOperation.click_element_by_xpath(f".//*[contains(text(),'{str(self.CapID)}')]/preceding::*[14]")
        time.sleep(10)
        self.extension_list = []
        self.extensions = self.driver.find_elements_by_xpath(Element.extension_click)
        for self.extension in self.extensions:
            self.extension_list.append(self.extension.text)
        # print(self.extension_list)
        self.df_extension['Extensions'] = self.extension_list
        print(self.df_extension)
        self.df_extension.to_excel('extension.xlsx',index=False)
        time.sleep(5)

    def Capability_parameter_validator(self):
        self.log.log_to_file(self, "INFO", " Validating Capability Parameters in Supplier Side! ")
        time.sleep(4)
        self.seleniumOperation.click_element_by_xpath(Element.comms_plus)
        self.output_channel_list = []
        self.output_channels = self.driver.find_elements_by_xpath(Element.output_channel)
        for self.output_channel in self.output_channels:
            self.output_channel_list.append(self.output_channel.text)
        # print(self.output_channel_list)
        if (self.output_channel_list.__getitem__(0) == self.ERP_sheet['filename_macro'].iloc[0] and
                self.output_channel_list.__getitem__(2).split('/').__getitem__(6) == "out" and
                self.output_channel_list.__getitem__(3).split('/').__getitem__(5) == "out"):
            print("filename_macro, archive_directory, and directory is Matched")
            ExcelOperations.set_value_to_cell(file.Output_File_Path, 4, 2, 'MATCHED')
        else:
            self.Warning('cancel', "filename_macro/ archive_directory/ directory is Not Matched")
            ExcelOperations.set_value_to_cell(file.Output_File_Path, 4, 2, 'NOT MATCHED')

    def Get_parameters(self):
        self.log.log_to_file(self, "INFO", " Geting parameters in Supplier Side! ")
        time.sleep(3)
        self.parameters_list = []
        self.parameters = self.driver.find_elements_by_xpath(Element.parameters)
        for self.parameter in self.parameters:
            self.parameters_list.append(self.parameter.text)
        self.df_parameter = pandas.DataFrame(columns=['parameters'])
        self.df_parameter['parameters'] = self.parameters_list
        # print(self.df_parameter)
        self.df_parameter = self.df_parameter.iloc[1:, :]
        self.df_parameter['parameters'] = self.df_parameter['parameters'].str.split('\n').str[0]
        self.df_parameter.rename(columns={'parameters': 'NAME'}, inplace=True)
        indexes_to_be_removed = self.df_parameter.loc[self.df_parameter['NAME'] == "ID"].index[0]
        self.df_parameter = self.df_parameter.iloc[:indexes_to_be_removed - 1, :]
        self.df_parameter = pandas.DataFrame(self.df_parameter.NAME.str.split(' ', 1).tolist(),
                                             columns=['NAME', 'VALUE'])
        print(self.df_parameter)
        print("_____________________________________________________________________________")
        try:
            if numpy.isnan(self.ERP_sheet.WRAPDOCUMENT.iloc[0]):
                print('WRAPDOCUMENT not applicable')
        except:
            if self.ERP_sheet.WRAPDOCUMENT.iloc[0] == \
                    self.df_parameter.loc[self.df_parameter['NAME'] == 'WRAPDOCUMENT', 'VALUE'].iloc[0]:
                print('WRAPDOCUMENT value matched')
            else:
                self.Warning('cancel', 'Warning!! WRAPDOCUMENT value does not match, do you want to continue ?')

        try:
            if numpy.isnan(self.ERP_sheet.WRAPTRAILER.iloc[0]):
                print('WRAPTRAILER not applicable')
        except:
            if self.ERP_sheet.WRAPTRAILER.iloc[0] == \
                    self.df_parameter.loc[self.df_parameter['NAME'] == 'WRAPTRAILER', 'VALUE'].iloc[0]:
                print('WRAPTRAILER value matched')
            else:
                self.Warning('cancel', 'Warning!! WRAPTRAILER value does not match, do you want to continue ?')

        try:
            if numpy.isnan(self.ERP_sheet.WRAPHEADER.iloc[0]):
                print('WRAPHEADER not applicable')
        except:
            if self.ERP_sheet.WRAPHEADER.iloc[0] == \
                    self.df_parameter.loc[self.df_parameter['NAME'] == 'WRAPHEADER', 'VALUE'].iloc[0]:
                print('WRAPHEADER value matched')
            else:
                self.Warning('cancel', 'Warning!! WRAPHEADER value does not match, do you want to continue ?')
        print("_____________________________________________________________________________")
        try:
            self.action_parameters_list = []
            self.action_parameters = self.driver.find_elements_by_xpath(Element.action_parameters)
            for self.action_parameter in self.action_parameters:
                self.action_parameters_list.append(self.action_parameter.text)

            try:
                if numpy.isnan(self.ERP_sheet['PearlScriptAction'].iloc[0]):
                    print("PearlScriptAction is not applicable")
                    ExcelOperations.set_value_to_cell(file.Output_File_Path, 8, 2, 'NOT MATCHED')
            except:
                if self.action_parameters_list[0] == self.ERP_sheet['PearlScriptAction'].iloc[0]:
                    print("PearlScriptAction is Matched")
                    ExcelOperations.set_value_to_cell(file.Output_File_Path, 8, 2, 'MATCHED')
                else:
                    self.Warning('cancel', "Warning!! PearlScriptAction is not Matched")

            try:
                if numpy.isnan(self.ERP_sheet['NamingScriptAction'].iloc[0]):
                    print("NamingScriptAction is not applicable")
                    ExcelOperations.set_value_to_cell(file.Output_File_Path, 9, 2, ' NOT MATCHED')
            except:
                if self.action_parameters_list[1] == self.ERP_sheet['NamingScriptAction'].iloc[0]:
                    print("NamingScriptAction is Matched")
                    ExcelOperations.set_value_to_cell(file.Output_File_Path, 9, 2, 'MATCHED')
                else:
                    self.Warning('cancel', "Warning!! NamingScriptAction is not Matched")
        except:
            self.Warning('cancel', "Warning!! PearlScriptAction and NamingScriptAction is not Present !! DO You want "
                                   "to Continue ?")
            pass