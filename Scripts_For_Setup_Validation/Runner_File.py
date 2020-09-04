from Scripts_For_Setup_Validation.Execute_Main import Execute_Main
from Scripts_For_Setup_Validation import Main as Main

# Parcel or EDI Validation
Execute = Main.Main_Executor()
Execute.Execute_GenerateInputs()

# SetUp Validation
# star_Execute_Main = Execute_Main()
# star_Execute_Main.start_purchaseOrder_setup_validation()

# FTP File Processing / Upload
Execute.Execute_FTP_Upload()

# FTP File Processing / Downloading
Execute.Accept_Parecl_validation()




