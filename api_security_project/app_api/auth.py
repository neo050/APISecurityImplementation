import jwt
import datetime
from flask import request, jsonify, current_app
from functools import wraps


def generate_token(user_id, role):
    """
    Generates a JWT token for a given user ID and role.
    """
    token = jwt.encode({
        'user_id': user_id,
        'role': role,  # Include the role in the token payload
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get the token from the Authorization header
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        # Split the token from "Bearer <token>"
        if token.startswith('Bearer '):
            token = token.split(' ')[1]
        else:
            return jsonify({'message': 'Token format is invalid!'}), 403

        try:
            # Decode the token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['user_id']
            current_role = data['role']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(current_user, current_role, *args, **kwargs)

    return decorated


def role_required(required_role):
    """
    Decorator to enforce role-based access control.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(current_user, current_role, *args, **kwargs):
            if current_role != required_role:
                return jsonify({'message': f'Access forbidden: {required_role} role required!'}), 403
            return f(current_user, current_role, *args, **kwargs)
        return decorated_function
    return decorator
