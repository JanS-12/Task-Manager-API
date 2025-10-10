from marshmallow import fields, validate
from app.extensions import ma

# Project Schema for validation
class ProjectSchema(ma.Schema):
    project_id      = fields.Int(dump_only = True)
    project_name    = fields.Str(required = True, validate = validate.Length(min = 3, max = 80))     # Validate Length 
    description     = fields.Str()
    owner_id        = fields.Int(required = True)
    created_at      = fields.DateTime(dump_only = True)
    updated_at      = fields.DateTime(dump_only = True)

    