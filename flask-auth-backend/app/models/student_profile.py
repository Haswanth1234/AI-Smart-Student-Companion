from datetime import datetime
from bson import ObjectId

class StudentProfile:
    """
    Student Profile Model - Stores additional student information
    Linked to users collection via user_id
    """
    
    @property
    def collection(self):
        """Lazy access to the collection"""
        from app import get_db
        db = get_db()
        if db is None:
            raise RuntimeError("Database not initialized. Ensure create_app() has run.")
        return db['student_profiles']

    def __init__(self):
        # Index creation should be handled outside of __init__
        pass
    
    def ensure_indexes(self):
        """Manually ensure indexes are created"""
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