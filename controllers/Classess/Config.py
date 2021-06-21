class Configuration:

    def GetData(self):

        Datadictionary = {

            # Mongo Parameters/Credentials
            "PrivateIp": "136.52.8.216",
            "MongoPort": 27017,
            "MongoDb": "HealthCare",
            "username": "kawish",
            "password": "#codexkawish",

            # Send Email Credentials
            "EmailID": "kawish@codexnow.com",
            "Password": "kawish@123",

            # api's EndPoint
            "apisEndPoint": "https://livefreenow.us:5003/",

            # Redis Parameters/Credentials
            "IpDPCS": "172.17.0.2",
            "PortDPCS": 6379

        }
        return Datadictionary