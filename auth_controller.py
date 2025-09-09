# import jwt
# from flask import Blueprint, request, jsonify, current_app, render_template
# from datetime import datetime, timedelta
# from infrastructure.models.user_model import User
# from infrastructure.databases.mssql import session
# from api.schemas.auth import RegisterUserRequestSchema, RegisterUserResponseSchema
# from services.auth_service import AuthService
# from infrastructure.repositories.auth_repository import AuthRepository

# bp = Blueprint('auth', __name__, url_prefix='/auth')
# auth_service = AuthService(AuthRepository(session))

# register_request = RegisterUserRequestSchema()
# register_response = RegisterUserResponseSchema()

# @bp.route('/signup', methods=['POST'])
# def register():
#     data = request.get_json()  # Chỉ dùng JSON cho API
#     errors = register_request.validate(data)
#     if errors:
#         return jsonify(errors), 400

#     user_name = data['user_name']
#     password = data['password']
#     email = data['email']
#     password_confirm = data['password_confirm']

#     if password != password_confirm:
#         return jsonify({'error': 'Passwords do not match'}), 400
    
#     if auth_service.check_exist(user_name):
#         return jsonify({'message': 'User already exists. Please login.'}), 400

#     try:
#         user = auth_service.create_user(user_name, password, email)
#         return jsonify(register_response.dump(user)), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# @bp.route('/login', methods=['GET'])
# def login_page():
#     return render_template('login.html')

# @bp.route('/register', methods=['GET'])
# def register_page():
#     return render_template('register.html')
import jwt
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from infrastructure.databases.mssql import session as db_session
from services.auth_service import AuthService
from infrastructure.repositories.auth_repository import AuthRepository

bp = Blueprint("auth", __name__, url_prefix="/auth")
auth_service = AuthService(AuthRepository(db_session))

# ========================
# WEB LOGIN FORM - SIMPLE VERSION
# ========================
@bp.route("/login", methods=["GET"])
def login_form():
    """Hiển thị form login"""
    return render_template("login.html")

@bp.route("/login", methods=["POST"])
def login_form_post():
    """Xử lý form login - KHÔNG parse JSON"""
    print("🔄 POST /auth/login được gọi")
    print(f"Content-Type: {request.content_type}")
    print(f"Method: {request.method}")
    
    # ✅ FORCE parse form data, KHÔNG parse JSON
    try:
        # Chỉ lấy form data, bỏ qua JSON
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        
        print(f"Form Username: {user_name}")
        print(f"Form Password: {'*' * len(password) if password else None}")

        if not user_name or not password:
            flash("Please provide both username and password", "danger")
            return redirect(url_for("auth.login_form"))

        # Thực hiện login
        user = auth_service.login(user_name, password)
        if not user:
            flash("Invalid username or password", "danger")
            return redirect(url_for("auth.login_form"))

        # Lưu session
        session["user_name"] = user_name
        session["user_id"] = getattr(user, 'id', user_name)  # Safer way to get id
        
        flash("Login successful!", "success")
        return redirect(url_for("index"))
        
    except Exception as e:
        print(f"❌ Login error: {e}")
        flash("An error occurred during login", "danger")
        return redirect(url_for("auth.login_form"))

# ========================
# WEB REGISTER FORM
# ========================
@bp.route("/register", methods=["GET"])
def register_form():
    return render_template("register.html")

@bp.route("/register", methods=["POST"]) 
def register_form_post():
    """Xử lý form register"""
    print("🔄 POST /auth/register được gọi")
    
    try:
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")
        email = request.form.get("email")

        print(f"Register attempt: {user_name}")

        if not all([user_name, password, password_confirm, email]):
            flash("All fields are required", "danger")
            return redirect(url_for("auth.register_form"))

        if password != password_confirm:
            flash("Passwords do not match", "danger")
            return redirect(url_for("auth.register_form"))

        if auth_service.check_exist(user_name):
            flash("User already exists", "warning")
            return redirect(url_for("auth.register_form"))

        # Thực hiện register
        user = auth_service.register(user_name, password, email)
        if user:
            flash("Register successful! Please login.", "success")
            return redirect(url_for("auth.login_form"))
        else:
            flash("Registration failed", "danger")
            return redirect(url_for("auth.register_form"))
            
    except Exception as e:
        print(f"❌ Register error: {e}")
        flash("Registration failed", "danger")
        return redirect(url_for("auth.register_form"))

# ========================
# API ROUTES - SEPARATE
# ========================
@bp.route("/api/login", methods=["POST"])
def login_api():
    """API JSON login - chỉ cho API clients"""
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
        
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    user_name = data.get("user_name")
    password = data.get("password")

    if not user_name or not password:
        return jsonify({"error": "Username and password required"}), 400

    try:
        user = auth_service.login(user_name, password)
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        session["user_name"] = user_name
        session["user_id"] = getattr(user, 'id', user_name)

        return jsonify({
            "message": "Login successful", 
            "user": {"user_name": user.user_name}
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@bp.route("/api/register", methods=["POST"])
def register_api():
    """API JSON register - chỉ cho API clients"""
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
        
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    user_name = data.get("user_name")
    password = data.get("password")
    email = data.get("email")
    password_confirm = data.get("password_confirm")

    if not all([user_name, password, email, password_confirm]):
        return jsonify({"error": "All fields required"}), 400

    if password != password_confirm:
        return jsonify({"error": "Passwords do not match"}), 400

    if auth_service.check_exist(user_name):
        return jsonify({"error": "User already exists"}), 400

    try:
        user = auth_service.register(user_name, password, email)
        return jsonify({
            "message": "User created successfully", 
            "user": {"user_name": user.user_name, "email": user.email}
        }), 201
    except Exception as e:
        return jsonify({"error": "Registration failed"}), 500

# ========================
# LOGOUT
# ========================
@bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for("auth.login_form"))

# ========================
# DEBUG
# ========================
@bp.route("/debug")
def debug():
    return jsonify({
        "message": "Auth routes working",
        "session": dict(session),
        "routes": [
            "GET,POST /auth/login - Form login",
            "POST /auth/api/login - JSON API login", 
            "GET,POST /auth/register - Form register",
            "POST /auth/api/register - JSON API register"
        ]
    })