from marshmallow import fields, validate
from app.schemas.base_schema import BaseSchema

class RegistrationSchema(BaseSchema):

    username = fields.Str(
        required = True, 
        validate = validate.Length(min = 3, max = 80)
    )        # Validate Length
    
    password = fields.Str(
        required = True, 
        validate = validate.Length(min = 8, max = 128), 
        load_only = True
    )  # Validate Length, load only, do not return. 
    
    email    = fields.Email(required = True)
    
    role = fields.String(
        required=False,
        load_default="user",
        validate=validate.OneOf(["user", "admin"])
    )