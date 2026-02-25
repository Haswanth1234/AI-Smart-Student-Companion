from datetime import datetime
from bson import ObjectId

class AdminProfile:
    """
    Admin Profile Model - Stores additional admin information
    Linked to users collection via user_id
    """
    
    def __init__(self):
        from app import get_db
        self.collection = get_db()['admin_profiles']
        self._create_indexes()
    
    def _create_indexes(self):
        """Create indexes"""
        try:
            self.collection.create_index('user_id', unique=True)
            self.collection.create_index('staff_id', unique=True)
        except:
            pass
    
    def create(self, profile_data):
        """
        Create new admin profile
        Args: profile_data (dict) - Contains user_id, department, staff_id
        Returns: ObjectId of created profile
        """
        profile_data['created_at'] = datetime.utcnow()
        result = self.collection.insert_one(profile_data)
        return result.inserted_id
    
    def find_by_user_id(self, user_id):
        """
        Get admin profile by user_id
        Args: user_id (str)
        Returns: Profile document or None
        """
        return self.collection.find_one({'user_id': ObjectId(user_id)})
    
    def find_by_staff_id(self, staff_id):
        """Find admin by staff ID"""
        return self.collection.find_one({'staff_id': staff_id})