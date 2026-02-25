from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.student_profile_service import StudentProfileService
from app.middleware.auth_middleware import role_required

student_profile_bp = Blueprint('student_profile', __name__)
student_profile_service = StudentProfileService()


@student_profile_bp.route('/profile', methods=['GET'])
@jwt_required()
@role_required(['student'])
def get_profile():
    """
    Get student profile
    
    Access: Student only
    
    Request Headers:
        Authorization: Bearer <JWT_TOKEN>
    
    Response (200):
        {
            "profile": {
                "studying_year": 2,
                "semester": 3,
                "semester_marks": [88, 92, 85, 90],
                "attendance_percentage": 87.5,
                "interested_domain": "AI/ML",
                "skills": ["Python", "Machine Learning"],
                "passout_year": 2026,
                "created_at": "2025-01-23T10:30:00",
                "updated_at": "2025-01-24T15:45:00"
            }
        }
    
    OR if profile doesn't exist:
        {
            "message": "No profile found. Please create your profile.",
            "profile": {}
        }
    
    Logic:
        1. Extract student_id from JWT token
        2. Validate student exists and has student role
        3. Fetch profile from database
        4. Return profile or empty object
    
    Errors:
        401: Token missing/invalid
        403: Not a student role
        404: Student not found
    """
    try:
        # Get student_id from JWT token
        student_id = get_jwt_identity()
        
        # Call service to get profile
        result = student_profile_service.get_student_profile(student_id)
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch profile',
            'details': str(e)
        }), 500


@student_profile_bp.route('/profile', methods=['PUT'])
@jwt_required()
@role_required(['student'])
def update_profile():
    """
    Create or update student profile
    
    Access: Student only
    
    Request Headers:
        Authorization: Bearer <JWT_TOKEN>
    
    Request Body (all fields optional):
        {
            "studying_year": 2,
            "semester": 3,
            "semester_marks": [88, 92, 85, 90],
            "attendance_percentage": 87.5,
            "interested_domain": "AI/ML",
            "skills": ["Python", "Machine Learning", "Deep Learning"],
            "passout_year": 2026
        }
    
    Response (200):
        {
            "message": "Profile updated successfully",
            "profile": {
                "studying_year": 2,
                "semester": 3,
                "semester_marks": [88, 92, 85, 90],
                "attendance_percentage": 87.5,
                "interested_domain": "AI/ML",
                "skills": ["Python", "Machine Learning", "Deep Learning"],
                "passout_year": 2026
            }
        }
    
    Logic:
        1. Extract student_id from JWT token
        2. Validate request body
        3. Validate each field (type, range, format)
        4. Check if profile exists
        5. Create new profile OR update existing (upsert)
        6. Return success with updated profile
    
    Validation Rules:
        - studying_year: integer (1-5)
        - semester: integer (1-10)
        - semester_marks: array of numbers (0-100)
        - attendance_percentage: float (0-100)
        - interested_domain: non-empty string
        - skills: array of non-empty strings
        - passout_year: integer (current_year to current_year+10)
    
    Errors:
        400: Validation failed
        401: Token missing/invalid
        403: Not a student role
        404: Student not found
        500: Server error
    """
    try:
        # Get student_id from JWT token
        student_id = get_jwt_identity()
        
        # Get request body
        profile_data = request.get_json()
        
        if not profile_data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Call service to create/update profile
        result = student_profile_service.create_or_update_profile(student_id, profile_data)
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({
            'error': 'Failed to update profile',
            'details': str(e)
        }), 500
