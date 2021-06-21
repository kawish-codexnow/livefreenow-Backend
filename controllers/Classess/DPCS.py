import redis
from controllers.Classess.Config import Configuration

class DPCS():

    def __init__(self):
        self.name   ='DPCS'
        self.DPCSIP = Configuration().GetData()['IpDPCS']
        self.DPCSPort = Configuration().GetData()['PortDPCS']

    def WriteDataToDPCS(self, DPCSValue, Key, Data):
        try:
            DPCS = redis.StrictRedis(host=str(self.DPCSIP), port=self.DPCSPort, db=DPCSValue)
            print('insert key',Key)
            DPCS.set(str(Key), Data)
            return True
        except Exception as e:
            print(str(e))
            return str(e)

    def ReadDataFromDPCS(self, DPCSValue, Key):
        try:
            DPCS = redis.StrictRedis(host=str(self.DPCSIP), port=self.DPCSPort, db=DPCSValue)
            print('get key',Key)
            return (DPCS.get(str(Key)))
        except Exception as e:
            print(str(e))
            return str(e)

    def FlushRedis(self,DPCSValue):
        try:
            DPCS = redis.StrictRedis(host=str(self.DPCSIP), port=self.DPCSPort, db=DPCSValue)
            DPCS.flushall()
            return True
        except Exception as e:
            return str(e)




