from marshmallow import fields
from app.extensions import ma

# User Schema for validation
class UserSchema(ma.Schema):
    user_id         = fields.Int(dump_only = True)
    username        = fields.Str(required = True)
    password_hash   = fields.Str(required = True)
    email           = fields.Email(required = True)
    created_at      = fields.DateTime(dump_only = True)