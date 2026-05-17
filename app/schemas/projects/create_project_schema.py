from marshmallow import fields, validate
from app.schemas.base_schema import BaseSchema

class CreateProjectSchema(BaseSchema):
    
    title = fields.Str(
        required = True, 
        validate = validate.Length(min = 3, max = 80)
    )     # Validate Length
     
    description = fields.Str(
        required = True, 
        validate = validate.Length(max = 255)
    )
    
    owner_id = fields.Int(required = False)