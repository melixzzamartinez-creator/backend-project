from flask import Blueprint, request, jsonify, current_app, g
from backend_project.models import User 
from backend_project.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
import jwt
from backend_project.app.auth.auth import require_auth



your_bp_variable = Blueprint("your_name_here", __name__)

@your_bp_variable.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200

@your_bp_variable.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if data is None:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "request body must be JSON"
        }), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not isinstance(username, str) or not 3 <= len(username) <= 20:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "username is required and must be between 3 and 20 characters"
        }), 400

    if not isinstance(email, str) or "@" not in email or "." not in email.split("@")[-1]:
            return jsonify({
                "code": "VALIDATION_ERROR",
                "message": "email is required and must be a valid email address"
            }), 400

    if not isinstance(password, str) or len(password) < 8:
            return jsonify({
                "code": "VALIDATION_ERROR",
                "message": "password is required and must be at least 8 characters long"
            }), 400

    existing_user = User.query.filter_by(username=username).first()

    if existing_user is not None:
        return jsonify({
            "code": "USERNAME_TAKEN",
            "message": "That username is already in use"
    }), 409


    password_hash = generate_password_hash(password)

    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "created_at": new_user.created_at.isoformat()
    }), 201

@your_bp_variable.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({
            "code": "AUTH_FAILED",
            "message": "Invalid username or password"
        }), 401

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user is None or not isinstance(password, str) or not check_password_hash(user.password_hash, password):
        return jsonify({
            "code": "AUTH_FAILED",
            "message": "Invalid username or password"
        }), 401
    
    expires_at = datetime.now(timezone.utc) + timedelta(
        seconds=current_app.config["JWT_LIFETIME_SECONDS"]
        )

    payload ={
        "sub": str(user.id),
        "role": user.role,
        "exp": expires_at
    }

    token = jwt.encode(
        payload,
        current_app.config["JWT_SECRET"],
        algorithm="HS256"
    )

    return jsonify({
         "access_token": token
    }), 200

@your_bp_variable.route("/me", methods=["GET"])
@require_auth
def me():
     user = User.query.get(g.current_user_id)

     if user is None:
          return jsonify({
               "code": "USER_NOT_FOUND",
               "message": "User not found"
          }), 404

     return jsonify({
          "id": user.id,
          "username": user.username,
          "email": user.email,
          "created_at": user.created_at.isoformat() if user.created_at else None
     }), 200

@your_bp_variable.route("/me", methods=["PATCH"])
@require_auth
def update_me():
    user = User.query.get(g.current_user_id)

    if user is None:
        return jsonify({
            "code": "USER_NOT_FOUND",
            "message": "User not found"
        }), 404

    data = request.get_json()

    if data is None:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "request body must be JSON"
        }), 400

    # username block
    if "username" in data:
        username = data["username"]

        if not isinstance(username, str) or not 3 <= len(username) <= 20:
            return jsonify({
                "code": "VALIDATION_ERROR",
                "message": "username is required and must be between 3 and 20 characters"
            }), 400

        existing_user = User.query.filter_by(username=username).first()

        if existing_user is not None and existing_user.id != user.id:
            return jsonify({
                "code": "USERNAME_TAKEN",
                "message": "That username is already taken"
            }), 409

        user.username = username

    # email block – NOT nested under username
    if "email" in data:
        email = data["email"]

        if not isinstance(email, str) or "@" not in email or "." not in email.split("@")[-1]:
            return jsonify({
                "code": "VALIDATION_ERROR",
                "message": "email must be a valid email address"
            }), 400

        existing_user = User.query.filter_by(email=email).first()

        if existing_user is not None and existing_user.id != user.id:
            return jsonify({
                "code": "EMAIL_TAKEN",
                "message": "email already in use"
            }), 409

        user.email = email

    db.session.commit()

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }), 200

@your_bp_variable.route("/admin/ping", methods=["GET"])
@require_auth
def admin_ping():
    user = User.query.get(g.current_user_id)

    if user is None:
        return jsonify({
            "code": "USER_NOT_FOUND",
            "message": "User not found"
        }), 404

    if user.role != "admin":
        return jsonify({
            "code": "FORBIDDEN",
            "message": "Admin access required"
        }), 403

    return jsonify({
        "message": "Welcome admin!!"
    }), 200