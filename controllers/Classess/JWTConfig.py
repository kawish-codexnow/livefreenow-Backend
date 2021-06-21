from datetime import datetime, timedelta
from flask_jwt_extended import (
    get_jwt_identity
)

from rest_framework_simplejwt.tokens import RefreshToken
import bcrypt
import jwt

from controllers.Classess.Config import Configuration
from controllers.Classess.MongoDB_Json import MongoDB

JWT_SECRET = 'SECRET_KEY'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 259200


class JWT:

    def __init__(self):
        self.ip = Configuration().GetData()['PrivateIp']
        self.port = Configuration().GetData()['MongoPort']
        self.db = Configuration().GetData()['MongoDb']
        self.mongoObj = MongoDB()
        self.mongoObj.ConnectMongo(self.ip, self.port, self.db)

    def login(self, request):
        try:
            data = request.data
            saved_password = self.mongoObj.read_value('users', '_id', data['email'])
            if saved_password != None:
                password = data['password']
                if bcrypt.checkpw(password.encode(), saved_password['password']):
                    payload = {'email':data['email'], 'password':data['password'], 'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)}
                    ret = {"access_token":jwt.encode(payload, JWT_SECRET), 'status':"True"}
                    return ret
                else:
                     return {"status": "False", "Error": "Invalid username or password"}
            else:
                return {'status': 'False', 'Error': "User not exists"}

        except Exception as e:
            return {'status': 'False', 'Error': "User not exists"}


    def refresh(self):
        try:
            current_user = get_jwt_identity()
            ret = {
                'access_token': RefreshToken(current_user),
                'refresh_token': RefreshToken(current_user),
                'status': "Successfully Refreshed"
            }
            return ret
        except Exception as e:
            return {"status": "False", "Error": str(e)}

    def get_user(self, token):
        try:
            email = token['email']
            record = self.mongoObj.read_value('users', '_id', email)
            record.pop('password', None)
            return record
        except Exception as e:
            return {"status": "False", "Error": str(e)}


    def token_validation(self,request):
        try:
            value = request.headers.get('Authorization')
            value = value.split()
            return {"msg":"success", "email": jwt.decode(value[1], JWT_SECRET)["email"], "status": "True"}
        except Exception as e:
            if e.__str__() == "'NoneType' object has no attribute 'split'":
                return {"msg": "missing 'Authorization' key in header", "status": "False"}
            elif e.__str__() == "list index out of range":
                return {"msg": "invalid token please write 'Bearer' before token code", "status": "False"}
            else:
                return {"msg": e.__str__(), "status": "False"}