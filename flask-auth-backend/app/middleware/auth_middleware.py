from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity

def jwt_required_custom(fn):
    """
    Custom JWT required decorator
    Verifies JWT token and extracts user info
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return fn(*args, **kwargs)
    return wrapper

def role_required(allowed_roles):
    """
    Role-based access control decorator
    Args: allowed_roles (list) - List of allowed roles ['student', 'admin']
    Usage: @role_required(['student'])
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # First verify JWT token exists
            verify_jwt_in_request()
            
            # Get claims from token
            claims = get_jwt()
            user_role = claims.get('role')
            
            # Fallback if claims missing
            if not user_role or user_role is None:
                from app.models.user import User
                user_id = get_jwt_identity()
                print(f"DEBUG: Middleware fallback for user_id: {user_id}")
                user = User().find_by_id(user_id)
                if user:
                    user_role = user['role']
                    print(f"DEBUG: Found user role: {user_role}")
                else:
                    print("DEBUG: User not found in middleware fallback")

            # Check if user's role is allowed
            print(f"DEBUG: Checking role {user_role} against {allowed_roles}")
            if user_role not in allowed_roles:
                return jsonify({
                    'error': 'Access denied',
                    'message': f'This endpoint is only accessible to {", ".join(allowed_roles)}'
                }), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def get_current_user():
    """
    Get current user info from JWT token
    Returns: dict with user_id, role, department, college_name
    """
    claims = get_jwt()
    user_id = get_jwt_identity()
    
    role = claims.get('role')
    department = claims.get('department')
    college_name = claims.get('college_name')
    
    # Fallback if claims missing
    if not role:
        from app.models.user import User
        user = User().find_by_id(user_id)
        if user:
            role = user['role']
            department = user.get('department')
            college_name = user.get('college_name')
    
    return {
        'user_id': user_id,
        'role': role,
        'department': department,
        'college_name': college_name
    }