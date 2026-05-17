from marshmallow import fields
from app.schemas.base_schema import BaseSchema

# Project Schema for validation
class ProjectResponseSchema(BaseSchema):
    id              = fields.Int(dump_only = True)
    title           = fields.Str()
    description     = fields.Str()
    owner_id        = fields.Int()
    created_at      = fields.DateTime(dump_only = True)
    updated_at      = fields.DateTime(dump_only = True)