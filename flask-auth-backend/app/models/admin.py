from datetime import datetime
from bson import ObjectId

class Admin:
    @property
    def collection(self):
        """Lazy access to the collection"""
        from app import get_db
        db = get_db()
        if db is None:
            raise RuntimeError("Database not initialized. Ensure create_app() has run.")
        return db['admins']

    def __init__(self):
        # Index creation should be handled outside of __init__ if possible
        pass
    
    def ensure_indexes(self):
        """Manually ensure indexes are created"""
        try:
            self.collection.create_index('email', unique=True)
            self.collection.create_index([('department', 1), ('college_name', 1)])
        except:
            pass
    
    def create(self, admin_data):
        """Create a new admin"""
        admin_data['created_at'] = datetime.utcnow()
        admin_data['updated_at'] = datetime.utcnow()
        result = self.collection.insert_one(admin_data)
        return result.inserted_id
    
    def find_by_email(self, email):
        """Find admin by email"""
        return self.collection.find_one({'email': email})
    
    def find_by_id(self, admin_id):
        """Find admin by ID"""
        return self.collection.find_one({'_id': ObjectId(admin_id)})
    
    def find_by_department_and_college(self, department, college_name):
        """Find admins by department and college"""
        return list(self.collection.find({
            'department': department,
            'college_name': college_name
        }))
    
    def update(self, admin_id, update_data):
        """Update admin data"""
        update_data['updated_at'] = datetime.utcnow()
        return self.collection.update_one(
            {'_id': ObjectId(admin_id)},
            {'$set': update_data}
        )