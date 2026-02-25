from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.student_controller import StudentController
from app.middleware.auth_middleware import role_required

student_bp = Blueprint('student', __name__)
student_controller = StudentController()

@student_bp.route('/profile', methods=['GET'])
@jwt_required()
@role_required(['student'])
def get_profile():
    """
    Get student profile (JWT required, Student only)
    
    Headers:
    Authorization: Bearer <JWT_TOKEN>
    """
    try:
        user_id = get_jwt_identity()
        result = student_controller.get_profile(user_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to fetch profile', 'details': str(e)}), 500

@student_bp.route('/profile', methods=['POST'])
@jwt_required()
@role_required(['student'])
def update_profile():
    """
    Create or update student profile (JWT required, Student only)
    
    Headers:
    Authorization: Bearer <JWT_TOKEN>
    
    Request Body:
    {
        "studying_year": 2,
        "semester": 3,
        "semester_marks": [85, 90, 78],
        "attendance_percentage": 85.5,
        "interested_domain": "AI/ML",
        "skills": ["Python", "Machine Learning"],
        "passout_year": 2026
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        result = student_controller.update_profile(user_id, data)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to update profile', 'details': str(e)}), 500

@student_bp.route('/user-info', methods=['PUT'])
@jwt_required()
@role_required(['student'])
def update_user_info():
    """
    Update user basic info (name, phone)
    
    Headers:
    Authorization: Bearer <JWT_TOKEN>
    
    Request Body:
    {
        "name": "Updated Name",
        "phone": "9876543210"
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        result = student_controller.update_user_info(user_id, data)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to update user info', 'details': str(e)}), 500