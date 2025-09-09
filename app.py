# import os
# from flask import Flask, jsonify, render_template
# from api.swagger import spec
# from api.controllers.todo_controller import bp as todo_bp
# from api.controllers.auth_controller import bp as auth_bp
# from api.controllers.user_controller import bp as user_bp
# from api.controllers.watch_controller import bp as watch_bp
# from infrastructure.databases import init_db
# from config import Config, SwaggerConfig
# from flasgger import Swagger
# from flask_swagger_ui import get_swaggerui_blueprint

# def create_app():
#     BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Thư mục src
#     TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
#     STATIC_DIR = os.path.join(BASE_DIR, 'static')

#     print(f"📂 Template dir: {TEMPLATES_DIR}")   # <-- In ra đường dẫn
#     print(f"📂 Static dir:   {STATIC_DIR}")     # <-- In ra đường dẫn

#     app = Flask(
#         __name__,
#         template_folder=os.path.join(BASE_DIR, "templates"),
#         static_folder=os.path.join(BASE_DIR, "static")
#     )
#     app.config.from_object(Config)

#     # Khởi tạo DB
#     init_db(app)

#     # Đăng ký blueprints
#     app.register_blueprint(todo_bp)
#     app.register_blueprint(auth_bp)
#     app.register_blueprint(user_bp)
#     app.register_blueprint(watch_bp)

#     # Swagger
#     Swagger(app, template=SwaggerConfig.template, config=SwaggerConfig.swagger_config)
#     SWAGGER_URL = '/api/docs'
#     API_URL = '/swagger.json'
#     swaggerui_bp = get_swaggerui_blueprint(
#         SWAGGER_URL,
#         API_URL,
#         config={"app_name": "Flask Clean Architecture API"}
#     )
#     app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

#     # JSON spec cho swagger
#     @app.route('/swagger.json')
#     def swagger_json():
#         return jsonify(spec.to_dict())

#     # Trang chủ
#     @app.route('/')
#     def index():
#         return render_template('index.html')

#     @app.route('/api/test', methods=['GET'])
#     def test_api():
#         return jsonify({"message": "API is working!"})

#     return app

# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True, host="0.0.0.0", port=5000)
import traceback
import os
from flask import Flask, render_template, redirect, url_for, session
from infrastructure.databases import init_db
from config import SwaggerConfig
from flasgger import Swagger as Swager
from flask_swagger_ui import get_swaggerui_blueprint

def create_app():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
    STATIC_DIR = os.path.join(BASE_DIR, 'static')

    app = Flask(
        __name__,
        template_folder=TEMPLATES_DIR,
        static_folder=STATIC_DIR
    )
    app.secret_key = "supersecretkey"

    print(f"🚀 Flask app starting...")

    # Init DB
    try:
        init_db(app)
        print("✅ Database initialized")
    except Exception as e:
        print(f"❌ Database error: {e}")

    # Register blueprints
    try:
        from api.controllers.auth_controller import bp as auth_bp
        app.register_blueprint(auth_bp)
        print("✅ Auth blueprint registered")
    except Exception as e:
        print(f"❌ Auth blueprint error: {e}")

    try:
        from api.controllers.todo_controller import bp as todo_bp
        app.register_blueprint(todo_bp)
        print("✅ Todo blueprint registered")
    except Exception as e:
        print(f"❌ Todo blueprint error: {e}")

    try:
        from api.controllers.user_controller import bp as user_bp
        app.register_blueprint(user_bp)
        print("✅ User blueprint registered")  
    except Exception as e:
        print(f"❌ User blueprint error: {e}")
        traceback.print_exc()

    try:
        from api.controllers.watch_controller import bp as watch_bp
        app.register_blueprint(watch_bp)
        print("✅ Watch blueprint registered")
    except Exception as e:
        print(f"❌ Watch blueprint error: {e}")

    # Main routes
    @app.route('/')
    def index():
        print(f"🏠 Index accessed, session: {dict(session)}")
        if 'user_name' not in session:
            print("❌ No session, redirect to login")
            # 🔥 Sửa lại redirect tới user.login_form thay vì auth.login_form
            return redirect(url_for('user.login_form'))
        print("✅ User logged in")
        return render_template('index.html', user_name=session.get('user_name'))

    @app.route('/debug')
    def debug():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(f"{rule.rule} -> {rule.endpoint} {list(rule.methods)}")
        return {
            'app': 'Flask Clean Architecture',
            'session': dict(session),
            'routes': routes
        }
    @app.route("/routes")
    def show_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
            "path": rule.rule,
            "endpoint": rule.endpoint,
            "methods": list(rule.methods)
        })
        return {"routes": routes}
    # ✅ Print all registered routes
    print("\n🔗 All Routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} [{', '.join(rule.methods)}] -> {rule.endpoint}")
    print()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)