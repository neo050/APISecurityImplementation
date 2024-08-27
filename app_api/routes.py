from flask import Blueprint, request, jsonify
from .auth import token_required, generate_token, role_required

def init_routes(app):
    # Auth blueprint
    auth_bp = Blueprint('auth', __name__)

    # Sign Up route - for creating a token with a role
    @auth_bp.route('/signup', methods=['POST'])
    def signup():
        data = request.json
        user_id = data.get('user_id')
        role = data.get('role', 'user')  # Default role is 'user'
        if user_id:
            token = generate_token(user_id, role)
            return jsonify({'token': token}), 200
        return jsonify({'message': 'Invalid credentials'}), 401

    # Protected route - accessible to any logged-in user
    @auth_bp.route('/login', methods=['GET'])
    @token_required
    def protected_route(current_user, current_role):
        return jsonify({'message': f'Hello, user {current_user} with role {current_role}'}), 200

    # Admin route - accessible only to users with the 'admin' role
    @auth_bp.route('/admin', methods=['GET'])
    @token_required
    @role_required('admin')
    def admin_route(current_user, current_role):
        return jsonify({'message': f'Welcome to the admin dashboard, {current_user}'}), 200

    @auth_bp.route('/editor', methods=['GET'])
    @token_required
    @role_required('editor')
    def editor_route(current_user, current_role):
        return jsonify({'message': f'Welcome, {current_user}, to the editor dashboard!'}), 200

    # Register the blueprint with the app
    app.register_blueprint(auth_bp, url_prefix='/api')

    # Root route
    @app.route('/')
    def index():
        return "Welcome to the API Security Implementation", 200
