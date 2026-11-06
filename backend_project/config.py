import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_LIFETIME_SECONDS = 60
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    DEBUG = True
    

class TestingConfig(Config):
    TESTING = True
    

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    DEBUG = False
    


config_dict = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}