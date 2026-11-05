from flask import Blueprint, request, jsonify, g
from backend_project.models import Task
from backend_project.extensions import db
from backend_project.app.auth.auth import require_auth

tasks_bp = Blueprint("tasks", __name__)

MAX_PER_PAGE = 100

@tasks_bp.route("/tasks", methods=["POST"])
@require_auth
def create_task():
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "Request body must be JSON"
        }), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "Title is required"
        }), 400

    task = Task(
        title=title.strip(),
        user_id=g.current_user_id
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "id": task.id,
        "title": task.title,
        "is_completed": task.is_completed,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "user_id": task.user_id
    }), 201

@tasks_bp.route("/tasks", methods=["GET"])
@require_auth
def get_tasks():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
    except ValueError:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "page and per_page must be integers"
        }), 400

    if page < 1 or per_page <1:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "page and per_page must be greater than 0"
        }), 400

    if per_page > MAX_PER_PAGE:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": f"per_page cannot exceed {MAX_PER_PAGE}"
        }), 400

    
    pagination = Task.query.filter_by(
        user_id=g.current_user_id
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "items": [
            {
            "id": task.id,
            "title": task.title,
            "is_completed": task.is_completed,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "user_id": task.user_id
            }

            for task in pagination.items
        ],
        "page":pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev
    }), 200

@tasks_bp.route("/tasks/<int:task_id>", methods=["GET"])
@require_auth
def get_task(task_id):
    task = Task.query.filter_by(
        id=task_id,
        user_id=g.current_user_id
    ).first()

    if task is None:
        return jsonify({
            "code": "NOT_FOUND",
            "message": "task not found"
        }), 404

    return jsonify({
        "id": task.id,
        "title": task.title,
        "is_completed": task.is_completed,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "user_id": task.user_id
    }), 200

@tasks_bp.route("/tasks/<int:task_id>", methods=["PATCH"])
@require_auth
def update_task(task_id):
    task = Task.query.filter_by(
        id=task_id,
        user_id=g.current_user_id
    ).first()
    
    if task is None:
        return jsonify({
            "code": "NOT_FOUND",
            "message": "task not found"
        }), 404

    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "Request body must be JSON"
        }), 400

    if not data:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "at least one field is required"
        }), 400

    if "title" in data:
        title = data["title"]

        if not isinstance(title, str) or not title.strip():
            return jsonify({
                "code": "VALIDATION_ERROR",
                "message": "Title must be a non-empty string"
            }), 400

        task.title = title.strip()

    if "is_completed" in data:
        is_completed = data["is_completed"]

        if not isinstance(is_completed, bool):
            return jsonify({
                "code": "VALIDATION_ERROR",
                "message": "is_completed must be true or false"
            }), 400

        task.is_completed = is_completed

    db.session.commit()

    return jsonify({
        "id": task.id,
        "title": task.title,
        "is_completed": task.is_completed,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "user_id": task.user_id
    }), 200

@tasks_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@require_auth
def delete_task(task_id):
    task = Task.query.filter_by(
        id=task_id,
        user_id=g.current_user_id
    ).first()

    if task is None:
        return jsonify({
            "code": "NOT_FOUND",
            "message": "task not found"
        }), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "message": "Task deleted successfully"
    }), 200