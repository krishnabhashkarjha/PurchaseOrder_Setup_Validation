
import logging
import datetime
import os
from Utilites import AppConstants
from datetime import date



class LogFileUtility:
    def __init__(self, task_type):
        self.currentDate = datetime.datetime.today().strftime('%d-%m-%Y')
        if os.path.isdir(AppConstants.LOG_FILE_BASE_PATH+"/"+self.currentDate):
            self.log_file_path = AppConstants.LOG_FILE_BASE_PATH + "/" + self.currentDate + "/" + "task_type" + ".log"
        else:
            os.makedirs(AppConstants.LOG_FILE_BASE_PATH + "/" + self.currentDate)
            self.log_file_path = AppConstants.LOG_FILE_BASE_PATH +"/"+self.currentDate +"/"+"task_type"+".log"
        logging.basicConfig(filename=self.log_file_path,format='%(asctime)s %(levelname)s: %(message)s',level = logging.INFO)

    def LogFolderCheck(self):
        self.currentDate = datetime.datetime.today().strftime('%d-%m-%Y')
        if os.path.isdir(AppConstants.LOG_FILE_BASE_PATH + "/" + self.currentDate):
            self.log_file_path = AppConstants.LOG_FILE_BASE_PATH + "/" + self.currentDate + "/" + "task_type" + ".log"
        else:
            os.makedirs(AppConstants.LOG_FILE_BASE_PATH + "/" + self.currentDate)
            self.log_file_path = AppConstants.LOG_FILE_BASE_PATH + "/" + self.currentDate + "/" + "task_type" + ".log"
        logging.basicConfig(filename=self.log_file_path, format='%(asctime)s %(levelname)s: %(message)s',
                            level=logging.INFO)
    def log_to_file(self, messageType, message):
        LogFileUtility.LogFolderCheck(self)
        if messageType == "ERROR":
            logging.error(message)
        elif messageType == "INFO":
            logging.info(message)


