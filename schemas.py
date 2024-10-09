from marshmallow import Schema, fields, validate
from bson import ObjectId
from marshmallow import ValidationError

class ObjectIdField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return ObjectId(value)
        except:
            raise ValidationError('Invalid ObjectId')

class UserSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=6, max=50), load_only=True)

class AdminSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=6, max=50), load_only=True)

class AssignmentSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    user_id = fields.Str(required=True)
    task = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    admin_id = fields.Str(required=True)
    status = fields.Str(validate=validate.OneOf(['pending', 'accepted', 'rejected']), default='pending')
    timestamp = fields.DateTime(format='iso')

class AssignmentInputSchema(Schema):
    task = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    admin = fields.Str(required=True, validate=validate.Length(min=3, max=50))