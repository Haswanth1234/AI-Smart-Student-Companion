from datetime import datetime
from bson import ObjectId

class Task:
    """
    Task Model - Handles the tasks collection
    """
    
    @property
    def collection(self):
        """Lazy access to the collection"""
        from app import get_db
        db = get_db()
        if db is None:
            raise RuntimeError("Database not initialized. Ensure create_app() has run.")
        return db['tasks']

    def __init__(self):
        # Index creation should be handled outside of __init__
        pass
    
    def ensure_indexes(self):
        """Manually ensure indexes are created"""
        try:
            self.collection.create_index('user_id')
            self.collection.create_index('due_date')
            self.collection.create_index('status')
        except:
            pass
    
    def create(self, task_data):
        """Create a new task"""
        task_data['created_at'] = datetime.utcnow()
        task_data['updated_at'] = datetime.utcnow()
        # Ensure default fields
        if 'status' not in task_data:
            task_data['status'] = 'pending'
        if 'is_ai_generated' not in task_data:
            task_data['is_ai_generated'] = False
            
        result = self.collection.insert_one(task_data)
        return result.inserted_id
    
    def find_by_user(self, user_id):
        """Find all tasks for a specific user"""
        return list(self.collection.find({'user_id': ObjectId(user_id)}).sort('due_date', 1))

    def find_by_id(self, task_id):
        """Find task by ID"""
        try:
            return self.collection.find_one({'_id': ObjectId(task_id)})
        except:
            return None

    def update(self, task_id, user_id, update_data):
        """Update task data (ensuring user owns the task)"""
        update_data['updated_at'] = datetime.utcnow()
        return self.collection.update_one(
            {'_id': ObjectId(task_id), 'user_id': ObjectId(user_id)},
            {'$set': update_data}
        )

    def delete(self, task_id, user_id):
        """Delete a task (ensuring user owns the task)"""
        return self.collection.delete_one({
            '_id': ObjectId(task_id), 
            'user_id': ObjectId(user_id)
        })
