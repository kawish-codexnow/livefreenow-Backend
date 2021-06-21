from controllers.Classess.Config import Configuration
from controllers.Classess.MongoDB_Json import MongoDB
import datetime
import random
import base64
import ast
import time, os
from email.mime.multipart import MIMEMultipart
import re
from email.mime.text import MIMEText
import smtplib

class email_scheduler:

    def __init__(self):
        self.ip = Configuration().GetData()['PrivateIp']
        self.port = Configuration().GetData()['MongoPort']
        self.db = Configuration().GetData()['MongoDb']
        self.email = Configuration().GetData()['EmailID']
        self.password = Configuration().GetData()['Password']
        self.mongoObj = MongoDB()
        self.mongoObj.ConnectMongo(self.ip, self.port, self.db)
        os.environ['TZ'] = 'Asia/Karachi'
        time.tzset()


    def send_notifcation_email(self, result_code, data):
        try:
            receiver_email = data["email"]
            if re.search(r'[\w.-]+@[\w.-]+.\w+', receiver_email):
                html = None
                if data["startdate"] != "" and data["enddate"] != "":
                    html = """<html> <head> <title>LiveFree | Notification Email</title> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="icon" href="favicon.ico"> <style> @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap'); body { font-family: 'Roboto', sans-serif; } </style> </head> <body> <div class="section" style="padding: 30px 0;width: 100%;margin: auto;"> <table style="max-width: 600px;border-spacing: 0;border-collapse: collapse;table-layout: auto;margin: 0 auto;" cellspacing="0" cellpadding="0" border="0" align="center" width="600"> <tbody> <tr> <th valign="top"> <table width="100%" cellspacing="0" cellpadding="0" border="0" style="margin: 0 auto;border-spacing: 0;border-collapse: collapse;table-layout: auto;background-color: #00334e;text-align: left;"> <tbody> <tr> <td> <a href="#"><img src="https://livefreenow.us/assets/livefreelogo.png" style="height: 50px;padding: 20px;"></a> </td> </tr> </tbody> </table> </th> </tr> <tr> <td> <table width="100%" cellpadding="0" cellspacing="0" style="border-spacing:0;border-collapse:collapse;table-layout:auto;margin:0 auto;background-color: #fff;height: 350px;"> <tbody style="vertical-align: top;"> <tr> <td align="left" style="padding:16px 40px"> <h1>Hello! <span style="color: #00669c;">""" + str(data["doctorname"]) + """</span>,</h1> <h4> Thanks for using LiveFree search portal for all your IMR/Worker's Comp analysis needs. You will get an email as soon as your search requested is completed. </h4> <p style="font-size: 14px;"> Your Search Criterion were: </p> <ul style="font-size: 14px;list-style-type: auto;padding-left: 1rem;"> <li style="padding: 5px 0;font-weight: 600;"> Body Part: <h3 style="margin: 10px 0;font-weight: normal;">""" + str(data["body_part"]) + """</h3> </li> <li style="padding: 5px 0;font-weight: 600;"> Treatment Requested: <h3 style="margin: 10px 0;font-weight: normal;">""" + str(data["treatment"]) + """</h3> </li> <li style="padding: 5px 0;font-weight: 600;"> Requested By Date: <h3 style="margin: 10px 0;font-weight: normal;">Start Date: """ + str(data["startdate"]) + """<br>End Date: """ + str(data["enddate"]) + """</h3> </li> </ul> <p style="font-size: 14px;">Your result is expected in 24 hours.</p> <p style="font-size: 14px;"> Regards, <br> <span style="color: #00669c;font-weight: 600;">LiveFree</span> </p> </td> </tr> </tbody> </table> </td> </tr> <tr> <td> <table width="100%" cellpadding="0" cellspacing="0" style="border-spacing:0;border-collapse:collapse;table-layout:auto;margin:0 auto;background-color: #00334e;color: #FFF;"> <tbody> <tr> <td align="left" style="padding:16px 40px"> <p style="font-size: 13px;line-height: 16px;">If you have any questions, contact us at <a href="mailto:info@livefreenow.us" style="color: #fff;">info@livefreenow.us</a>. </p> <p style="font-size: 13px;line-height: 16px;">© Copyright <a href="https://livefreenow.us" target="_blank" style="color: #fff;">LiveFree</a>. All Rights Reserved</p> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> </div> </body> </html>"""
                else:
                    html = """<html> <head> <title>LiveFree | Notification Email</title> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="icon" href="favicon.ico"> <style> @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap'); body { font-family: 'Roboto', sans-serif; } </style> </head> <body> <div class="section" style="padding: 30px 0;width: 100%;margin: auto;"> <table style="max-width: 600px;border-spacing: 0;border-collapse: collapse;table-layout: auto;margin: 0 auto;" cellspacing="0" cellpadding="0" border="0" align="center" width="600"> <tbody> <tr> <th valign="top"> <table width="100%" cellspacing="0" cellpadding="0" border="0" style="margin: 0 auto;border-spacing: 0;border-collapse: collapse;table-layout: auto;background-color: #00334e;text-align: left;"> <tbody> <tr> <td> <a href="#"><img src="https://livefreenow.us/assets/livefreelogo.png" style="height: 50px;padding: 20px;"></a> </td> </tr> </tbody> </table> </th> </tr> <tr> <td> <table width="100%" cellpadding="0" cellspacing="0" style="border-spacing:0;border-collapse:collapse;table-layout:auto;margin:0 auto;background-color: #fff;height: 350px;"> <tbody style="vertical-align: top;"> <tr> <td align="left" style="padding:16px 40px"> <h1>Hello! <span style="color: #00669c;">""" + str(data["doctorname"]) + """</span>,</h1> <h4> Thanks for using LiveFree search portal for all your IMR/Worker's Comp analysis needs. You will get an email as soon as your search requested is completed. </h4> <p style="font-size: 14px;"> Your Search Criterion were: </p> <ul style="font-size: 14px;list-style-type: auto;padding-left: 1rem;"> <li style="padding: 5px 0;font-weight: 600;"> Body Part: <h3 style="margin: 10px 0;font-weight: normal;">""" + str(data["body_part"]) + """</h3> </li> <li style="padding: 5px 0;font-weight: 600;"> Treatment Requested: <h3 style="margin: 10px 0;font-weight: normal;">""" + str(data["treatment"]) + """</h3> </li> <li style="padding: 5px 0;font-weight: 600;"> Requested By Case Count: <h3 style="margin: 10px 0;font-weight: normal;">Requested Cases: """ + str(data["case_no"]) + """</h3> </li> </ul> <p style="font-size: 14px;">Your result is expected in 24 hours.</p> <p style="font-size: 14px;"> Regards, <br> <span style="color: #00669c;font-weight: 600;">LiveFree</span> </p> </td> </tr> </tbody> </table> </td> </tr> <tr> <td> <table width="100%" cellpadding="0" cellspacing="0" style="border-spacing:0;border-collapse:collapse;table-layout:auto;margin:0 auto;background-color: #00334e;color: #FFF;"> <tbody> <tr> <td align="left" style="padding:16px 40px"> <p style="font-size: 13px;line-height: 16px;">If you have any questions, contact us at <a href="mailto:info@livefreenow.us" style="color: #fff;">info@livefreenow.us</a>. </p> <p style="font-size: 13px;line-height: 16px;">© Copyright <a href="https://livefreenow.us" target="_blank" style="color: #fff;">LiveFree</a>. All Rights Reserved</p> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> </div> </body> </html>"""

                # Record the MIME types of both parts - text/plain and text/html.
                part = MIMEText(html, 'html')
                # # The mail addresses and password
                sender_address = self.email
                sender_pass = self.password
                receiver_address = receiver_email
                # Setup the MIME
                message = MIMEMultipart()
                message.attach(part)
                message['From'] = sender_address
                message['To'] = receiver_address
                message['Subject'] = 'LiveFree Notification (Result Ref# ' + str(result_code) + ')'  # The subject line
                # Create SMTP session for sending the mail
                session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
                session.starttls()  # enable security
                session.login(sender_address, sender_pass)  # login with mail_id and password
                text = message.as_string()
                session.sendmail(sender_address, receiver_address, text)
                session.quit()
                return {"msg": "please check your email", "status": "True"}
            else:
                return {"msg": "invalid email", "status": "False"}
        except Exception as e:
            return {'msg': str(e), 'status': 'False'}



    def update_scheduler(self, data):
        try:
            request_time = datetime.datetime.now().replace(second=0, microsecond=0)
            send_email_time = (request_time + datetime.timedelta(seconds=10)).replace(second=0, microsecond=0)
            data["request_time"] = request_time
            data["send_email_time"] = send_email_time
            data["result"] = ""
            data["result_status"] = ""
            data["case_outcome"] = 0
            data["result_code"] = random.randint(123456,123456789)
            data["status"] = 0
            data["email_status"] = "pending"
            self.mongoObj.write_value("scheduler",data)
            return {"msg":"scheduler updated", "result_code": data["result_code"],"status":"True"}
        except Exception as e:
            return {"msg": e.__str__(), "status": "False"}


    def get_result(self,result_code):
        try:
            query_data = base64.b64decode((bytes(result_code.replace("~", "="), "utf-8"))).decode("utf-8")
            query_data = query_data.split("result_code")
            value = self.mongoObj.read_value_multi_keys("scheduler",{"email": query_data[0],"result_code":int(query_data[1])})
            if value != None:
                return ast.literal_eval(value["result"])
            else:
                return {"msg": "Your result session has been expired please execute this query again", "status": "False"}
        except Exception as e:
            return {"msg": e.__str__(), "status": "False"}
