from flask_jwt_extended import create_access_token

def generate_access_token(user_id, role, department, college_name):
    """
    Generate JWT access token with user info
    Args:
        user_id (str) - User's MongoDB ObjectId
        role (str) - 'student' or 'admin'
        department (str) - User's department
        college_name (str) - User's college
    Returns: JWT token string
    """
    additional_claims = {
        'role': role,
        'department': department,
        'college_name': college_name
    }
    
    access_token = create_access_token(
        identity=str(user_id),
        additional_claims=additional_claims
    )
    
    return access_token