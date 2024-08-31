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
    def check_role(required_role):
        return session.get('role') == required_role
    # Web Signup route - render signup form and handle form submission
    @app.route('/signup', methods=['GET', 'POST'])
    def signup_page():
        if request.method == 'POST':
            username = request.form.get('user_id')
            email = request.form.get('email')
            password = request.form.get('password')
            role_name = request.form.get('role', 'user')
            if username and email and password:
                existing_user = User.query.filter_by(username=username).first()
                if existing_user:
                    return render_template('register.html', error='User already exists')
                # Ensure role name is correct and exists (case-insensitive lookup)
                role = Role.query.filter(Role.name.ilike(role_name)).first()
                if not role:
                    return render_template('register.html', error='Invalid role')

                # Create a new user and set the password
                new_user = User(username=username, email=email, role_id=role.id)
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
    # Web Login route - render login form and handle form submission
    @app.route('/login', methods=['GET', 'POST'])
    def login_page():
        if request.method == 'POST':
            user_id = request.form.get('user_id')
            password = request.form.get('password')

            user = User.query.filter_by(username=user_id).first()
            if user and user.check_password(password):
                # Set session variables
                session['user_id'] = user.id
                session['role'] = user.role.name  # Store the role name or you can store role.id

                return redirect(url_for('index'))
            else:
                return render_template('login.html', error='Invalid credentials')

        return render_template('login.html')

    # Web Admin Board route - render the admin board page
    @app.route('/admin_board', methods=['GET', 'POST'])
    def admin_board():
        if 'user_id' not in session:
            return redirect(url_for('login_page'))

        user_role = session.get('role')

        if request.method == 'POST':
            if user_role != 'ADMIN':
                return render_template('admin_board.html', messages=[], error='Access Denied')

            content = request.form.get('message')
            user_id = session.get('user_id')

            if user_id and content:
                new_message = Message(content=content, board_type='ADMIN', user_id=user_id)
                db.session.add(new_message)
                db.session.commit()

            return redirect(url_for('admin_board'))

        # Only ADMIN can view the ADMIN board
        if user_role == 'ADMIN':
            messages = Message.query.filter_by(board_type='ADMIN').order_by(Message.timestamp.desc()).all()
            return render_template('admin_board.html', messages=messages)
        else:
            return render_template('admin_board.html', messages=[], error='Access Denied')

    # View and Post on the USER board
    @app.route('/user_board', methods=['GET', 'POST'])
    def user_board():
        if 'user_id' not in session:
            return redirect(url_for('login_page'))

        user_role = session.get('role')

        if request.method == 'POST':
            if user_role not in ['USER', 'EDITOR', 'ADMIN']:
                return render_template('user_board.html', messages=[], error='Access Denied')

            content = request.form.get('message')
            user_id = session.get('user_id')

            if user_id and content:
                new_message = Message(content=content, board_type='USER', user_id=user_id)
                db.session.add(new_message)
                db.session.commit()

            return redirect(url_for('user_board'))

        # Only ADMIN, EDITOR, and USER can view the USER board
        if user_role in ['USER', 'EDITOR', 'ADMIN']:
            messages = Message.query.filter_by(board_type='USER').order_by(Message.timestamp.desc()).all()
            return render_template('user_board.html', messages=messages)
        else:
            return render_template('user_board.html', messages=[], error='Access Denied')

        # View and Post on the EDITOR board

    # View and Post on the EDITOR board
    @app.route('/editor_board', methods=['GET', 'POST'])
    def editor_board():
        if 'user_id' not in session:
            return redirect(url_for('login_page'))

        user_role = session.get('role')

        if request.method == 'POST':
            if user_role not in ['EDITOR', 'ADMIN']:
                return render_template('editor_board.html', messages=[], error='Access Denied')

            content = request.form.get('message')
            user_id = session.get('user_id')

            if user_id and content:
                new_message = Message(content=content, board_type='EDITOR', user_id=user_id)
                db.session.add(new_message)
                db.session.commit()

            return redirect(url_for('editor_board'))

        # Only ADMIN and EDITOR can write on the EDITOR board, USER can only view
        if user_role in ['USER', 'EDITOR', 'ADMIN']:
            messages = Message.query.filter_by(board_type='EDITOR').order_by(Message.timestamp.desc()).all()
            return render_template('editor_board.html', messages=messages, can_post=user_role in ['EDITOR', 'ADMIN'])
        else:
            return render_template('editor_board.html', messages=[], error='Access Denied')

    # Web Logout route - clear session
    @app.route('/logout')
    def logout_page():
        session.clear()
        return redirect(url_for('index'))

    # Root route
    @app.route('/')
    def index():
        print(f"User ID in session: {session.get('user_id')}")
        print(f"User role in session: {session.get('role')}")
        return render_template('index.html')

    """
    
    
    # Web Post Message route - handles posting a message
    @app.route('/post_message', methods=['POST'])
    def post_message():
        content = request.form.get('message')
        # Assuming you have session management to retrieve current user
        user_id = session.get('user_id')

        if user_id and content:
            new_message = Message(content=content, board_type='USER', user_id=user_id)
            db.session.add(new_message)
            db.session.commit()

        return redirect(url_for('user_board'))
   """

