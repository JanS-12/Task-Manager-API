import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///taskmanager.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
    
    # JWT
    JWT_SECRET_KEY  = os.getenv("JWT_SECRET_KET", "jwt-secret-dev")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes = int(os.getenv("ACESS_EXPIRES_MINUTES", 15))) # 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days = int(os.getenv("REFRESH_EXPIRES_DAYS", 3))) # 3 Days
