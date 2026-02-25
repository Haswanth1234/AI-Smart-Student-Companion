from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from app.services.admin_dashboard_service import AdminDashboardService
from app.middleware.auth_middleware import role_required

admin_dashboard_bp = Blueprint('admin_dashboard', __name__)
dashboard_service = AdminDashboardService()

@admin_dashboard_bp.route('/dashboard/overview', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_dashboard_overview():
    """
    Get Admin Dashboard Overview
    Returns statistics for the admin's department
    """
    try:
        # Get admin details from JWT
        claims = get_jwt()
        department = claims.get('department')
        college_name = claims.get('college_name')
        
        if not department or not college_name:
            return jsonify({'error': 'Admin setup incomplete: Missing department or college'}), 400
            
        # Get overview data
        data = dashboard_service.get_overview(department, college_name)
        
        return jsonify(data), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to fetch dashboard data', 'details': str(e)}), 500

@admin_dashboard_bp.route('/dashboard/tasks', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_student_tasks():
    """
    Get all tasks for students in the admin's department
    """
    try:
        claims = get_jwt()
        department = claims.get('department')
        college_name = claims.get('college_name')
        
        if not department or not college_name:
            # Fallback if claims missing (rare)
            return jsonify({'error': 'Admin context missing'}), 400

        # Fix: Ensure service is initialized here if moved
        # But dashboard_service is global in this file? 
        # Better to initialize locally to be safe like in attendance routes
        local_service = AdminDashboardService()
        tasks = local_service.get_student_tasks(department, college_name)
        
        return jsonify(tasks), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch student tasks', 'details': str(e)}), 500

@admin_dashboard_bp.route('/dashboard/alerts', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_student_alerts():
    """
    Get all alerts for students in the admin's department
    """
    try:
        claims = get_jwt()
        department = claims.get('department')
        college_name = claims.get('college_name')
        
        if not department or not college_name:
            return jsonify({'error': 'Admin context missing'}), 400

        local_service = AdminDashboardService()
        alerts = local_service.get_all_student_alerts(department, college_name)
        
        return jsonify(alerts), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch student alerts', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Failed to fetch student alerts', 'details': str(e)}), 500

@admin_dashboard_bp.route('/dashboard/alerts/<alert_id>/resolve', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def resolve_student_alert(alert_id):
    """
    Mark an alert as resolved
    """
    try:
        # Get admin_id from JWT
        admin_id = get_jwt_identity()
        data = request.get_json()
        resolution_notes = data.get('notes', '')
        
        local_service = AdminDashboardService()
        success = local_service.resolve_alert(alert_id, resolution_notes, admin_id)
        
        if success:
            return jsonify({'message': 'Alert resolved successfully'}), 200
        else:
            return jsonify({'error': 'Failed to resolve alert'}), 400
            
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to resolve alert', 'details': str(e)}), 500

@admin_dashboard_bp.route('/dashboard/tasks', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def create_student_task():
    """
    Create a new task for a student
    """
    try:
        admin_id = get_jwt_identity()
        data = request.get_json()
        
        # Basic validation
        if not data.get('title') or not data.get('student_id') or not data.get('due_date'):
            return jsonify({'error': 'Missing required fields (title, student_id, due_date)'}), 400
            
        local_service = AdminDashboardService()
        task_id = local_service.create_task(data, admin_id)
        
        return jsonify({'message': 'Task created successfully', 'task_id': task_id}), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to create task', 'details': str(e)}), 500

@admin_dashboard_bp.route('/dashboard/tasks/<task_id>', methods=['PUT'])
@jwt_required()
@role_required(['admin'])
def update_student_task(task_id):
    """
    Update an existing task
    """
    try:
        data = request.get_json()
        
        local_service = AdminDashboardService()
        success = local_service.update_task(task_id, data)
        
        if success:
            return jsonify({'message': 'Task updated successfully'}), 200
        else:
            return jsonify({'error': 'Task not found or no changes made'}), 404
            
    except Exception as e:
        return jsonify({'error': 'Failed to update task', 'details': str(e)}), 500

@admin_dashboard_bp.route('/dashboard/tasks/<task_id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def delete_student_task(task_id):
    """
    Delete a task
    """
    try:
        local_service = AdminDashboardService()
        success = local_service.delete_task(task_id)
        
        if success:
            return jsonify({'message': 'Task deleted successfully'}), 200
        else:
            return jsonify({'error': 'Task not found'}), 404
            
    except Exception as e:
        return jsonify({'error': 'Failed to delete task', 'details': str(e)}), 500

@admin_dashboard_bp.route('/dashboard/reports', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_reports():
    """
    Get aggregated data for reports page
    """
    try:
        claims = get_jwt()
        department = claims.get('department')
        college_name = claims.get('college_name')
        
        if not department or not college_name:
            return jsonify({'error': 'Admin context missing'}), 400
            
        local_service = AdminDashboardService()
        data = local_service.get_reports_data(department, college_name)
        
        return jsonify(data), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to fetch reports data', 'details': str(e)}), 500
