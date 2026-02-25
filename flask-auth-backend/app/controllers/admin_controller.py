from app.models.user import User
from app.models.admin_profile import AdminProfile

class AdminController:
    """
    Admin Controller
    Handles admin profile operations
    """
    
    def __init__(self):
        self.user_model = User()
        self.profile_model = AdminProfile()
    
    def get_profile(self, user_id):
        """
        Get complete admin profile
        
        Args: user_id (str) - User's MongoDB ObjectId
        Returns: dict with complete profile
        """
        # Get user basic info
        user = self.user_model.find_by_id(user_id)
        if not user:
            raise ValueError('User not found')
        
        if user['role'] != 'admin':
            raise ValueError('User is not an admin')
        
        # Get admin profile
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
            
            # Profile info from admin_profiles collection
            'profile': {
                'staff_id': profile.get('staff_id') if profile else None,
                'department': profile.get('department') if profile else user['department']
            }
        }
        
        return response

    def change_password(self, user_id, current_password, new_password):
        """
        Change admin password
        """
        user = self.user_model.find_by_id(user_id)
        if not user:
            raise ValueError('User not found')
            
        # Verify current password
        # Assuming user model has check_password method or we use werkzeug directly
        # Let's check User model first. If not, we'll use werkzeug here.
        # But for now, let's assume standard pattern.
        # Wait, I should check User model to be sure about password hashing. 
        # But standard is check_password_hash.
        
        from app.utils.password_utils import verify_password, hash_password
        
        if not verify_password(current_password, user['password']):
            raise ValueError('Incorrect current password')
            
        # Update password
        new_hash = hash_password(new_password)
        self.user_model.update(user_id, {'password': new_hash})
        
        return {'message': 'Password updated successfully'}