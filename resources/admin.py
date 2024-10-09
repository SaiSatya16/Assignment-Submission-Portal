from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.admin import AdminModel
from models.assignment import AssignmentModel
from schemas import AdminSchema, AssignmentSchema
from marshmallow import ValidationError
import logging
from extensions import bcrypt
from bson import ObjectId
from bson.errors import InvalidId


logger = logging.getLogger(__name__)

admin_schema = AdminSchema()
assignment_schema = AssignmentSchema()

class AdminRegister(Resource):
    def post(self):
        try:
            admin_data = admin_schema.load(request.get_json())
        except ValidationError as err:
            logger.error(f"Validation error in AdminRegister: {err.messages}")
            return {"message": "Validation error", "errors": err.messages}, 400

        if AdminModel.find_by_username(admin_data['username']):
            logger.info(f"Attempted to register existing admin username: {admin_data['username']}")
            return {"message": "An admin with that username already exists"}, 400

        try:
            hashed_password = bcrypt.generate_password_hash(admin_data['password']).decode('utf-8')
            admin = AdminModel(admin_data['username'], hashed_password)
            admin.save_to_db()
            logger.info(f"New admin registered: {admin_data['username']}")
            return {"message": "Admin created successfully."}, 201
        except Exception as e:
            logger.error(f"Error in AdminRegister: {str(e)}")
            return {"message": "An error occurred creating the admin."}, 500

class AdminLogin(Resource):
    def post(self):
        try:
            admin_data = admin_schema.load(request.get_json())
        except ValidationError as err:
            logger.error(f"Validation error in AdminLogin: {err.messages}")
            return {"message": "Validation error", "errors": err.messages}, 400

        admin = AdminModel.find_by_username(admin_data['username'])

        if admin and admin.check_password(admin_data['password']):
            access_token = create_access_token(identity=str(admin._id))
            logger.info(f"Admin logged in: {admin_data['username']}")
            return {'access_token': access_token}, 200
        
        logger.info(f"Failed login attempt for admin username: {admin_data['username']}")
        return {'message': 'Invalid credentials'}, 401

class AssignmentList(Resource):
    @jwt_required()
    def get(self):
        admin_id = get_jwt_identity()
        try:
            assignments = AssignmentModel.find_by_admin(admin_id)
            logger.info(f"Assignments retrieved for admin: {admin_id}")
            assignment_list = [assignment.json() for assignment in assignments]
            logger.debug(f"Assignment list: {assignment_list}")
            return {'assignments': assignment_list}, 200
        except Exception as e:
            logger.error(f"Error in AssignmentList: {str(e)}")
            return {"message": "An error occurred retrieving the assignments.", "error": str(e)}, 500

class AcceptAssignment(Resource):
    @jwt_required()
    def post(self, id):
        admin_id = get_jwt_identity()
        logger.debug(f"Attempting to accept assignment: {id} by admin: {admin_id}")
        try:
            assignment = AssignmentModel.find_by_id(id)
            logger.debug(f"Assignment found: {assignment}")

            if not assignment:
                logger.warning(f"Attempt to accept non-existent assignment: {id}")
                return {'message': 'Assignment not found'}, 404

            if str(assignment.admin_id) != admin_id:
                logger.warning(f"Unauthorized attempt to accept assignment: {id} by admin: {admin_id}")
                return {'message': 'Not authorized to accept this assignment'}, 403

            assignment.status = 'accepted'
            assignment.save_to_db()
            logger.info(f"Assignment {id} accepted by admin {admin_id}")
            return {'message': 'Assignment accepted successfully.'}, 200
        except InvalidId:
            logger.warning(f"Invalid assignment id: {id}")
            return {"message": "Invalid assignment ID"}, 400
        except Exception as e:
            logger.error(f"Error in AcceptAssignment: {str(e)}")
            return {"message": "An error occurred accepting the assignment.", "error": str(e)}, 500

class RejectAssignment(Resource):
    @jwt_required()
    def post(self, id):
        admin_id = get_jwt_identity()
        logger.debug(f"Attempting to reject assignment: {id} by admin: {admin_id}")
        try:
            assignment = AssignmentModel.find_by_id(id)
            logger.debug(f"Assignment found: {assignment}")

            if not assignment:
                logger.warning(f"Attempt to reject non-existent assignment: {id}")
                return {'message': 'Assignment not found'}, 404

            if str(assignment.admin_id) != admin_id:
                logger.warning(f"Unauthorized attempt to reject assignment: {id} by admin: {admin_id}")
                return {'message': 'Not authorized to reject this assignment'}, 403

            assignment.status = 'rejected'
            assignment.save_to_db()
            logger.info(f"Assignment {id} rejected by admin {admin_id}")
            return {'message': 'Assignment rejected successfully.'}, 200
        except InvalidId:
            logger.warning(f"Invalid assignment id: {id}")
            return {"message": "Invalid assignment ID"}, 400
        except Exception as e:
            logger.error(f"Error in RejectAssignment: {str(e)}")
            return {"message": "An error occurred rejecting the assignment.", "error": str(e)}, 500