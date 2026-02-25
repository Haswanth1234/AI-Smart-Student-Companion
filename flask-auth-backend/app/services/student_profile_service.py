from app.models.student_profile import StudentProfile
from app.models.user import User
from app.validators.student_validators import validate_profile_data
from bson import ObjectId
from datetime import datetime

class StudentProfileService:
    """Student Profile Service"""
    
    def __init__(self):
        self.profile_model = StudentProfile()
        self.user_model = User()
    
    def get_student_profile(self, student_id):
        """
        Get student profile with name and email from users collection
        
        Returns:
            dict: Profile data including name & email from users collection
        """
        # Get user basic info
        student = self.user_model.find_by_id(student_id)
        if not student:
            raise ValueError('Student not found')
        
        if student['role'] != 'student':
            raise ValueError('User is not a student')
        
        # Get profile data
        profile = self.profile_model.find_by_user_id(student_id)
        
        # Always return name and email from users collection
        response = {
            'user_info': {
                'name': student['name'],
                'email': student['email'],
                'phone': student.get('phone'),
                'department': student.get('department')
            },
            'profile_completed': student.get('profile_completed', False)
        }
        
        if not profile:
            response['message'] = 'No profile found. Please complete your profile.'
            response['profile'] = {}
        else:
            response['profile'] = {
                'studying_year': profile.get('studying_year'),
                'semester': profile.get('semester'),
                'semester_marks': profile.get('semester_marks', []),
                'attendance_percentage': profile.get('attendance_percentage'),
                'interested_domain': profile.get('interested_domain'),
                'skills': profile.get('skills', []),
                'passout_year': profile.get('passout_year'),
                'created_at': profile.get('created_at').isoformat() if profile.get('created_at') else None,
                'updated_at': profile.get('updated_at').isoformat() if profile.get('updated_at') else None
            }
        
        return response
    
    def create_or_update_profile(self, student_id, profile_data):
        """
        Create or update student profile
        Marks profile as completed after first creation
        """
        # Validate student exists
        student = self.user_model.find_by_id(student_id)
        if not student:
            raise ValueError('Student not found')
        
        if student['role'] != 'student':
            raise ValueError('Only students can update profile')
        
        # Validate profile data
        is_valid, errors = validate_profile_data(profile_data)
        if not is_valid:
            error_messages = [f"{field}: {message}" for field, message in errors.items()]
            raise ValueError(f"Validation failed: {', '.join(error_messages)}")
        
        # Prepare update data
        update_data = {
            'user_id': ObjectId(student_id)
        }
        
        # Add provided fields
        if 'studying_year' in profile_data:
            update_data['studying_year'] = profile_data['studying_year']
        
        if 'semester' in profile_data:
            update_data['semester'] = profile_data['semester']
        
        if 'semester_marks' in profile_data:
            update_data['semester_marks'] = profile_data['semester_marks']
        
        if 'attendance_percentage' in profile_data:
            update_data['attendance_percentage'] = profile_data['attendance_percentage']
        
        if 'interested_domain' in profile_data:
            update_data['interested_domain'] = profile_data['interested_domain'].strip()
        
        if 'skills' in profile_data:
            skills = [skill.strip() for skill in profile_data['skills']]
            update_data['skills'] = list(set(skills))
        
        if 'passout_year' in profile_data:
            update_data['passout_year'] = profile_data['passout_year']
            
        # NEW: Handle User collection updates (Name, Email, Department)
        user_update_data = {}
        if 'name' in profile_data:
            user_update_data['name'] = profile_data['name']
        
        if 'email' in profile_data and profile_data['email'] != student['email']:
            # Check if email is already taken by another user
            existing_user = self.user_model.find_by_email(profile_data['email'])
            if existing_user and str(existing_user['_id']) != str(student_id):
                raise ValueError('Email already in use by another account')
            user_update_data['email'] = profile_data['email']
            
        if 'department' in profile_data:
            user_update_data['department'] = profile_data['department']
            
        if 'phone' in profile_data:
            phone_val = profile_data['phone']
            # Check if phone is already taken by another user
            if phone_val:
                existing_user_phone = self.user_model.find_by_phone(phone_val)
                if existing_user_phone and str(existing_user_phone['_id']) != str(student_id):
                    raise ValueError('Phone number already in use by another account')
                user_update_data['phone'] = phone_val
            
        if user_update_data:
            self.user_model.update(student_id, user_update_data)
        
        # Check if profile exists
        existing_profile = self.profile_model.find_by_user_id(student_id)
        
        if existing_profile:
            # Update existing profile
            update_data['updated_at'] = datetime.utcnow()
            self.profile_model.create_or_update(student_id, update_data)
            message = 'Profile updated successfully'
        else:
            # Create new profile (first time)
            update_data['created_at'] = datetime.utcnow()
            update_data['updated_at'] = datetime.utcnow()
            self.profile_model.create_or_update(student_id, update_data)
            
            # NEW: Mark profile as completed in users collection
            self.user_model.mark_profile_completed(student_id)
            
            message = 'Profile created successfully'
        
        # Fetch updated profile and user data
        updated_profile = self.profile_model.find_by_user_id(student_id)
        updated_user = self.user_model.find_by_id(student_id)
        
        return {
            'message': message,
            'profile_completed': True,  # NEW: Always true after creation/update
            'user_info': {
                'name': updated_user['name'],
                'email': updated_user['email'],
                'phone': updated_user.get('phone'),
                'department': updated_user.get('department')
            },
            'profile': {
                'studying_year': updated_profile.get('studying_year'),
                'semester': updated_profile.get('semester'),
                'semester_marks': updated_profile.get('semester_marks', []),
                'attendance_percentage': updated_profile.get('attendance_percentage'),
                'interested_domain': updated_profile.get('interested_domain'),
                'skills': updated_profile.get('skills', []),
                'passout_year': updated_profile.get('passout_year')
            }
        }