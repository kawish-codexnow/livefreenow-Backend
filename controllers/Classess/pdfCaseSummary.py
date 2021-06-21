from controllers.Classess import MongoDB_Json
from controllers.Classess.Config import Configuration
import pandas as pd

class pdfCaseSummary:

    def __init__(self):
        self.name = "pdfCaseSummary"
        self.ip = Configuration().GetData()['PrivateIp']
        self.port = Configuration().GetData()['MongoPort']
        self.mongoObj = MongoDB_Json.MongoDB()
        self.mongoObj.ConnectMongo(self.ip, self.port, "IMR_DATA")


    def get_all_case_no(self):
        try:
            values = self.mongoObj.read_all_data_column("case_numbers","case_number")
            df = pd.DataFrame(list(values))
            return {"msg":list(df["case_number"]),"status":"True"}
        except Exception as e:
            return {"msg": e.__str__(), "status": "False"}


    def fetch_case_data(self,case_number):
        try:
            values = self.mongoObj.read_value("pdf_data_records","case_number",case_number)
            if values !=None:
                del values["_id"]
                return {"msg":values,"status":"True"}
            else:
                return {"msg": "Invalid Case Number", "status": "False"}
        except Exception as e:
            return {"msg": e.__str__(), "status": "False"}
