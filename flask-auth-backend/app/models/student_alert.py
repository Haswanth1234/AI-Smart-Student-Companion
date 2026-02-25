from datetime import datetime, timedelta
from bson import ObjectId

class StudentAlert:
    """Student Alerts Model"""
    
    @property
    def collection(self):
        """Lazy access to the collection"""
        from app import get_db
        db = get_db()
        if db is None:
            raise RuntimeError("Database not initialized. Ensure create_app() has run.")
        return db['student_alerts']

    def __init__(self):
        # Index creation should be handled outside of __init__
        pass
    
    def ensure_indexes(self):
        """Manually ensure indexes are created"""
        try:
            self.collection.create_index('user_id')
            self.collection.create_index([('user_id', 1), ('is_read', 1)])
            self.collection.create_index([('user_id', 1), ('created_at', -1)])
        except:
            pass
    
    def create(self, alert_data):
        """Create new alert"""
        alert_data['created_at'] = datetime.utcnow()
        alert_data['is_read'] = False
        
        # Set expiry (30 days by default)
        if 'expires_at' not in alert_data:
            alert_data['expires_at'] = datetime.utcnow() + timedelta(days=30)
        
        result = self.collection.insert_one(alert_data)
        return result.inserted_id
    
    def find_unread_by_user(self, user_id):
        """Get unread alerts"""
        return list(self.collection.find({
            'user_id': ObjectId(user_id),
            'is_read': False,
            'expires_at': {'$gt': datetime.utcnow()}
        }).sort('created_at', -1))
    
    def find_all_by_user(self, user_id, limit=50):
        """Get all alerts (read & unread)"""
        return list(self.collection.find({
            'user_id': ObjectId(user_id),
            'expires_at': {'$gt': datetime.utcnow()}
        }).sort('created_at', -1).limit(limit))
    
    def mark_as_read(self, alert_id):
        """Mark alert as read"""
        return self.collection.update_one(
            {'_id': ObjectId(alert_id)},
            {'$set': {'is_read': True}}
        )
    
    def count_unread(self, user_id):
        """Count unread alerts"""
        return self.collection.count_documents({
            'user_id': ObjectId(user_id),
            'is_read': False,
            'expires_at': {'$gt': datetime.utcnow()}
        })