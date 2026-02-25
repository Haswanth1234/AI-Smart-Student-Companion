from flask import Blueprint, request, jsonify
from app.controllers.student_controller import StudentController

student_bp = Blueprint('student_auth', __name__)
student_controller = StudentController()

@student_bp.route('/register', methods=['POST'])
def register():
    """Student registration endpoint"""
    try:
        data = request.get_json()
        result = student_controller.register(data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@student_bp.route('/login', methods=['POST'])
def login():
    """Student login endpoint"""
    try:
        data = request.get_json()
        result = student_controller.login(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401