from datetime import datetime
from bson import ObjectId

class StudentProfile:
    """
    Student Profile Model - Stores additional student information
    Linked to users collection via user_id
    """
    
    def __init__(self):
        from app import get_db
        self.collection = get_db()['student_profiles']
        self._create_indexes()
    
    def _create_indexes(self):
        """Create index on user_id for fast lookups"""
        try:
            self.collection.create_index('user_id', unique=True)
        except:
            pass
    
    def create_or_update(self, user_id, profile_data):
        """
        Create new profile or update existing one
        Args: 
            user_id (str) - Reference to users collection
            profile_data (dict) - Profile information
        Returns: Result of operation
        """
        profile_data['updated_at'] = datetime.utcnow()
        
        # Use upsert: update if exists, insert if doesn't exist
        result = self.collection.update_one(
            {'user_id': ObjectId(user_id)},
            {'$set': profile_data},
            upsert=True
        )
        return result
    
    def find_by_user_id(self, user_id):
        """
        Get student profile by user_id
        Args: user_id (str)
        Returns: Profile document or None
        """
        return self.collection.find_one({'user_id': ObjectId(user_id)})
    
    def delete(self, user_id):
        """Delete student profile"""
        return self.collection.delete_one({'user_id': ObjectId(user_id)})