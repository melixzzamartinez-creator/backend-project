from flask import Blueprint

your_bp_variable = Blueprint("your_name_here", __name__)

@your_bp_variable.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200