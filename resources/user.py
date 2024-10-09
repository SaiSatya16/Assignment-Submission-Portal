from flask_restful import Resource, reqparse
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import UserModel
from models.admin import AdminModel
from models.assignment import AssignmentModel
from schemas import UserSchema, AssignmentSchema, AssignmentInputSchema
from marshmallow import ValidationError
import logging
from extensions import bcrypt
logger = logging.getLogger(__name__)
assignment_input_schema = AssignmentInputSchema()

logger = logging.getLogger(__name__)

user_schema = UserSchema()
assignment_schema = AssignmentSchema()

class UserRegister(Resource):
    def post(self):
        try:
            user_data = user_schema.load(request.get_json())
        except ValidationError as err:
            logger.error(f"Validation error in UserRegister: {err.messages}")
            return {"message": "Validation error", "errors": err.messages}, 400

        if UserModel.find_by_username(user_data['username']):
            logger.info(f"Attempted to register existing username: {user_data['username']}")
            return {"message": "A user with that username already exists"}, 400

        try:
            hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
            user = UserModel(user_data['username'], hashed_password)
            user.save_to_db()
            logger.info(f"New user registered: {user_data['username']}")
            return {"message": "User created successfully."}, 201
        except Exception as e:
            logger.error(f"Error in UserRegister: {str(e)}")
            return {"message": "An error occurred creating the user."}, 500

class UserLogin(Resource):
    def post(self):
        try:
            user_data = user_schema.load(request.get_json())
        except ValidationError as err:
            logger.error(f"Validation error in UserLogin: {err.messages}")
            return {"message": "Validation error", "errors": err.messages}, 400

        user = UserModel.find_by_username(user_data['username'])

        if user and user.check_password(user_data['password']):
            access_token = create_access_token(identity=str(user._id))
            logger.info(f"User logged in: {user_data['username']}")
            return {'access_token': access_token}, 200
        
        logger.info(f"Failed login attempt for username: {user_data['username']}")
        return {'message': 'Invalid credentials'}, 401

class UploadAssignment(Resource):
    @jwt_required()
    def post(self):
        try:
            data = assignment_input_schema.load(request.get_json())
        except ValidationError as err:
            logger.error(f"Validation error in UploadAssignment: {err.messages}")
            return {"message": "Validation error", "errors": err.messages}, 400

        user_id = get_jwt_identity()
        admin = AdminModel.find_by_username(data['admin'])

        if not admin:
            logger.warning(f"Attempt to upload assignment to non-existent admin: {data['admin']}")
            return {'message': 'Admin not found'}, 404

        try:
            assignment = AssignmentModel(user_id, data['task'], str(admin._id))
            assignment.save_to_db()
            logger.info(f"New assignment uploaded by user {user_id} for admin {admin._id}")
            return {'message': 'Assignment uploaded successfully.', 'assignment_id': str(assignment._id)}, 201
        except Exception as e:
            logger.error(f"Error in UploadAssignment: {str(e)}")
            return {"message": "An error occurred uploading the assignment."}, 500

class AdminList(Resource):
    @jwt_required()
    def get(self):
        try:
            admins = [admin.username for admin in AdminModel.find_all()]
            logger.info("AdminList retrieved successfully")
            return {'admins': admins}, 200
        except Exception as e:
            logger.error(f"Error in AdminList: {str(e)}")
            return {"message": "An error occurred retrieving the admin list."}, 500