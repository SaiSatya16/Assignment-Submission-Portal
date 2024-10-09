from extensions import mongo, bcrypt
from bson import ObjectId

class AdminModel:
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
            result = mongo.db.admins.insert_one(self.json())
            self._id = result.inserted_id
        else:
            mongo.db.admins.update_one({'_id': ObjectId(self._id)}, {'$set': self.json()})

    @classmethod
    def find_by_username(cls, username):
        admin_data = mongo.db.admins.find_one({'username': username})
        return cls(**admin_data) if admin_data else None

    @classmethod
    def find_all(cls):
        return [cls(**admin) for admin in mongo.db.admins.find()]

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)