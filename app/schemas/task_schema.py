from marshmallow import fields, validate
from app.extensions import ma

# Task Schema for validation
class TaskSchema(ma.Schema):
    task_id     = fields.Int(dump_only = True)
    task_name   = fields.Str(required = True, validate = validate.Length(min = 5, max = 80))    # Validate Length
    description = fields.Str()
    project_id  = fields.Int(required = True)
    created_at  = fields.DateTime(dump_only = True)
    updated_at  = fields.DateTime(dump_only = True)