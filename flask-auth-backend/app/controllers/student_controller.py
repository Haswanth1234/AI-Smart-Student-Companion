from app.models.user import User
from app.models.student_profile import StudentProfile
from bson import ObjectId

class StudentController:
    """
    Student Controller
    Handles student profile operations
    """
    
    def __init__(self):
        self.user_model = User()
        self.profile_model = StudentProfile()
    
    def get_profile(self, user_id):
        """
        Get complete student profile
        
        Args: user_id (str) - User's MongoDB ObjectId
        Returns: dict with complete profile
        """
        # Get user basic info
        user = self.user_model.find_by_id(user_id)
        if not user:
            raise ValueError('User not found')
        
        if user['role'] != 'student':
            raise ValueError('User is not a student')
        
        # Get student profile (may not exist yet)
        profile = self.profile_model.find_by_user_id(user_id)
        
        # Combine data
        response = {
            # Basic info from users collection
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'phone': user.get('phone'),  # NEW: Include phone
            'role': user['role'],
            'department': user['department'],
            'college_name': user['college_name'],
            
            # Profile info from student_profiles collection
            'profile': {
                'studying_year': profile.get('studying_year') if profile else None,
                'semester': profile.get('semester') if profile else None,
                'semester_marks': profile.get('semester_marks', []) if profile else [],
                'attendance_percentage': profile.get('attendance_percentage') if profile else None,
                'interested_domain': profile.get('interested_domain') if profile else None,
                'skills': profile.get('skills', []) if profile else [],
                'passout_year': profile.get('passout_year') if profile else None
            }
        }
        
        return response
    
    def update_profile(self, user_id, profile_data):
        """
        Create or update student profile
        
        Args:
            user_id (str) - User's MongoDB ObjectId
            profile_data (dict) - Profile information to update
        Returns: dict with success message
        """
        # Verify user exists and is a student
        user = self.user_model.find_by_id(user_id)
        if not user:
            raise ValueError('User not found')
        
        if user['role'] != 'student':
            raise ValueError('Only students can update student profile')
        
        # Prepare profile data
        update_data = {
            'user_id': ObjectId(user_id)
        }
        
        # Add optional fields if provided
        if 'studying_year' in profile_data:
            update_data['studying_year'] = profile_data['studying_year']
        
        if 'semester' in profile_data:
            update_data['semester'] = profile_data['semester']
        
        if 'semester_marks' in profile_data:
            update_data['semester_marks'] = profile_data['semester_marks']
        
        if 'attendance_percentage' in profile_data:
            update_data['attendance_percentage'] = profile_data['attendance_percentage']
        
        if 'interested_domain' in profile_data:
            update_data['interested_domain'] = profile_data['interested_domain']
        
        if 'skills' in profile_data:
            update_data['skills'] = profile_data['skills']
        
        if 'passout_year' in profile_data:
            update_data['passout_year'] = profile_data['passout_year']
        
        # Update or create profile
        self.profile_model.create_or_update(user_id, update_data)
        
        return {
            'message': 'Student profile updated successfully'
        }
    
    def update_user_info(self, user_id, user_data):
        """
        Update user basic info (name, phone) - NEW METHOD
        
        Args:
            user_id (str) - User's MongoDB ObjectId
            user_data (dict) - User info to update (name, phone)
        Returns: dict with success message
        """
        from app.utils.validators import validate_phone
        
        user = self.user_model.find_by_id(user_id)
        if not user:
            raise ValueError('User not found')
        
        update_data = {}
        
        # Update name if provided
        if 'name' in user_data:
            update_data['name'] = user_data['name']
        
        # Update phone if provided
        if 'phone' in user_data:
            phone = user_data['phone']
            
            if phone and not validate_phone(phone):
                raise ValueError('Invalid phone number format')
            
            # Check if phone already exists for another user
            if phone:
                import re
                cleaned_phone = re.sub(r'[\s\-]', '', phone)
                existing = self.user_model.find_by_phone(cleaned_phone)
                if existing and str(existing['_id']) != user_id:
                    raise ValueError('Phone number already in use')
                
                update_data['phone'] = cleaned_phone
        
        if update_data:
            self.user_model.update(user_id, update_data)
        
        return {
            'message': 'User information updated successfully'
        }