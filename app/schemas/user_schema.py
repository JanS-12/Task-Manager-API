from marshmallow import fields, validate
from app.extensions import ma

# User Schema for validation
class UserSchema(ma.Schema):
    user_id         = fields.Int(dump_only = True)
    username        = fields.Str(required = True, validate = validate.Length(min = 3, max = 80))        # Validate Length
    password_hash   = fields.Str(required = True, validate = validate.Length(min = 8, max = 128), load_only = True)  # Validate Length, load only, do not return. 
    email           = fields.Email(required = True)
    role            = fields.Str(required = True)
    created_at      = fields.DateTime(dump_only = True)
    updated_at      = fields.DateTime(dump_only = True)