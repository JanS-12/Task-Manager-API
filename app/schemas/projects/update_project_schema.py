from marshmallow import fields, validate
from app.schemas.base_schema import BaseSchema

class UpdateProjectSchema(BaseSchema):
    
    title = fields.Str(
        required = False, 
        validate = validate.Length(min = 3, max = 80)
    )     # Validate Length
     
    description = fields.Str(
        required = False, 
        validate = validate.Length(max = 255)
    )
    
    owner_id = fields.Int(required = False)