from datetime import datetime
from bson import ObjectId

class User:
    """
    User Model - Handles the main users collection
    """
    
    @property
    def collection(self):
        """Lazy access to the collection"""
        from app import get_db
        db = get_db()
        if db is None:
            raise RuntimeError("Database not initialized. Ensure create_app() has run.")
        return db['users']

    def __init__(self):
        # We don't create indexes in __init__ because it's called during import
        pass
    
    def ensure_indexes(self):
        """Manually ensure indexes are created"""
        try:
            self.collection.create_index('email', unique=True)
            self.collection.create_index('phone', unique=True, sparse=True)
            self.collection.create_index('roll_number', unique=True, sparse=True)
            self.collection.create_index([('role', 1), ('department', 1), ('college_name', 1)])
        except:
            pass
    
    def create(self, user_data):
        """Create a new user in database"""
        user_data['created_at'] = datetime.utcnow()
        user_data['profile_completed'] = False
        result = self.collection.insert_one(user_data)
        return result.inserted_id
    
    def find_by_email(self, email):
        """Find user by email address"""
        return self.collection.find_one({'email': email})
    
    def find_by_phone(self, phone):
        """Find user by phone number"""
        return self.collection.find_one({'phone': phone})
    
    def find_by_roll_number(self, roll_number):
        """Find user by roll number"""
        return self.collection.find_one({'roll_number': roll_number})
    
    def find_by_id(self, user_id):
        """Find user by MongoDB ObjectId"""
        return self.collection.find_one({'_id': ObjectId(user_id)})
    
    def update(self, user_id, update_data):
        """Update user data"""
        update_data['updated_at'] = datetime.utcnow()
        return self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
    
    def mark_profile_completed(self, user_id):
        """Mark user's profile as completed"""
        return self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'profile_completed': True, 'updated_at': datetime.utcnow()}}
        )
    
    def find_by_role(self, role):
        """Find all users with specific role"""
        return list(self.collection.find({'role': role}))
    
    def find_students_by_department_and_college(self, department, college_name):
        """
        Find all students in specific department and college
        Args:
            department (str): Department name
            college_name (str): College name
        Returns:
            List of student documents
        """
        return list(self.collection.find({
            'role': 'student',
            'department': department,
            'college_name': college_name
        }).sort('name', 1))  # Sort by name alphabetically