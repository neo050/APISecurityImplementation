from flask import Blueprint, request, jsonify
from api_security_project.app_api.auth import token_required, generate_token

def init_routes(app):
    # Auth blueprint
    auth_bp = Blueprint('auth', __name__)

    # Define routes for the auth blueprint
    @auth_bp.route('/login', methods=['POST'])
    def login():
        data = request.json
        user_id = data.get('user_id')
        if user_id:
            token = generate_token(user_id)
            return jsonify({'token': token}), 200
        return jsonify({'message': 'Invalid credentials'}), 401

    @auth_bp.route('/protected', methods=['GET'])
    @token_required
    def protected_route(current_user):
        return jsonify({'message': f'Hello, user {current_user}'}), 200

    # Define additional routes for the auth blueprint before registration
    @auth_bp.route('/login-test', methods=['GET'])
    def login_test():
        return "This is a test route for GET requests", 200

    # Register the blueprint with the app
    app.register_blueprint(auth_bp, url_prefix='/api')

    # Root route
    @app.route('/')
    def index():
        return "Welcome to the API Security Implementation", 200
