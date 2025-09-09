# from flask import Blueprint, request, jsonify
# from services.user_service import UserService
# from infrastructure.repositories.user_repository import UserRepository
# from api.schemas.user import UserRequestSchema, UserResponseSchema
# from infrastructure.databases.mssql import session

# bp = Blueprint("user", __name__, url_prefix="/users")

# request_schema = UserRequestSchema()
# response_schema = UserResponseSchema()

# @bp.route("/", methods=["GET"])
# def list_users():
#     db = session()
#     service = UserService(UserRepository(db))
#     users = service.list_users()
#     return jsonify([
#         {
#             "id": u.id,
#             "user_name": u.user_name,
#             "description": u.description,
#             "status": u.status
#         }
#         for u in users
#     ])

# @bp.route("/register", methods=["POST"])
# def register():
#     data = request.json
#     db = session()
#     service = UserService(UserRepository(db))
#     try:
#         user = service.create_user(
#             user_name=data["user_name"],
#             password=data["password"],
#             description=data.get("description"),
#             status=data.get("status", True)
#         )
#         return jsonify({"message": "User created", "id": user.id}), 201
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 400

# @bp.route("/login", methods=["POST"])
# def login():
#     data = request.json
#     db = session()
#     service = UserService(UserRepository(db))
#     user = service.authenticate_user(data["user_name"], data["password"])
#     if not user:
#         return jsonify({"error": "Invalid username or password"}), 401
#     return jsonify({"message": "Login successful", "id": user.id}), 200

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from services.user_service import UserService
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.databases.mssql import session as db_session
from domain.models.user import UserRole


bp = Blueprint("user", __name__, url_prefix="/users")

# ========================
# FORM ROUTES (WEB)
# ========================
@bp.route("/login/form", methods=["GET"])
def login_form():
    """Hiển thị form login"""
    return render_template("login.html")

@bp.route("/login/form", methods=["POST"])
def login_form_post():
    """Xử lý login từ form"""
    user_name = request.form.get("user_name")
    password = request.form.get("password")

    if not user_name or not password:
        flash("Please provide both username and password", "danger")
        return redirect(url_for("user.login_form"))

    db = db_session
    service = UserService(UserRepository(db))
    user = service.authenticate_user(user_name, password)

    if not user:
        flash("Invalid username or password", "danger")
        return redirect(url_for("user.login_form"))

    # Lưu session
    session["user_name"] = user.user_name
    session["user_id"] = user.id

    flash("Login successful!", "success")
    return redirect(url_for("index"))


@bp.route("/register/form", methods=["GET"])
def register_form():
    """Hiển thị form đăng ký"""
    return render_template("register.html")

@bp.route("/register/form", methods=["POST"])
def register_form_post():
    user_name = request.form.get("user_name")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if password != confirm_password:
        flash("Passwords do not match", "danger")
        return redirect(url_for("user.register_form"))

    try:
        service = UserService(UserRepository(db_session))
        new_user = service.create_user(
            user_name=user_name,
            email=email,
            password=password,
            role="user"  # hoặc UserRole.USER nếu enum
        )

        flash("Register successfully!", "success")
        return redirect(url_for("user.login_form"))

    except Exception as e:
        db_session.rollback()
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("user.register_form"))

# ========================
# API ROUTES (JSON)
# ========================
@bp.route("/", methods=["GET"])
def list_users():
    db = db_session
    service = UserService(UserRepository(db))
    users = service.list_users()
    return jsonify([
        {
            "id": u.id,
            "user_name": u.user_name,
            "description": u.description,
            "status": u.status
        }
        for u in users
    ])


@bp.route("/register", methods=["POST"])
def register():
    data = request.json
    db = db_session
    service = UserService(UserRepository(db))
    try:
        user = service.create_user(
            user_name=data["user_name"],
            password=data["password"],
            description=data.get("description"),
            status=data.get("status", True)
        )
        return jsonify({"message": "User created", "id": user.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/login", methods=["POST"])
def login():
    data = request.json
    db = db_session
    service = UserService(UserRepository(db))
    user = service.authenticate_user(data["user_name"], data["password"])
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401
    return jsonify({"message": "Login successful", "id": user.id}), 200

