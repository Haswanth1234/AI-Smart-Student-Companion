from datetime import datetime
from bson import ObjectId

class StudentInsight:
    """Student Insights Model"""
    
    def __init__(self):
        from app import get_db
        self.collection = get_db()['student_insights']
        self._create_indexes()
    
    def _create_indexes(self):
        """Create indexes for fast queries"""
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