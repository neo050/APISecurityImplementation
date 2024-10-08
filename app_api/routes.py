from flask import Blueprint, request, jsonify, redirect, url_for, render_template, session,flash
from sqlalchemy.exc import OperationalError, IntegrityError
from .models import db, User, Message, Role
from tenacity import retry, wait_fixed, stop_after_attempt
import logging

# Setup logging for error tracking
logging.basicConfig(level=logging.ERROR)

# Create a Blueprint for the web routes
web_bp = Blueprint('web', __name__)

def init_routes(app):
    # Web Signup route - render signup form and handle form submission
    @web_bp.route('/signup', methods=['GET', 'POST'])
    def signup_page():
        if request.method == 'POST':
            username = request.form.get('user_id')
            email = request.form.get('email')
            password = request.form.get('password')
            role_name = request.form.get('role', 'user')
            try:
                if username and email and password:
                    # Check if the email already exists
                    existing_email = User.query.filter_by(email=email).first()
                    if existing_email:
                        flash('Email is already in use', 'error')
                        return render_template('web/register.html', username=username, email=email, role=role_name)

                    existing_user = User.query.filter_by(username=username).first()
                    if existing_user:
                        flash('User already exists', 'error')
                        return render_template('web/register.html', username=username, email=email, role=role_name)

                    role = Role.query.filter(Role.name.ilike(role_name)).first()
                    if not role:
                        flash('Invalid role', 'error')
                        return render_template('web/register.html', username=username, email=email, role=role_name)

                    new_user = User(username=username, email=email, role_id=role.id)
                    new_user.set_password(password)
                    db.session.add(new_user)
                    db.session.commit()

                    session['user_id'] = new_user.id
                    session['role'] = new_user.role.name.upper()

                    return redirect(url_for('web.index'))
                else:
                    flash('Invalid credentials', 'error')
                    return render_template('web/register.html', username=username, email=email, role=role_name)
            except IntegrityError:
                db.session.rollback()
                logging.error("Duplicate entry for email.", exc_info=True)
                flash('Email is already in use', 'error')
                return render_template('web/register.html', username=username, email=email, role=role_name)
            except OperationalError:
                logging.error("Database connection failed.", exc_info=True)
                flash('Database connection failed. Please try again later.', 'error')
                return render_template('web/register.html', username=username, email=email, role=role_name)

        return render_template('web/register.html')

    # Web Login route - render login form and handle form submission
    @retry(wait=wait_fixed(2), stop=stop_after_attempt(3), reraise=True)
    def get_user(username):
        return User.query.filter_by(username=username).first()

    @web_bp.route('/login', methods=['GET', 'POST'])
    def login_page():
        if request.method == 'POST':
            user_id = request.form.get('user_id')
            password = request.form.get('password')

            try:
                user = get_user(user_id)
                if user and user.check_password(password):
                    session['user_id'] = user.id
                    session['role'] = user.role.name.upper()

                    return redirect(url_for('web.index'))
                else:
                    return render_template('web/login.html', error='Invalid credentials')
            except OperationalError:
                logging.error("Database connection failed.", exc_info=True)
                return render_template('web/login.html', error='Database connection failed. Please try again later.')

        return render_template('web/login.html')

    # Admin Board route
    @web_bp.route('/admin_board', methods=['GET', 'POST'])
    def admin_board():
        if 'user_id' not in session:
            return redirect(url_for('web.login_page'))

        user_role = session.get('role').upper()

        if user_role == 'USER':
            return render_template('web/admin_board.html', messages=[], error='Access Denied')

        try:
            if request.method == 'POST':
                content = request.form.get('message')
                user_id = session.get('user_id')

                if user_id and content:
                    new_message = Message(content=content, board_type='ADMIN', user_id=user_id)
                    db.session.add(new_message)
                    db.session.commit()

                return redirect(url_for('web.admin_board'))

            messages = Message.query.filter_by(board_type='ADMIN').order_by(Message.timestamp.desc()).all()
            can_post = (user_role == 'ADMIN')
            return render_template('web/admin_board.html', messages=messages, can_post=can_post)
        except OperationalError:
            logging.error("Database connection failed.", exc_info=True)
            return render_template('web/admin_board.html', messages=[],
                                   error='Database connection failed. Please try again later.')

    # User Board route
    @web_bp.route('/user_board', methods=['GET', 'POST'])
    def user_board():
        if 'user_id' not in session:
            return redirect(url_for('web.login_page'))

        user_role = session.get('role').upper()

        try:
            if request.method == 'POST':
                if user_role not in ['USER', 'EDITOR', 'ADMIN']:
                    return render_template('web/user_board.html', messages=[], error='Access Denied')

                content = request.form.get('message')
                user_id = session.get('user_id')

                if user_id and content:
                    new_message = Message(content=content, board_type='USER', user_id=user_id)
                    db.session.add(new_message)
                    db.session.commit()

                return redirect(url_for('web.user_board'))

            messages = Message.query.filter_by(board_type='USER').order_by(Message.timestamp.desc()).all()
            can_post = (user_role in ['USER', 'EDITOR', 'ADMIN'])
            return render_template('web/user_board.html', messages=messages, can_post=can_post)
        except OperationalError:
            logging.error("Database connection failed.", exc_info=True)
            return render_template('web/user_board.html', messages=[],
                                   error='Database connection failed. Please try again later.')

    # Editor Board route
    @web_bp.route('/editor_board', methods=['GET', 'POST'])
    def editor_board():
        if 'user_id' not in session:
            return redirect(url_for('web.login_page'))

        user_role = session.get('role').upper()

        try:
            if request.method == 'POST':
                if user_role not in ['EDITOR', 'ADMIN']:
                    return render_template('web/editor_board.html', messages=[], error='Access Denied')

                content = request.form.get('message')
                user_id = session.get('user_id')

                if user_id and content:
                    new_message = Message(content=content, board_type='EDITOR', user_id=user_id)
                    db.session.add(new_message)
                    db.session.commit()

                return redirect(url_for('web.editor_board'))

            messages = Message.query.filter_by(board_type='EDITOR').order_by(Message.timestamp.desc()).all()
            can_post = (user_role in ['EDITOR', 'ADMIN'])
            return render_template('web/editor_board.html', messages=messages, can_post=can_post)
        except OperationalError:
            logging.error("Database connection failed.", exc_info=True)
            return render_template('web/editor_board.html', messages=[],
                                   error='Database connection failed. Please try again later.')

    # Logout route
    @web_bp.route('/logout')
    def logout_page():
        session.clear()
        return redirect(url_for('web.index'))

    # Index page route
    @web_bp.route('/')
    def index():
        return render_template('web/index.html')

    # Register the Blueprint with the app
    app.register_blueprint(web_bp)
