from selenium import webdriver
import pandas
from Utilites import AppConstants
from Scripts_For_Setup_Validation.Setup_Methods import setup_methods
from Scripts_For_Setup_Validation.Extention_Verification import Extention_Verification
from Utilites.SeleniumOperations import SeleniumOperations
from Utilites.LogFileUtility import LogFileUtility as lo

class Execute_Main:

    def __init__(self):
        try:
            print("Start Execution.")
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--start-maximized")
            self.driver = webdriver.Chrome(AppConstants.BROWSER_DRIVER, chrome_options=chrome_options)
            self.log = lo
        except Exception as e:
            self.log.log_to_file(self, "ERROR", "NOT able to Connected Scripts.Execute_Main() Constructor" + str(e))

    def start_purchaseOrder_setup_validation(self):
        print("Starting PurchaseOrder Setup Validation.")
        seleniumOperation = SeleniumOperations(self.driver, self.log)

        # Setup_Methods
        setup_method = setup_methods(self.driver,self.log,seleniumOperation)
        setup_method.Login()
        setup_method.Nexus();setup_method.search_relationships();setup_method.SaveIDs()
        setup_method.Save_capability()
        setup_method.Capability_parameter_validator();setup_method.Get_parameters()

        # Extention_Verification
        extention_verification = Extention_Verification(self.driver, self.log, seleniumOperation)
        extention_verification.receiver_search();extention_verification.SaveIDs()
        extention_verification.Extensions_validation();extention_verification.retailer_version_extraction()
        extention_verification.map_extension_validation()

        self.driver.quit()