from extensions import mongo
from bson import ObjectId
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class AssignmentModel:
    def __init__(self, user_id, task, admin_id, status='pending', _id=None, timestamp=None):
        self.user_id = user_id
        self.task = task
        self.admin_id = admin_id
        self.status = status
        self.timestamp = timestamp if timestamp else datetime.now(timezone.utc)
        self._id = _id

    def json(self):
        return {
            'user_id': self.user_id,
            'task': self.task,
            'admin_id': self.admin_id,
            'status': self.status,
            'timestamp': self.timestamp
        }

    def save_to_db(self):
        if not self._id:
            result = mongo.db.assignments.insert_one(self.json())
            self._id = result.inserted_id
        else:
            mongo.db.assignments.update_one({'_id': ObjectId(self._id)}, {'$set': self.json()})
        logger.debug(f"Saved assignment with ID: {self._id}")

    @classmethod
    def find_by_admin(cls, admin_id):
        logger.debug(f"Finding assignments for admin: {admin_id}")
        assignments = mongo.db.assignments.find({'admin_id': admin_id})
        return [cls(**assignment) for assignment in assignments]

    @classmethod
    def find_by_id(cls, _id):
        logger.debug(f"Finding assignment by ID: {_id}")
        try:
            assignment = mongo.db.assignments.find_one({'_id': ObjectId(_id)})
            logger.debug(f"Found assignment: {assignment}")
            return cls(**assignment) if assignment else None
        except Exception as e:
            logger.error(f"Error finding assignment by ID: {str(e)}")
            return None

    @classmethod
    def from_mongo(cls, mongo_data):
        if mongo_data:
            mongo_data['_id'] = str(mongo_data['_id'])
            logger.debug(f"Creating AssignmentModel from mongo data: {mongo_data}")
            return cls(**mongo_data)
        return None