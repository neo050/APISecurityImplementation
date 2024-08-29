from flask import Blueprint, request, jsonify
from .auth import token_required, generate_token, role_required
from .models import db, User, Message

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

    # Editor route - accessible only to users with the 'editor' role
    @auth_bp.route('/editor', methods=['GET'])
    @token_required
    @role_required('editor')
    def editor_route(current_user, current_role):
        return jsonify({'message': f'Welcome, {current_user}, to the editor dashboard!'}), 200

    # Message Board route - allows users to post messages
    @auth_bp.route('/post_message', methods=['POST'])
    @token_required
    def post_message(current_user, current_role):
        data = request.json
        content = data.get('content')
        board_type = data.get('board_type', 'USER')  # Default to 'USER' board

        # Check if user is allowed to post on the Admin board
        if current_role != 'admin' and board_type == 'ADMIN':
            return jsonify({'message': 'Not authorized to post on Admin board'}), 403

        # Create a new message
        new_message = Message(content=content, board_type=board_type, user_id=current_user.id)
        db.session.add(new_message)
        db.session.commit()

        return jsonify({'message': 'Message posted successfully'}), 201

    # View Messages route - allows users to view messages based on board type
    @auth_bp.route('/view_messages/<board_type>', methods=['GET'])
    @token_required
    def view_messages(current_user, current_role, board_type):
        # Admins can view both boards, users only their own board
        if board_type == 'ADMIN' and current_role != 'admin':
            return jsonify({'message': 'Not authorized to view Admin board'}), 403

        messages = Message.query.filter_by(board_type=board_type).order_by(Message.timestamp.desc()).all()
        return jsonify([{'user': msg.author.username, 'content': msg.content, 'timestamp': msg.timestamp} for msg in messages]), 200

    # Register the blueprint with the app
    app.register_blueprint(auth_bp, url_prefix='/api')

    # Root route
    @app.route('/')
    def index():
        return "Welcome to the API Security Implementation", 200
