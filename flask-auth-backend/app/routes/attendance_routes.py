from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.attendance_service import AttendanceService
from app.services.admin_dashboard_service import AdminDashboardService
from app.middleware.auth_middleware import role_required

# Create Blueprint
attendance_bp = Blueprint('attendance', __name__)

# Services will be initialized inside routes to avoid circular imports/context issues


# ===== ADMIN ROUTES =====

@attendance_bp.route('/admin/attendance/mark', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def mark_attendance():
    """
    Mark attendance for a student (Admin only)
    
    Request Headers:
        Authorization: Bearer <JWT_TOKEN>
    
    Request Body:
        {
            "student_id": "65b0f1a2c3d4e5f6a7b8c9d0",
            "date": "2025-01-23",
            "status": "present"
        }
    """
    try:
        admin_id = get_jwt_identity()
        data = request.get_json()
        
        student_id = data.get('student_id')
        date = data.get('date')
        status = data.get('status')
        
        if not all([student_id, date, status]):
            return jsonify({
                'error': 'Missing required fields',
                'required': ['student_id', 'date', 'status']
            }), 400
        
        attendance_service = AttendanceService()
        result = attendance_service.mark_attendance(
            student_id=student_id,
            date=date,
            status=status,
            admin_id=admin_id
        )
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({
            'error': 'Failed to mark attendance',
            'details': str(e)
        }), 500


@attendance_bp.route('/admin/attendance/summary', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_attendance_summary():
    """
    Get attendance summary dashboard for admin's department
    
    Access: Admin only
    
    Request Headers:
        Authorization: Bearer <ADMIN_JWT_TOKEN>
    
    Response (200):
        {
            "department": "MCA",
            "college_name": "SNS",
            "summary": {
                "total_students": 60,
                "present_today": 52,
                "absent_today": 8,
                "average_attendance": 82.4,
                "students_below_75": 11
            },
            "defaulters": [...]
        }
    """
    try:
        admin_id = get_jwt_identity()
        # Initialize service here
        admin_dashboard_service = AdminDashboardService()
        result = admin_dashboard_service.get_attendance_summary(admin_id)
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch attendance summary',
            'details': str(e)
        }), 500


# ===== STUDENT ROUTES =====

@attendance_bp.route('/student/attendance', methods=['GET'])
@jwt_required()
@role_required(['student'])
def get_my_attendance():
    """
    Get own attendance (Student only)
    
    Request Headers:
        Authorization: Bearer <JWT_TOKEN>
    """
    try:
        student_id = get_jwt_identity()
        attendance_service = AttendanceService()
        result = attendance_service.get_student_attendance(student_id)
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch attendance',
            'details': str(e)
        }), 500