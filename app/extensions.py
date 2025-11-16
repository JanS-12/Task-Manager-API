from flask_limiter.util import get_remote_address
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
limiter = Limiter(key_func = get_remote_address,)