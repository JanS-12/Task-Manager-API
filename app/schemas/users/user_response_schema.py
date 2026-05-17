from marshmallow import fields
from app.schemas.base_schema import BaseSchema

class UserResponseSchema(BaseSchema):

    id         = fields.Integer(dump_only=True)
    username   = fields.String()
    email      = fields.Email()
    role       = fields.String()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)