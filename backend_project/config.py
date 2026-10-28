import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    JWT_SECRET = os.getenv("JWT_SECRET")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    pass

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    DEBUG = True
    pass

class TestingConfig(Config):
    TESTING = True
    pass

class ProductionConfig(Config):
    DEBUG = False
    pass


config_dict = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}