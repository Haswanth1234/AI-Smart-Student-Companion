from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.alerts.alert_generator import AlertGenerator
from app.models.student_alert import StudentAlert
from app.middleware.auth_middleware import role_required
from bson import ObjectId

alerts_bp = Blueprint('alerts', __name__)
alert_generator = AlertGenerator()
alert_model = StudentAlert()


@alerts_bp.route('/student/alerts/generate', methods=['POST'])
@jwt_required()
@role_required(['student'])
def generate_alerts():
    """
    Generate alerts for current student
    
    POST /api/student/alerts/generate
    """
    try:
        user_id = get_jwt_identity()
        alert_ids = alert_generator.generate_alerts_for_student(user_id)
        
        return jsonify({
            'message': f'{len(alert_ids)} alert(s) generated',
            'alert_count': len(alert_ids)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to generate alerts', 'details': str(e)}), 500


@alerts_bp.route('/student/alerts', methods=['GET'])
@jwt_required()
@role_required(['student'])
def get_alerts():
    """
    Get all alerts for current student
    
    GET /api/student/alerts
    GET /api/student/alerts?unread_only=true
    """
    try:
        user_id = get_jwt_identity()
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        
        if unread_only:
            alerts = alert_model.find_unread_by_user(user_id)
        else:
            alerts = alert_model.find_all_by_user(user_id)
        
        formatted_alerts = []
        for alert in alerts:
            formatted_alerts.append({
                'id': str(alert['_id']),
                'type': alert['alert_type'],
                'severity': alert['severity'],
                'title': alert['title'],
                'message': alert['message'],
                'is_read': alert['is_read'],
                'created_at': alert['created_at'].isoformat(),
                'status': alert.get('status', 'pending'),
                'resolution_notes': alert.get('resolution_notes'),
                'resolved_at': alert.get('resolved_at').isoformat() if alert.get('resolved_at') else None,
                'context': alert.get('context', {})
            })
        
        unread_count = alert_model.count_unread(user_id)
        
        return jsonify({
            'alerts': formatted_alerts,
            'total': len(formatted_alerts),
            'unread_count': unread_count
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch alerts', 'details': str(e)}), 500


@alerts_bp.route('/student/alerts/<alert_id>/read', methods=['PUT'])
@jwt_required()
@role_required(['student'])
def mark_alert_read(alert_id):
    """
    Mark an alert as read
    
    PUT /api/student/alerts/<alert_id>/read
    """
    try:
        alert_model.mark_as_read(alert_id)
        
        return jsonify({'message': 'Alert marked as read'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to mark alert', 'details': str(e)}), 500