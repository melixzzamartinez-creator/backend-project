from functools import wraps
from flask import request, jsonify, current_app, g
import jwt


def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({
                "code": "AUTH_REQUIRED",
                "message": "Missing or invalid authorization header"
            }), 401

        token = auth_header.split(" ", 1)[1]

        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET"],
                algorithms=["HS256"]
            )
            user_id = int(payload["sub"])

        except Exception as e:
            print("JWT decode error:", type(e).__name__, str(e))
            return jsonify({
                "code": "AUTH_FAILED",
                "message": "Invalid or expired token"
            }), 401

        g.current_user_id = user_id
        return fn(*args, **kwargs)

    return wrapper