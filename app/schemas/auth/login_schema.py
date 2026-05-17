from marshmallow import fields, validate
from app.schemas.base_schema import BaseSchema

class LoginSchema(BaseSchema):
    username = fields.Str(
        required = True,
        validate = validate.Length(min = 3, max = 80)
    )

    password = fields.Str(
        required = True,
        validate = validate.Length(min = 8, max = 128),
        load_only = True
    )