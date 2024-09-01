from flask import Blueprint, request, jsonify, redirect, url_for, render_template, session
from sqlalchemy.exc import OperationalError
from .models import db, User, Message, Role
from tenacity import retry, wait_fixed, stop_after_attempt
from sqlalchemy.exc import OperationalError


def init_routes(app):
    # Web Signup route - render signup form and handle form submission
    @app.route('/signup', methods=['GET', 'POST'])
    def signup_page():
        if request.method == 'POST':
            username = request.form.get('user_id')
            email = request.form.get('email')
            password = request.form.get('password')
            role_name = request.form.get('role', 'user')
            try:
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
                    session['role'] = new_user.role.name.upper()

                    return redirect(url_for('index'))
                else:
                    return render_template('register.html', error='Invalid credentials')
            except OperationalError:
                return render_template('register.html', error='Database connection failed. Please try again later.')

        return render_template('register.html')

    # Web Login route - render login form and handle form submission
    @retry(wait=wait_fixed(2), stop=stop_after_attempt(3), reraise=True)
    def get_user(username):
        return User.query.filter_by(username=username).first()

    # Example usage in a route
    @app.route('/login', methods=['GET', 'POST'])
    def login_page():
        if request.method == 'POST':
            user_id = request.form.get('user_id')
            password = request.form.get('password')

            try:
                user = get_user(user_id)
                if user and user.check_password(password):
                    session['user_id'] = user.id
                    session['role'] = user.role.name.upper()

                    return redirect(url_for('index'))
                else:
                    return render_template('login.html', error='Invalid credentials')
            except OperationalError:
                return render_template('login.html', error='Database connection failed. Please try again later.')
        else:
            # Handle GET request
            return render_template('login.html')
    # View and Post on the ADMIN board
    # View and Post on the ADMIN board
    @app.route('/admin_board', methods=['GET', 'POST'])
    def admin_board():
        if 'user_id' not in session:
            return redirect(url_for('login_page'))

        user_role = session.get('role').upper()

        # Only allow access if the user is an ADMIN or EDITOR
        if user_role == 'USER':
            return render_template('index.html', error='Access Denied: You do not have permission to view the Admin Board.')

        try:
            if request.method == 'POST':
                content = request.form.get('message')
                user_id = session.get('user_id')

                if user_id and content:
                    new_message = Message(content=content, board_type='ADMIN', user_id=user_id)
                    db.session.add(new_message)
                    db.session.commit()

                return redirect(url_for('admin_board'))

            messages = Message.query.filter_by(board_type='ADMIN').order_by(Message.timestamp.desc()).all()
            can_post = (user_role == 'ADMIN')
            return render_template('admin_board.html', messages=messages, can_post=can_post)
        except OperationalError:
            return render_template('admin_board.html', messages=[],
                                   error='Database connection failed. Please try again later.')

    # View and Post on the USER board
    @app.route('/user_board', methods=['GET', 'POST'])
    def user_board():
        if 'user_id' not in session:
            return redirect(url_for('login_page'))

        user_role = session.get('role').upper()

        try:
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

            messages = Message.query.filter_by(board_type='USER').order_by(Message.timestamp.desc()).all()
            can_post = (user_role in ['USER', 'EDITOR', 'ADMIN'])
            return render_template('user_board.html', messages=messages, can_post=can_post)
        except OperationalError:
            return render_template('user_board.html', messages=[], error='Database connection failed. Please try again later.')

    # View and Post on the EDITOR board
    @app.route('/editor_board', methods=['GET', 'POST'])
    def editor_board():
        if 'user_id' not in session:
            return redirect(url_for('login_page'))

        user_role = session.get('role').upper()

        try:
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

            messages = Message.query.filter_by(board_type='EDITOR').order_by(Message.timestamp.desc()).all()
            can_post = (user_role in ['EDITOR', 'ADMIN'])
            return render_template('editor_board.html', messages=messages, can_post=can_post)
        except OperationalError:
            return render_template('editor_board.html', messages=[], error='Database connection failed. Please try again later.')

    # Web Logout route - clear session
    @app.route('/logout')
    def logout_page():
        session.clear()
        return redirect(url_for('index'))

    # Root route
    @app.route('/')
    def index():
        return render_template('index.html')
