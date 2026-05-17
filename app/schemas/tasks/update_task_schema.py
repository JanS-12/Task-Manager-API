from marshmallow import fields, validate
from app.schemas.base_schema import BaseSchema

class UpdateTaskSchema(BaseSchema):
    
    title = fields.Str(
        required = False, 
        validate = validate.Length(min = 3, max = 80)
    )     # Validate Length
     
    description = fields.Str(
        required = False, 
        validate = validate.Length(max = 255)
    )
    
    project_id = fields.Int(required = False)