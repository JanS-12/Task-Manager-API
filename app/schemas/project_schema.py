from marshmallow import fields
from app.extensions import ma

# Project Schema for validation
class ProjectSchema(ma.Schema):
    project_id      = fields.Int(dump_only = True)
    project_name    = fields.Str(required = True)
    description     = fields.Str()
    owner_id        = fields.Int(required = True)
    created_at      = fields.DateTime(dump_only = True)