from flask import Blueprint, request, jsonify
from app.controllers.admin_controller import AdminController

admin_bp = Blueprint('admin_auth', __name__)
admin_controller = AdminController()

@admin_bp.route('/register', methods=['POST'])
def register():
    """Admin registration endpoint"""
    try:
        data = request.get_json()
        result = admin_controller.register(data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin_bp.route('/login', methods=['POST'])
def login():
    """Admin login endpoint"""
    try:
        data = request.get_json()
        result = admin_controller.login(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401