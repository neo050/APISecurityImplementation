# app/routes.py

from flask import Blueprint, request, jsonify
from auth import generate_token, token_required  # Absolute import

def init_routes(app):
    auth_bp = Blueprint('auth', __name__)

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

    app.register_blueprint(auth_bp, url_prefix='/api')
