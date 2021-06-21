from controllers.Classess.JWTConfig import JWT
from controllers.Classess.User import user

jwt_auth = JWT()

class userApi():
    def __init__(self):
        self.name = "usersApi"
        self.user = user()

    def post(self, request):
        data = request.data
        action = data["action"]

        if action == 'register':
            return self.user.register(request)

        elif action == 'changepassword':
            token = jwt_auth.token_validation(request)
            if token["status"] == "False":
                return token
            result = self.user.changepassword(request, token)
            return result


        elif action == 'verify':
            return self.user.verify(request)

        elif action == 'sendforgetemail':
            return self.user.sendforgetemail(request)

        elif action == 'forgetpassword':
            return self.user.forgot(request)

        elif action == 'contactus':
            try :
                return self.user.send_contact_email(request)
            except Exception as e :
                return {'status': 'False', 'Error': str(e)}
