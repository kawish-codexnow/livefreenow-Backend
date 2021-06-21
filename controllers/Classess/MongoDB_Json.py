# To Save / Read Data in Json Format

from pymongo import MongoClient


class MongoDB():
    def __init__(self):
        self.name = 'Mongo'
        self.client = None
        self.db = None

    def ConnectMongo(self, Host, Port, dbName):
        self.client = MongoClient('mongodb://' + 'kawish' + ':' + '#codexkawish' + '@' + Host + ':' + str(Port) + '/')
        self.db = self.client[str(dbName)]
        # self.client = MongoClient(Host,Port)
        # self.db = self.client[str(dbName)]

    # To Save One Record
    def write_value(self,collectionName, data):
        try:
            self.collection = self.db[collectionName]
            post_data = data
            self.collection.insert_one(post_data)

        except Exception as e:
            print(str(e))

    # To save whole df in Json Format
    def write_values(self, collectionName, data):
        try:
            self.collection = self.db[collectionName]
            self.collection.insert_many(data)
        except Exception as e:
            print(str(e))

    # Example of how to use this method is given in the end of this file
    def update_value(self, collectionName, myquery, newvalues):
        try:
            self.collection = self.db[collectionName]
            self.collection.update_one(myquery, {"$set": newvalues})
        except Exception as e:
            print(str(e))

    def read_value(self,collectionName, key, value):
        try:
            self.collection = self.db[collectionName]
            value = self.collection.find_one({key: value})
            return value

        except Exception as e:
            print(str(e))


    def read_value_multi_keys(self,collectionName, query):
        try:
            self.collection = self.db[collectionName]
            value = self.collection.find_one(query)
            return value

        except Exception as e:
            print(str(e))


    # To Read whole collection
    def read_all_data(self, collectionName):
        try:
            self.collection = self.db[collectionName]
            value = self.collection.find({})
            return value

        except Exception as e:
            print(str(e))


    # To Read whole collection with query
    def read_all_data_with_query(self, collectionName, query):
        try:
            self.collection = self.db[collectionName]
            value = self.collection.find(query)
            return value

        except Exception as e:
            print(str(e))


    # To Read whole column
    def read_all_data_column(self, collectionName,column_name):
        try:
            self.collection = self.db[collectionName]
            value = self.collection.find({}, {column_name: 1}).limit(500)
            return value

        except Exception as e:
            print(str(e))

    def drop_collection(self, collection_name):
        try:
            return self.db.drop_collection(collection_name)
        except Exception as e:
            return str(e)

    def check_record_exists(self, collection_name, key, value):
        self.collection = self.db[collection_name]
        result = self.collection.find({key: value}).count() > 0
        print(result)
        return result

    def push_value_in_list(self,collection_name, value):
        self.collection = self.db[collection_name]
        self.collection.update({'key':'12345'}, {'$addToSet': {'body_parts': value["body_part"], "drugs": value["drugs"], "treatments": value["treatment"], "servies": value["services"]}})



# Sample For Update Value :
# mongoObj = MongoDB()
# mongoObj.ConnectMongo('35.160.233.37', '27017', 'AutoETL')
# mongoObj.update_value('users',{'_id': 'abdullah@codexnow.com', 'Company': 'CodeX'}, {'Company': 'Xprime'})