import pandas as  pd
import logging
import os
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("csv_handler_v2.log"),
        logging.StreamHandler()
    ]
)

class CSVHandler:
    def __init__(self,file_path="ok.csv"):
        self.file_path=file_path
        logging.info(f"CSVHandler initialized with file path: {self.file_path}")

        
    def save_to_csv(self,data):
        try:
            data=pd.DataFrame(data)
            data.to_csv(self.file_path,index=False,mode='a',header=False)
            logging.info(f"Data appended to existing file: {self.file_path}")

        except Exception as e:
            logging.error(f"Error occuring while storing data to {self.file_path}",exc_info=True)
            
        