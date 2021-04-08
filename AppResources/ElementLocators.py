INPUT_FILE_PATH = "../AppResources/InputFile.xlsx"
Output_File_Path = "../AppResources/OutPut.xlsx"

#Launchpad login
Login_Email = "//input[@type='email' and @id='username']"

Login_Password_Xpath = "//input[@type='password' and @id='password']"

Sign_in_button = "//span[contains(text(),'Sign In')]"

#TT Production
COMPANY_SEARCH_INPUTBOX=".//*[@id='advanced_search_dropdown']/div[1]/div/div[1]/div[2]/div[1]/div/companies-chosen-select/div/ul/li/input"
TRADING_SEARCH_INPUTBOX= ".//*[@id='advanced_search_dropdown']/div[1]/div/div[1]/div[2]/div[3]/div/trading-partner-chosen-select/div/ul/li/input"

Select_company_total_path = ".//*[contains(text(), 'Lowes')]/..//..//div[not(contains(text(),' '))]"
Select_company_Part1 = ".//*[contains(text(), '"
Select_company_Part2 = "')]/..//..//div[not(contains(text(),' '))]"

Select_tradingpartner_Part1 = ".//*[text()='"
Select_tradingpartner_Part2 = "']"
TT_url = 'https://commerce.spscommerce.com/transaction-tracker/preprod/transactions/'
Status_dropdown = ".//*[text()='Status']/..//*[text()='Any']"
Status_Accepted = ".//*[text()='Accepted']"
TT_Search = ".//*[@class = 'sps-btn sps-btn--key'][contains(text(), 'Search')]"
parcels_ids = ".//*[@class='sps-table__cell']/..//*[@ng-bind='transaction.parcel_uid']"

Input_Download_selector ="(.//*[@class='sps-icon sps-icon-ellipses']['::before'])[1]"
Input_Download = "(.//*[@class='sps-icon sps-icon-download-cloud']['::before'])[1]"
Get_TPID = ".//*[contains(text(), 'TradingPartnerId')]"

#FTP pre-prod Upload
ftp_username =
ftp_username_path = "//input[@id='username']"
ftp_password_path = "//input[@id='password']"
Remember_Me_path = ".//*[contains(text(), 'Remember Me')]"
ftp_login = "//span[@id='LoginButtonText'][contains(text(), 'Login')]"
ftp_folder = "//a[contains(text(), 'ftp')]"
FTP_PREPROD_LINK = "https://commshare.spspreprod.in/#/ftp/inbound_edi/"
#FTP_add_file = ".//*[contains(@id,'browseFileButtonPanel')]"
FTP_add_file = ".//*[contains(@id,'browseFileButtonPanel')]//input[@type='file']"
FTP_Refresh = ".//*[contains(@title,'Refresh')]"
btn_upload = "//button/..//*[text()='Upload']"

plus_click = ".//*[contains(text(),'FItoService')]/preceding::*[8]"
file_url = ".//*[contains(text(),'File Name')]/following::*[1]"
