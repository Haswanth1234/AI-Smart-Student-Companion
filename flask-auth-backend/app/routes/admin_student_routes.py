from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.admin_student_service import AdminStudentService
from app.middleware.auth_middleware import role_required

admin_student_bp = Blueprint('admin_students', __name__)
admin_student_service = AdminStudentService()


@admin_student_bp.route('/admin/students', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_students_list():
    """
    Get all students in admin's department and college
    
    Access: Admin only
    
    Request Headers:
        Authorization: Bearer <ADMIN_JWT_TOKEN>
    
    Response (200):
        {
            "department": "MCA",
            "college_name": "SNS",
            "statistics": {
                "total_students": 45,
                "students_with_profile": 30,
                "students_without_profile": 15
            },
            "students": [
                {
                    "id": "65b0f1a2c3d4e5f6a7b8c9d0",
                    "name": "Haswanth",
                    "email": "haswanth@student.com",
                    "phone": "9876543210",
                    "roll_number": "MCA2024001",
                    "department": "MCA",
                    "college_name": "SNS",
                    "profile_completed": true,
                    "attendance_percentage": 87.5,
                    "studying_year": 2,
                    "semester": 3,
                    "interested_domain": "AI/ML",
                    "registered_on": "2025-01-20T10:30:00"
                }
            ]
        }
    
    Logic:
        1. Extract admin_id from JWT token
        2. Get admin's department & college from database
        3. Query all students with matching department & college
        4. Join with student_profiles for attendance data
        5. Sort by name alphabetically
        6. Return formatted list
    
    Security:
        - JWT required
        - Admin role required
        - Shows only students in admin's department
    
    Errors:
        401: Token missing/invalid
        403: Not an admin
        404: Admin not found
        500: Server error
    """
    try:
        # Get admin_id from JWT token
        admin_id = get_jwt_identity()
        
        # Get students list
        result = admin_student_service.get_students_list(admin_id)
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch students',
            'details': str(e)
        }), 500


@admin_student_bp.route('/admin/students/<student_id>', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_student_details(student_id):
    """
    Get detailed information about a specific student
    
    Access: Admin only (same department)
    
    Request Headers:
        Authorization: Bearer <ADMIN_JWT_TOKEN>
    
    URL Parameters:
        student_id: Student's user ID
    
    Response (200):
        {
            "student_info": {
                "id": "65b0f1a2c3d4e5f6a7b8c9d0",
                "name": "Haswanth",
                "email": "haswanth@student.com",
                "phone": "9876543210",
                "roll_number": "MCA2024001",
                "department": "MCA",
                "college_name": "SNS",
                "profile_completed": true,
                "registered_on": "2025-01-20T10:30:00"
            },
            "profile": {
                "studying_year": 2,
                "semester": 3,
                "semester_marks": [88, 92, 85],
                "attendance_percentage": 87.5,
                "interested_domain": "AI/ML",
                "skills": ["Python", "Machine Learning"],
                "passout_year": 2026
            },
            "attendance_summary": {
                "total_records": 45,
                "recent_attendance": [
                    {"date": "2025-01-23", "status": "present"},
                    {"date": "2025-01-22", "status": "present"}
                ]
            }
        }
    
    Logic:
        1. Validate admin and student exist
        2. Verify student is in admin's department
        3. Fetch complete student profile
        4. Fetch attendance summary
        5. Return detailed view
    
    Errors:
        401: Token missing/invalid
        403: Not an admin or student not in department
        404: Student not found
    """
    try:
        # Get admin_id from JWT token
        admin_id = get_jwt_identity()
        
        # Get student details
        result = admin_student_service.get_student_details(admin_id, student_id)
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch student details',
            'details': str(e)
        }), 500