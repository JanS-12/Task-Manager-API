from marshmallow import fields
from app.extensions import ma

# Task Schema for validation
class TaskSchema(ma.Schema):
    task_id     = fields.Int(dump_only = True)
    task_name   = fields.Str(required = True)
    description = fields.Str()
    project_id  = fields.Int(required = True)
    created_at  = fields.DateTime(dump_only = True)