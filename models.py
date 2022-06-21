import pymongo
from flask_login import UserMixin

#connect to MongoDB
import pymongo
connection = pymongo.MongoClient('mongodb://localhost:27017')
db = connection['ECA']
records = db.useraccount
catalogrecords = db.catalogrecords

class User(UserMixin):
    def __init__(self,email,data):
        self._email = email
        self._data = data

    def get_email(self):
        return self._email
    
    def get_id(self):
        return self._email
    
    def get_data(self):
        return self._data
    
class UserAccount():
    def __init__(self,email,password,nric):
        records.insert_one({'email' : email, 'password': password, 'nric' : nric})
    
    def get_user_byEmail(email):
        
        filter = {}
        filter["email"] = email
        
        Cursor = records.find(filter).limit(1)
        if Cursor.count() == 1:
            return User(email=email, data=Cursor.next())
        else:
            return None