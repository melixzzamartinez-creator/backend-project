from flask import Flask
from backend_project.extensions import db, migrate
from backend_project.routes import your_bp_variable
from backend_project.config import config_dict



def create_app(config_name): 
    app = Flask(__name__)

    config_class = config_dict[config_name]
    app.config.from_object(config_class)

    print("JWT_SECRET from config:", app.config.get("JWT_SECRET"))
    print("DB URI from config:", app.config.get("SQLALCHEMY_DATABASE_URI"))
    
    db.init_app(app)
    migrate.init_app(app)
    app.register_blueprint(your_bp_variable)

    return app