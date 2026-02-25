from flask import Blueprint, jsonify
from bson import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.student_profile import StudentProfile
from app.models.attendance import Attendance
from app.models.student_alert import StudentAlert
from app.models.task_reminder import Task
from app.middleware.auth_middleware import role_required

student_dashboard_bp = Blueprint('student_dashboard', __name__)

@student_dashboard_bp.route('/dashboard/overview', methods=['GET'])
@jwt_required()
@role_required(['student'])
def get_dashboard_overview():
    """
    Get aggregated dashboard overview data
    
    Response:
    {
        "profile": {
            "name": "Student Name",
            "department": "CSE",
            "year": "3rd Year",
            "attendance_percentage": 85.5
        },
        "stats": {
            "attendance": 85.5,
            "tasks_pending": 3,
            "alerts_unread": 2,
            "student_type": "Advanced"
        }
    }
    """
    try:
        user_id = get_jwt_identity()
        
        # Initialize models
        profile_model = StudentProfile()
        attendance_model = Attendance()
        alert_model = StudentAlert()
        task_model = Task()
        
        # 1. Fetch Profile Data
        profile = profile_model.find_by_user_id(user_id)
        from app.models.user import User
        user = User().find_by_id(user_id)
        
        # 1.5 Proactive Alert Generation
        # Ensure alerts are up-to-date whenever student loads dashboard
        from app.services.alerts.alert_generator import AlertGenerator
        alert_generator = AlertGenerator()
        alert_generator.generate_alerts_for_student(user_id)
        
        # 2. Fetch Stats
        tasks_pending = task_model.collection.count_documents({
            'user_id': ObjectId(user_id), 
            'status': {'$ne': 'completed'}
        })
        
        alerts_unread = alert_model.count_unread(user_id)
        
        attendance_percentage = 0
        if profile and 'attendance_percentage' in profile:
            attendance_percentage = profile['attendance_percentage']
        
        # Determine student type based on MARKS (not attendance)
        from app.utils.learner_classifier import calculate_average_marks, classify_learner
        
        student_type = "Intermediate Learner" # Default
        if profile:
            semester_marks = profile.get('semester_marks', [])
            avg_marks = calculate_average_marks(semester_marks)
            student_type = classify_learner(avg_marks)
            
        return jsonify({
            'profile': {
                'name': user['name'],
                'department': user.get('department', 'N/A'),
                'year': f"{profile.get('studying_year', 1)}rd Year" if profile else "1st Year",
                'attendance_percentage': attendance_percentage
            },
            'stats': {
                'attendance': attendance_percentage,
                'tasks_pending': tasks_pending,
                'alerts_unread': alerts_unread,
                'student_type': student_type,
                'average_marks': avg_marks if 'avg_marks' in locals() else 0.0
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch dashboard overview', 'details': str(e)}), 500
