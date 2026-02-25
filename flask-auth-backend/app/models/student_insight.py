from datetime import datetime
from bson import ObjectId

class StudentInsight:
    """Student Insights Model"""
    
    @property
    def collection(self):
        """Lazy access to the collection"""
        from app import get_db
        db = get_db()
        if db is None:
            raise RuntimeError("Database not initialized. Ensure create_app() has run.")
        return db['student_insights']

    def __init__(self):
        # Index creation should be handled outside of __init__
        pass
    
    def ensure_indexes(self):
        """Manually ensure indexes are created"""
        try:
            self.collection.create_index('user_id')
            self.collection.create_index([('user_id', 1), ('generated_at', -1)])
        except:
            pass
    
    def create(self, insight_data):
        """Create new insight"""
        insight_data['generated_at'] = datetime.utcnow()
        insight_data['last_updated'] = datetime.utcnow()
        result = self.collection.insert_one(insight_data)
        return result.inserted_id
    
    def find_by_user_id(self, user_id):
        """Get latest insight for a student"""
        return self.collection.find_one(
            {'user_id': ObjectId(user_id)},
            sort=[('generated_at', -1)]
        )
    
    def find_all_by_user(self, user_id, limit=10):
        """Get insight history"""
        return list(self.collection.find(
            {'user_id': ObjectId(user_id)}
        ).sort('generated_at', -1).limit(limit))