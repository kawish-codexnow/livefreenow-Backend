import pandas as pd
from controllers.Classess.Config import Configuration
from controllers.Classess.MongoDB_Json import MongoDB
from controllers.Classess.email_scheduler import email_scheduler
import numpy as np
import pickle

class search_portal():

    def __init__(self):

        self.df = pd.read_csv('./iponymData/csvstore/search_portal_data20210611_1.csv')
        self.df.columns = ["Case.#", "Final Determination", "Clinical Summary",
                           "Determination Summary", "Decision Explanation", "Body Part", "Decision", "Date"]
        self.df = self.df.astype(str)
        self.df2 = self.df.copy(deep=True)

        self.apisEndPoint = Configuration().GetData()['apisEndPoint']
        self.ip = Configuration().GetData()['PrivateIp']
        self.port = Configuration().GetData()['MongoPort']
        self.db = Configuration().GetData()['MongoDb']
        self.mongoObj = MongoDB()
        self.mongoObj.ConnectMongo(self.ip, self.port, self.db)

    def search_data_new(self, val_to_search):
        try:
            self.df2 = self.df.copy(deep=True)
            values = []
            case_no = 0
            if 'decision' in val_to_search:
                decision = val_to_search['decision']
                if decision != "all":
                    temp_df = self.df2[self.df2['Decision'].str.contains(decision, case=False)]
                    if len(temp_df) > 0:
                        self.df2 = temp_df
                    else:
                        return {"msg": "Data doesn't exist", "status": "False"}

            if 'body_part' in val_to_search:
                body_part = val_to_search['body_part']
                temp_df = self.df2[self.df2['Body Part'].str.contains(r'\b{0}\b'.format(body_part), case=False)]
                if len(temp_df) > 0:
                    self.df2 = temp_df
                else:
                    values.append(body_part)

            if 'treatment' in val_to_search:
                treatment = val_to_search['treatment']
                values += treatment
            if 'startdate' in val_to_search:
                start_date = val_to_search['startdate']
            if 'enddate' in val_to_search:
                end_date = val_to_search['enddate']

            if 'case_no' in val_to_search:
                case_no = val_to_search['case_no']
            for val in values:
                mask = np.column_stack([self.df2[col].str.contains(r"\b{0}\b".format(val), case=False)
                                        for col in self.df2 if
                                        col != 'Decision' or col != 'Case.#' or col != 'Body Part'])
                temp_df = self.df2.loc[mask]
                if len(temp_df) > 0:
                    self.df2 = self.df2.loc[mask]
                else:
                    print(val)
            self.df2 = self.df2.drop_duplicates()
            #               self.df2 = self.df2[self.df2[column_name].str.contains(r"\b{0}\b".format(val), case=False)]
            if start_date != "" and end_date != "":
                self.df2['Date'] = pd.to_datetime(self.df2['Date'])
                mask = (self.df2['Date'] > start_date) & (self.df2['Date'] <= end_date)
                self.df2 = self.df2.loc[mask]
                outcome_count = len(self.df2)
                requested_count = len(self.df2)

            else:
                self.df2 = self.df2.sort_values(by="Date", key=pd.to_datetime, ascending=False)
                outcome_count = len(self.df2)
                self.df2 = self.df2.head(case_no)
                requested_count = len(self.df2)

            if self.df2.empty:
                return {"msg": "Data doesn't exist", "status": "False"}

            else:
                self.df2["Body Part"] = body_part
                self.df2["Treatment Requested"] = str(treatment)
                self.df2 = self.df2.replace({np.NAN: None})
                self.df2["Date"] = self.df2["Date"].astype(str)
                del self.df2["Determination Summary"]
                del self.df2["Final Determination"]
                self.df2.to_csv("./templates/"+val_to_search["email"]+str(val_to_search["result_code"])+".csv", index=False)
                self.df2.to_excel("./templates/"+val_to_search["email"]+str(val_to_search["result_code"])+".xlsx", index=False, sheet_name='Sheet1', engine='xlsxwriter')
                return_data = self.df2.head(100).to_dict(orient='record')
                return {"msg": return_data, "pdfurl": self.apisEndPoint + val_to_search["email"]+str(val_to_search["result_code"])+".xlsx", "csvurl": self.apisEndPoint + val_to_search["email"]+str(val_to_search["result_code"])+'.csv', "count": requested_count, "case_outcome": outcome_count, "status": "True"}
        except Exception as e:
            return {"msg": e.__str__(), "status": "False"}


    def scheduler_search(self):
        try:
            data = self.mongoObj.read_all_data_with_query("scheduler", {"result": ""})
            for x in data:
                return_data = self.search_data_new(x)
                if return_data["status"] == "True":
                    self.mongoObj.update_value("scheduler", {"email": x["email"], "result_code": x["result_code"], "result": "", "result_status": "", "case_outcome": 0}, {"result": str(return_data), "result_status": "True", "case_outcome": return_data["case_outcome"]})
                else:
                    self.mongoObj.update_value("scheduler", {"email": x["email"], "result_code": x["result_code"], "result": "", "result_status": ""}, {"result": str(return_data), "result_status": "False"})
            return {"msg": "success", "status": "True"}

        except Exception as e:
            return {"msg": e.__str__(), "status": "False"}


    def search_data(self, column_name, val_to_search):
        try:
            if column_name == 'denial_date' or column_name == 'decision' or column_name == 'case_number':
                temp_val = []
                temp_val.append(val_to_search[0])
                val_to_search = temp_val
            for val in val_to_search:
                self.df2 = self.df2[self.df2[column_name].str.contains(r"\b{0}\b".format(val), case=False)]

            return_data = self.df2.head(100).to_dict(orient='record')
            if len(return_data) == 0:
                return {"msg": "Data doesn't exist", "status": "False"}
            else:
                return {"msg": return_data, "count": len(self.df2), "status": "True"}
        except Exception as e:
            return {"msg": e.__str__(), "status": "False"}


    def get_column_names(self):
        try:
            return {"msg": list(self.df.columns), "status": "True"}
        except Exception as e:
            return {"msg": e.__str__(), "status": "False"}

    def reset_data(self):
        try:
            self.df2 = self.df.copy(deep=True)
            return {"msg": self.df2.head(100).to_dict(orient='record'), "status": "True"}
        except Exception as e:
            return {"msg": e.__str__(), "status": "False"}

    def reset_list(self):
        try:
            df = pd.read_excel("controllers/Classess/IMR Decisions Searchable.xls")
            body_parts = df["Body Part"].unique().tolist()
            body_parts = [x for x in body_parts if str(x) != 'nan']
            body_parts = [x.strip().lower().split() for x in body_parts]
            body_parts = list(set([item for sublist in body_parts for item in sublist]))

            pickle_in = open("./iponymData/drug_symptoms/drug_list.pickle", "rb")
            drugs = pickle.load(pickle_in)

            pickle_in = open("controllers/Classess/diseases_treatment.pickle", "rb")
            example_dict = pickle.load(pickle_in)
            treatments = []
            for k, v in example_dict.items():
                treatments += v

            drugs = [x for x in drugs if str(x) != 'nan']
            treatments = [x for x in treatments if str(x) != 'nan']
            servies = []
            self.mongoObj.drop_collection("filter_lists")
            self.mongoObj.write_value("filter_lists",
                                      {"body_parts": body_parts, "drugs": drugs, "treatments": treatments,
                                       "servies": servies, "key": "12345"})
            return {"msg": "reset lists successfully", "status": "True"}

        except Exception as e:
            return {"msg": e.__str__(), "status": "False"}

    def get_list(self):
        try:
            data = list(self.mongoObj.read_all_data("filter_lists"))[0]
            data.pop('_id', None)
            data.pop('key', None)
            return {"msg": data, "status": "True"}

        except Exception as e:
            return {"msg": e.__str__(), "status": "False"}

    def apply_search(self, dic):
        try:
            scheduler_status = email_scheduler().update_scheduler(dic)
            # send notification email
            if scheduler_status["status"] == "True":
                email_status = email_scheduler().send_notifcation_email(scheduler_status["result_code"], dic)
            else:
                return scheduler_status
            # update filter lists
            if email_status["status"] == "True":
                self.mongoObj.push_value_in_list("filter_lists", dic)
                return email_status
            else:
                return email_status

        except Exception as e:
            return {"msg": e.__str__(), "status": "False"}


    def get_result(self, result_code):
        try:
            return email_scheduler().get_result(result_code)

        except Exception as e:
            return {"msg": e.__str__(), "status": "False"}
