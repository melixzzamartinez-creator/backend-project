from flask import Flask, jsonify
from backend_project.extensions import db, migrate
from backend_project.config import config_dict
from backend_project.routes.auth import auth_bp
from backend_project.routes.tasks import tasks_bp
from backend_project.routes.general import general_bp


def create_app(config_name): 
    app = Flask(__name__)

    config_class = config_dict[config_name]
    app.config.from_object(config_class)

    
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(general_bp)

    from backend_project import models  

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "code": "BAD_REQUEST",
            "message": "Bad request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "code": "AUTH_FAILED",
            "message": "Authentication required"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "code": "FORBIDDEN",
            "message": "You do not have permission to access this resource"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "code": "NOT_FOUND",
            "message": "Resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "code": "METHOD_NOT_ALLOWED",
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected server error occurred"
        }), 500

    return app
