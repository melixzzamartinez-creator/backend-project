from flask import Blueprint

general_bp = Blueprint("general", __name__)

@general_bp.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200