from marshmallow import fields, validate
from app.schemas.base_schema import BaseSchema

class UpdateUserSchema(BaseSchema):

    username = fields.String(
        required = False,
        validate = validate.Length(min=3, max=80)
    )

    password = fields.String(
        required = False,
        validate = validate.Length(min=8, max=128),
        load_only = True
    )

    email = fields.Email(required = False)
    
    role = fields.String(
        required = False,
        load_default = "user",
        validate = validate.OneOf(["user", "admin"])
    )