from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.admin_controller import AdminController
from app.middleware.auth_middleware import role_required

admin_bp = Blueprint('admin', __name__)
admin_controller = AdminController()

@admin_bp.route('/profile', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_profile():
    """
    Get admin profile (JWT required, Admin only)
    
    Headers:
    Authorization: Bearer <JWT_TOKEN>
    """
    try:
        user_id = get_jwt_identity()
        result = admin_controller.get_profile(user_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to fetch profile', 'details': str(e)}), 500

@admin_bp.route('/change-password', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def change_password():
    """
    Change admin password
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Missing current or new password'}), 400
            
        result = admin_controller.change_password(user_id, current_password, new_password)
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to change password', 'details': str(e)}), 500