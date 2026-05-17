from marshmallow import fields
from app.schemas.base_schema import BaseSchema

# Task Schema for validation
class TaskResponseSchema(BaseSchema):
    id          = fields.Int(dump_only = True)
    title       = fields.Str()
    description = fields.Str()
    project_id  = fields.Int()
    created_at  = fields.DateTime(dump_only = True)
    updated_at  = fields.DateTime(dump_only = True)