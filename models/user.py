from extensions import mongo, bcrypt
from bson import ObjectId

class UserModel:
    def __init__(self, username, password, _id=None):
        self.username = username
        self.password = password
        self._id = _id

    def json(self):
        return {
            'username': self.username,
            'password': self.password
        }

    def save_to_db(self):
        if not self._id:
            result = mongo.db.users.insert_one(self.json())
            self._id = result.inserted_id
        else:
            mongo.db.users.update_one({'_id': self._id}, {'$set': self.json()})

    @classmethod
    def find_by_username(cls, username):
        user_data = mongo.db.users.find_one({'username': username})
        return cls(**user_data) if user_data else None

    @classmethod
    def find_by_id(cls, _id):
        user_data = mongo.db.users.find_one({'_id': ObjectId(_id)})
        return cls(**user_data) if user_data else None

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)