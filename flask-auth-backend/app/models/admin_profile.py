from datetime import datetime
from bson import ObjectId

class AdminProfile:
    """
    Admin Profile Model - Stores additional admin information
    Linked to users collection via user_id
    """
    
    @property
    def collection(self):
        """Lazy access to the collection"""
        from app import get_db
        db = get_db()
        if db is None:
            raise RuntimeError("Database not initialized. Ensure create_app() has run.")
        return db['admin_profiles']

    def __init__(self):
        # Index creation should be handled outside of __init__
        pass
    
    def ensure_indexes(self):
        """Manually ensure indexes are created"""
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