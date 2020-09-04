# Login_Link
login_link = "https://commerce.spscommerce.com/auth/login/"

# Common Constants
INPUT_FILE_PATH = "../AppResources/InputFile_For_PurchaseOrder_Setup.xlsx"
Extention_File_Path = "../Scripts_For_Setup_Validation/extension.xlsx"
Login_Email_Xpath = "//input[@type='email' and @name = 'username']"
Login_Password_Xpath = "//input[@type='password' and @name = 'password']"
Login_Button = "//button[@test='login-button']"

# Login Credentials
Launchpad_username = "achoudhary@spscommerce.com"
Launchpad_password = "XIP/2161ml"

# Setup_Methods
Nexus_tile = "//span[contains(text(),'Nexus')]"
Dropdown_selector = "//span[@class='sps-select__value'][contains(text(),'Production')]"
Pre_Production_selctor = "//span[contains(text(),'Pre-Production')]"
Network = "//*[contains(text(),'Network')]"
relationships_tab = "//button[contains(text(), 'Relationships')]"
advance_search = "//button[span]"
sender_search_selcetor = "//input[@name='search-adv-search-sender_profile_company_name__contains_ic']/following::span[@class='sps-select__value'][contains(text(), 'IN')][1]"
sender_exact_match = "//input[@name='search-adv-search-sender_profile_company_name__contains_ic']/following::*[contains(text(), 'EXACT MATCH')][1]"
sender_name_box = "//input[@name='search-adv-search-sender_profile_company_name__eq_ic']"
receiver_search_selecetor = "//input[@name='search-adv-search-receiver_profile_company_name__contains_ic']/following::span[@class='sps-select__value'][contains(text(), 'IN')][1]"
receiver_exact_match = "//input[@name='search-adv-search-receiver_profile_company_name__contains_ic']/following::*[contains(text(), 'EXACT MATCH')][1]"
receiver_name_box = "//input[@name='search-adv-search-receiver_profile_company_name__eq_ic']"
# sender_search_selcetor = "//span[@class='sps-select__value'][contains(text(), 'IN')]"
# exact_match = "//div[@class='sps-option-list__option-caption'][contains(text(), 'EXACT MATCH')]"
# search_company = "//input[@type='text' and @placeholder='Search']"
# search_button = "//i[@class='sps-icon sps-icon-search' and @aria-hidden='true']"
search_click = "//button[contains(text(),'Search')]"
toggle_compact_view = "//i[@class='sps-icon sps-icon-list-table'and @aria-hidden='true']"
supplier_ISA_IDs_path = "//td[11]/a[@title='Connections' and @style='text-decoration: none;']"
supplier_Group_IDs_path = "//td[13]/a[@title='Connections' and @style='text-decoration: none;']"
retailer_ISA_IDs_path = "//td[14]/a[@title='Connections' and @style='text-decoration: none;']"
retailer_Group_IDs_path = "//td[16]/a[@title='Connections' and @style='text-decoration: none;']"
sender_TPID = "//td[9][@class='sps-table__cell']"
sender_profile_ID = "//td[5]/a[@title='Profile Details' and @style='text-decoration: none;']"
receiver_profile_ID = "//td[7]/a[@title='Profile Details' and @style='text-decoration: none;']"
relationionship_navigation_buttons = "//div[@class='sps-pagination__navigation-buttons']"
relationship_next_button = "//button[@title='Next']"
relationship_next_button_disabled = "//button[@title='Next' and @disabled]"
datatype_click = "//td[14][@class='sps-table__cell']"
service_double_click = '//*[@id="root"]/div[1]/div/div[2]/div/div[4]/div[2]/div/div[3]/div[3]/table/thead/tr/th[8]/div'
service_click = "//td[8][@class='sps-table__cell']"
doctype_click = "//td[4][@class='sps-table__cell']"
version_click = "//td[15][@class='sps-table__cell']"
# extension_click = "//td[6][@class='sps-table__cell']"
extension_click =".//*[contains(@class,'Extensions_contentRow__20CQ8')]"
capid = "//td[7]/a[@title='Capability Details' and @style='text-decoration: none;']"
comms_plus = ".//*[contains(text(),'Create Comms Config')]/preceding::*[5]/following::*[contains(text(),'filebroker')]/preceding::*[2]"
output_channel = ".//*[contains(@class,'sps-description-list__term')]/following::*[contains(@class,'sps-description-list__definition')][9]"
parameters = ".//*[contains(text(),'Name')]/following::*[contains(@class,'sps-table__row')]"
action_parameters = ".//*[contains(text(),'script_location')]/following::*[1]"

# Extention_Verification
nexus_relation_link = 'https://commerce.spscommerce.com/nexus/preprod/network/relationships/'