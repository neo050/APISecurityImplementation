from flask import Blueprint, request, jsonify, redirect, url_for, render_template, session
from .auth import token_required, generate_token, role_required
from .models import db, User, Message, Role


def init_routes(app):
    # --------------------
    # API Routes
    # --------------------
    api_bp = Blueprint('api', __name__, url_prefix='/api')

    # (API routes remain unchanged)

    # Register the API blueprint
    app.register_blueprint(api_bp)

    # --------------------
    # Web Routes
    # --------------------

    # Web Signup route - render signup form and handle form submission
    @app.route('/signup', methods=['GET', 'POST'])
    def signup_page():
        if request.method == 'POST':
            username = request.form.get('user_id')  # This should match the form field name 'user_id'
            password = request.form.get('password')
            role_name = request.form.get('role', 'user')

            if username and password:
                existing_user = User.query.filter_by(username=username).first()
                if existing_user:
                    return render_template('register.html', error='User already exists')

                # Find the role by name
                role = Role.query.filter_by(name=role_name).first()
                if not role:
                    return render_template('register.html', error='Invalid role')

                # Create a new user and set the password
                new_user = User(username=username, role_id=role.id)
                new_user.set_password(password)  # Hash and set the password

                db.session.add(new_user)
                db.session.commit()

                session['user_id'] = new_user.id
                session['role'] = new_user.role_id

                return redirect(url_for('index'))
            else:
                return render_template('register.html', error='Invalid credentials')

        return render_template('register.html')

    # Web Login route - render login form and handle form submission
    @app.route('/login', methods=['GET', 'POST'])
    def login_page():
        if request.method == 'POST':
            user_id = request.form.get('user_id')
            password = request.form.get('password')


            user = User.query.filter_by(username=user_id).first()
            if user and user.verify_password(password):
                # Set session variables
                session['user_id'] = user.id
                session['role'] = user.role

                return redirect(url_for('index'))
            else:
                return render_template('login.html', error='Invalid credentials')

        return render_template('login.html')

    # Web Admin Board route - render the admin board page
    @app.route('/admin_board', methods=['GET'])
    def admin_board():
        messages = Message.query.filter_by(board_type='ADMIN').order_by(Message.timestamp.desc()).all()
        return render_template('admin_board.html', messages=messages)

    # Web User Board route - render the user board page
    @app.route('/user_board', methods=['GET', 'POST'])
    def user_board():
        if request.method == 'POST':
            content = request.form.get('message')
            # Assuming you have session management to retrieve current user
            user_id = session.get('user_id')
            role = session.get('role')

            if user_id and content:
                new_message = Message(content=content, board_type='USER', user_id=user_id)
                db.session.add(new_message)
                db.session.commit()

            return redirect(url_for('user_board'))

        messages = Message.query.filter_by(board_type='USER').order_by(Message.timestamp.desc()).all()
        return render_template('user_board.html', messages=messages)

    # Web Logout route - clear session
    @app.route('/logout')
    def logout_page():
        session.clear()
        return redirect(url_for('index'))

    # Root route
    @app.route('/')
    def index():
        return render_template('index.html')
