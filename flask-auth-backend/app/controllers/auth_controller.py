from app.models.user import User
from app.utils.password_utils import hash_password, verify_password
from app.utils.token_utils import generate_access_token
from app.utils.validators import validate_email, validate_password, validate_required_fields, validate_phone

class AuthController:
    """Authentication Controller"""
    
    def __init__(self):
        self.user_model = User()
    
    def register(self, data):
        """Register a new user (student or admin)"""
        
        # Required fields validation
        required_fields = ['name', 'email', 'password', 'role', 'department', 'college_name']
        is_valid, missing = validate_required_fields(data, required_fields)
        
        if not is_valid:
            raise ValueError(f'Missing required fields: {", ".join(missing)}')
        
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        phone = data.get('phone')
        roll_number = data.get('roll_number')  # NEW: Get roll_number (optional)
        
        # Validate email
        if not validate_email(email):
            raise ValueError('Invalid email format')
        
        # Validate password
        if not validate_password(password):
            raise ValueError('Password must be at least 6 characters')
        
        # Validate phone if provided
        if phone and not validate_phone(phone):
            raise ValueError('Invalid phone number format. Use 10 digits (e.g., 9876543210)')
        
        # Validate role
        if role not in ['student', 'admin']:
            raise ValueError('Role must be either "student" or "admin"')
        
        # Check if email already exists
        if self.user_model.find_by_email(email):
            raise ValueError('User with this email already exists')
        
        # Check if phone already exists
        if phone and self.user_model.find_by_phone(phone):
            raise ValueError('User with this phone number already exists')
        
        # NEW: Check if roll_number already exists (for students only)
        if role == 'student' and roll_number:
            if self.user_model.find_by_roll_number(roll_number):
                raise ValueError('Student with this roll number already exists')
        
        # Hash password
        hashed_password = hash_password(password)
        
        # Prepare user data
        user_data = {
            'name': data.get('name'),
            'email': email,
            'password': hashed_password,
            'role': role,
            'department': data.get('department').upper(),
            'college_name': data.get('college_name').upper()
        }
        
        # Add phone if provided
        if phone:
            import re
            cleaned_phone = re.sub(r'[\s\-]', '', phone)
            user_data['phone'] = cleaned_phone
        
        # NEW: Add roll_number if provided (for students)
        if role == 'student' and roll_number:
            user_data['roll_number'] = roll_number.upper()
        
        # Create user
        user_id = self.user_model.create(user_data)
        
        return {
            'message': f'{role.capitalize()} registered successfully',
            'user_id': str(user_id)
        }
    
    def login(self, data):
        """Login user and generate JWT token"""
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            raise ValueError('Email and password are required')
        
        print(f"[DEBUG] Login attempt for: {email}", flush=True)
        user = self.user_model.find_by_email(email)
        if not user:
            print(f"[DEBUG] User not found: {email}", flush=True)
            raise ValueError('Invalid email or password')
        
        print(f"[DEBUG] User found: {user.get('name')}", flush=True)
        if not verify_password(password, user['password']):
            print(f"[DEBUG] Password mismatch for: {email}", flush=True)
            raise ValueError('Invalid email or password')
        
        print(f"[DEBUG] Password verified, generating token...", flush=True)
        access_token = generate_access_token(
            user_id=str(user['_id']),
            role=user.get('role', 'student'),
            department=user.get('department', 'GENERAL'),
            college_name=user.get('college_name', 'GENERAL')
        )
        
        # Return user data with profile_completed status and roll_number
        return {
            'message': 'Login successful',
            'token': access_token,
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'phone': user.get('phone'),
                'roll_number': user.get('roll_number'),  # NEW: Include roll_number
                'role': user.get('role', 'student'),
                'department': user.get('department', 'GENERAL'),
                'college_name': user.get('college_name', 'GENERAL'),
                'profile_completed': user.get('profile_completed', False)
            }
        }