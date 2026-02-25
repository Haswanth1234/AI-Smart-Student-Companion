from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)
auth_controller = AuthController()

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        # ✅ CHECK FOR MISSING ROLE BEFORE PROCESSING
        if not data or 'role' not in data:
            return jsonify({"error": "Missing required fields: role"}), 400

        # Process registration through controller
        result = auth_controller.register(data)
        
        return jsonify(result), 201

    except ValueError as e:
        # Handle specific validation errors from the controller
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Handle unexpected server errors
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and get JWT token
    
    Request Body:
    {
        "email": "john@example.com",
        "password": "password123"
    }
    """
    try:
        data = request.get_json()
        result = auth_controller.login(data)
        return jsonify(result), 200
    except ValueError as e:
        print(f"[AUTH] Validation error: {str(e)}", flush=True)
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        import traceback
        print("[AUTH] CRITICAL LOGIN ERROR:", flush=True)
        traceback.print_exc()
        return jsonify({'error': 'Internal server error during login', 'details': str(e)}), 500
    