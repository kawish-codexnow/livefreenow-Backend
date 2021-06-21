import base64
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from mailer import Message
from controllers.Classess.MongoDB_Json import MongoDB
from controllers.Classess.Config import Configuration
import bcrypt


class user:

    def __init__(self):
        self.name = "user"
        self.ip = Configuration().GetData()['PrivateIp']
        self.port = Configuration().GetData()['MongoPort']
        self.db = Configuration().GetData()['MongoDb']
        self.email = Configuration().GetData()['EmailID']
        self.password = Configuration().GetData()['Password']
        self.mongoObj = MongoDB()
        self.mongoObj.ConnectMongo(self.ip, self.port, self.db)

    # for account registration (SignUp)
    def register(self, request):
        data = request.data
        try:
            if re.search(r'[\w.-]+@[\w.-]+.\w+', data['email']):
                user_email = data['email']
                user_password = data['password']
                hashed_password = bcrypt.hashpw(user_password.encode(), bcrypt.gensalt())
                if self.mongoObj.check_record_exists('users', '_id', user_email):
                    return {"msg": "Email already exist", "status": "False"}
                else:
                    dic = {"_id": user_email, "password": hashed_password, "FirstName": data['firstname'],
                           'LastName': data['lastname'], "status": "1", "Department_Organization": data['department_organization'],
                           "Phone": data['phone'], "Company": data['company'], "Country": data['country'] , "Storage": "1000"}

                    html = """<html> <head> <title>LiveFree | Signup Email</title> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="icon" href="favicon.ico"> <style> @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap'); body { font-family: 'Roboto', sans-serif; } </style> </head> <body> <div class="section" style="padding: 30px 0;width: 100%;margin: auto;"> <table style="max-width: 600px;border-spacing: 0;border-collapse: collapse;table-layout: auto;margin: 0 auto;" cellspacing="0" cellpadding="0" border="0" align="center" width="600"> <tbody> <tr> <th valign="top"> <table width="100%" cellspacing="0" cellpadding="0" border="0" style="margin: 0 auto;border-spacing: 0;border-collapse: collapse;table-layout: auto;background-color: #00334e;text-align: left;"> <tbody> <tr> <td> <a href="#"><img src="https://livefreenow.us/assets/livefreelogo.png" style="height: 50px;padding: 20px;"></a> </td> </tr> </tbody> </table> </th> </tr> <tr> <td> <table width="100%" cellpadding="0" cellspacing="0" style="border-spacing:0;border-collapse:collapse;table-layout:auto;margin:0 auto;background-color: #fff;height: 350px;"> <tbody style="vertical-align: top;"> <tr> <td align="center" style="padding: 40px 40px 0 40px"> <img src="https://livefreenow.us/assets/checkmark.png" alt="success" width="150"> </td> </tr> <tr> <td align="left" style="padding:16px 40px"> <h1>Hello! <span style="color: #00669c;">"""+ str(data['firstname'])+"""</span>,</h1> <h4> Thanks for registering to LiveFree for all your IMR/Worker's Comp analysis needs. Would like to have a walk through of using LiveFree. If yes please download a short video or slide by clicking the link below: </h4> <p style="font-size: 14px;">Video: <a href="videolink" style="color: #00669c;font-weight: 600;">videolink</a> </p> <p style="font-size: 14px;">Powerpoint: <a href="powerpointlink" style="color: #00669c;font-weight: 600;">powerpointlink</a> </p> <p style="font-size: 14px;"> Regards, <br> <span style="color: #00669c;font-weight: 600;">LiveFree</span> </p> </td> </tr> </tbody> </table> </td> </tr> <tr> <td> <table width="100%" cellpadding="0" cellspacing="0" style="border-spacing:0;border-collapse:collapse;table-layout:auto;margin:0 auto;background-color: #00334e;color: #FFF;"> <tbody> <tr> <td align="left" style="padding:16px 40px"> <p style="font-size: 13px;line-height: 16px;">If you have any questions, contact us at <a href="mailto:info@livefreenow.us" style="color: #fff;">info@livefreenow.us</a>. </p> <p style="font-size: 13px;line-height: 16px;">© Copyright <a href="https://livefreenow.us" target="_blank" style="color: #fff;">LiveFree</a>. All Rights Reserved</p> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> </div> </body> </html>"""

                    part = MIMEText(html, 'html')
                    sender_address = self.email
                    sender_pass = self.password
                    receiver_address = user_email
                    message = MIMEMultipart()
                    message.attach(part)
                    message['From'] = sender_address
                    message['To'] = receiver_address
                    message['Subject'] = 'LiveFree Registration Successful'  # The subject line
                    # Create SMTP session for sending the mail
                    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
                    session.starttls()  # enable security
                    session.login(sender_address, sender_pass)  # login with mail_id and password
                    text = message.as_string()
                    session.sendmail(sender_address, receiver_address, text)
                    session.quit()
                    print("Email Registration sent!")
                    self.mongoObj.write_value("users", dic)
                    return {"status": "True", "msg": "User registered successfully!"}
            else:
                return {"msg": "invalid email", "status": "False"}
        except Exception as e:
            return {'status': 'False', 'msg': str(e)}

    def changepassword(self, request, decoded):
        try:
            data = request.data
            userid = decoded['email']
            record = self.mongoObj.read_value("users", '_id', userid)
            if (record != None):
                old_password = data['oldpassword']
                new_password = data["newpassword"]
                new_hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
                if bcrypt.checkpw(old_password.encode(), record['password']):
                    self.mongoObj.update_value('users',{'_id': userid}, {'password' : new_hashed_password})
                    return {"status": "True", 'msg': "Password Changed Successfully"}
                else:
                    return {"msg": "invalid old password", "status": "False"}
            else:
                return {"msg": "No user exist", "status": "False"}
        except Exception as e:
            return {'status': 'False', 'Error': str(e)}

    def verify(self, request):
        data = request.data
        try:
            email = base64.b64decode((bytes(str(data["email"]).replace("~", "="), "utf-8"))).decode("utf-8")
            record = self.mongoObj.read_value("users","_id", email)
            if (record != None):
                self.mongoObj.update_value("users", {'_id': email, 'status': '0'}, {'status': '1'})
                message = Message(From=self.email,
                                  To=email)
                message.Subject = "AutoETL Account Approved"

                message.Html = """

                <!DOCTYPE html>
                <html>
                <head>
                <style>
                @import url('https://fonts.googleapis.com/css?family=Open+Sans');

                body{
                font-family: sans-serif;
                }
                .main{
                background-color : #f3f7fa;
                height:300px;
                padding: 25px 250px;
                }
                .main h1{
                color : #0070c9;
                text-align: center;
                }
                .sub-main{
                padding: 25px 50px;
                background-color:#FFF;
                }
                .main .sub-main h1{
                    text-align: center;
                    color : #46555d;
                    font-weight:200;
                }
                .main .sub-main p{
                    text-align: center;
                    color:#46555d;
                    font-size:14px;
                }
                .main .sub-main img{
                    display:block; margin-left:auto;margin-right:auto;width:10%;height:10%;
                }
                </style>
                </head>
                <body>
                <div class="main" style=" background-color : #f3f7fa;height:300px; padding: 25px 250px;">
                <h1 style="color : #0070c9;text-align: center;">Codex</h1>
                <div class="sub-main" style="padding: 25px 50px; background-color:#FFF;">
                    <img style="display:block; margin-left:auto;margin-right:auto;width:10%;height:10%;" src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqbCA0f04h_Z2mbp3qs4Yr_Zxz5Xu_l8NYUCwOJMIJK7RWWGYW' />
                    <h1 style="text-align: center;color : #46555d;font-weight:200;">Account Approved</h1>
                    <hr>
                    <p style="  text-align: center;color:#46555d;font-size:14px;"><b>Dear """ + record[
                    '_id'] + """ !</b>  Your account has been approved successfully, Here is the link """ + self.sp_link + """ to Access AutoETL
                  </p>
                </div>
                </div>
                </body>
                </html>
                """

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.email, self.password)
                server.sendmail(self.email, email, message.as_string())
                return {"status": "True"}
            else:
                return {"msg": "invalid email", "status": "False"}
        except Exception as e:
            return {"msg": "invalid email", "status": "False"}


    def sendforgetemail(self, request):
        try:
            data = request.data
            email = data["email"]
            record = self.mongoObj.read_value("users","_id", email)
            if (record != None):
                message = Message(From=self.email,
                                  To=email)
                message.Subject = "Change Password"
                message.Html = """

                <!DOCTYPE html>
                <html>
                <head>
                <style>
                body{
                font-family: sans-serif;
                }
                .main{
                background-color : #f3f7fa;
                height:300px;
                padding: 25px 250px;
                }
                .main h1{
                color : #0070c9;
                text-align: center;
                }
                .sub-main{
                padding: 25px 50px;
                background-color:#FFF;
                }
                .main .sub-main h1{
                    text-align: center;
                    color : #46555d;
                    font-weight:200;
                }
                .main .sub-main p{
                    text-align: center;
                    color:#46555d;
                    font-size:14px;
                }
                .main .sub-main img{
                    display:block; margin-left:auto;margin-right:auto;width:10%;height:10%;
                }
                </style>
                </head>
                <body>
                <div class="main" style=" background-color : #f3f7fa;height:300px;padding: 25px 250px;">
                <h1 style="color : #0070c9;text-align: center;>Codex</h1>
                <div class="sub-main" style="padding: 25px 50px;background-color:#FFF;">
                    <img style="display:block; margin-left:auto;margin-right:auto;width:10%;height:10%;"  src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqbCA0f04h_Z2mbp3qs4Yr_Zxz5Xu_l8NYUCwOJMIJK7RWWGYW' />
                    <h1 style="text-align: center;color : #46555d;font-weight:200;">Reset Your Codex Password</h1>
                    <hr>
                     <p style=" text-align: center;color:#46555d;font-size:14px;">If this request is not from you, you can ignore this message and your account will still be secure.</p>
                      <p>Here is the link : <br>""" + self.forgot_passwordLink + (
                    str(base64.b64encode(bytes(email, "utf-8")).decode("utf-8"))).replace("=", "~") + """  to change your password
                   </p>
                </div>
                </div>
                </body>
                </html>
                """

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.email, self.password)
                server.sendmail(self.email, email, message.as_string())
                return {"status": "True"}
            else:
                return {"msg": "invalid email", "status": "False"}

        except Exception as e:
            return {"msg": "invalid email", "status": "False"}

    def forgot(self, request):
        try:
            data = request.data
            email = base64.b64decode((bytes(str(data["email"]).replace("~","="),"utf-8"))).decode("utf-8")
            record = self.mongoObj.read_value("users","_id", email)
            if (record != None):
                new_password = data["newpassword"]
                new_hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
                self.mongoObj.update_value("users", {'_id': email, 'password': record['password']}, {'password': new_hashed_password})
                return {"status": "True"}
            else:
                return {"msg": "invalid email", "status": "False"}
        except Exception as e:
            return {"msg": "invalid email", "status": "False"}



    def send_contact_email(self, request):
        try:
            print(request.data)
            data = request.data
            first_name = data["first_name"]
            last_name = data["last_name"]
            email = data["email"]
            content = data["content"]
            if re.search(r'[\w.-]+@[\w.-]+.\w+', email):
                message = Message(From=self.email, To="Support-Codex-Contact")
                message.Subject = "Feedback " + first_name
                message.Html = """<p>Iponym Contact Us!<br>""" + \
                               """<br>""" + "Name : " + first_name + " " + last_name + """<br>""" + \
                               """<br>""" + "Email : " + email + """<br><br><br> """ + \
                               content
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.email, self.password)
                server.sendmail(self.email, self.email, message.as_string())
                return {"status": "True"}
            else:
                return {"msg": "invalid email", "status": "False"}
        except Exception as e:
            return {'status': 'False', 'Error': str(e)}
