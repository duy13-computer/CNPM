from src.api.controllers.auth_controller import bp as auth_bp

def register_routes(app):
    app.register_blueprint(auth_bp) 