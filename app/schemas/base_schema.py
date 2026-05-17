from marshmallow import RAISE
from app.extensions import ma

class BaseSchema(ma.Schema):

    class Meta:
        unknown = RAISE