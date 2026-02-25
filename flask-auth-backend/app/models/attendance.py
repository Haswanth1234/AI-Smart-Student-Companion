from datetime import datetime
from bson import ObjectId

class Attendance:
    """
    Attendance Model - Manages daily attendance records
    Each document represents one student's attendance for one date
    """
    
    @property
    def collection(self):
        """Lazy access to the collection"""
        from app import get_db
        db = get_db()
        if db is None:
            raise RuntimeError("Database not initialized. Ensure create_app() has run.")
        return db['attendance']

    def __init__(self):
        # Index creation should be handled outside of __init__
        pass
    
    def ensure_indexes(self):
        """Manually ensure indexes are created"""
        try:
            # Unique constraint: one attendance record per student per date
            self.collection.create_index(
                [('student_id', 1), ('date', 1)], 
                unique=True
            )
            # Index for fast queries by student
            self.collection.create_index('student_id')
            # Index for date range queries
            self.collection.create_index('date')
        except:
            pass
    
    def mark_attendance(self, attendance_data):
        """
        Mark attendance for a student
        Args:
            attendance_data (dict): {
                'student_id': ObjectId,
                'date': 'YYYY-MM-DD',
                'status': 'present' or 'absent',
                'marked_by': ObjectId (admin_id)
            }
        Returns: ObjectId of created record or raises error if duplicate
        """
        attendance_data['created_at'] = datetime.utcnow()
        result = self.collection.insert_one(attendance_data)
        return result.inserted_id
    
    def find_by_student_and_date(self, student_id, date):
        """
        Check if attendance already marked for student on specific date
        Args:
            student_id (str or ObjectId)
            date (str): YYYY-MM-DD format
        Returns: Attendance document or None
        """
        return self.collection.find_one({
            'student_id': ObjectId(student_id),
            'date': date
        })
    
    def get_student_attendance_history(self, student_id):
        """
        Get all attendance records for a student
        Args: student_id (str or ObjectId)
        Returns: List of attendance documents sorted by date (newest first)
        """
        return list(self.collection.find({
            'student_id': ObjectId(student_id)
        }).sort('date', -1))
    
    def calculate_attendance_stats(self, student_id):
        """
        Calculate attendance statistics for a student
        Uses MongoDB aggregation for efficiency
        
        Args: student_id (str or ObjectId)
        Returns: dict {
            'total_days': int,
            'present_days': int,
            'absent_days': int,
            'attendance_percentage': float
        }
        """
        pipeline = [
            # Match all records for this student
            {'$match': {'student_id': ObjectId(student_id)}},
            
            # Group and count by status
            {'$group': {
                '_id': '$status',
                'count': {'$sum': 1}
            }}
        ]
        
        results = list(self.collection.aggregate(pipeline))
        
        # Initialize counters
        present_days = 0
        absent_days = 0
        
        # Parse aggregation results
        for result in results:
            if result['_id'] == 'present':
                present_days = result['count']
            elif result['_id'] == 'absent':
                absent_days = result['count']
        
        total_days = present_days + absent_days
        
        # Calculate percentage
        if total_days > 0:
            attendance_percentage = round((present_days / total_days) * 100, 2)
        else:
            attendance_percentage = 0.0
        
        return {
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': absent_days,
            'attendance_percentage': attendance_percentage
        }
    
    def delete_attendance(self, student_id, date):
        """
        Delete attendance record (for corrections)
        Args:
            student_id (str or ObjectId)
            date (str): YYYY-MM-DD
        Returns: DeleteResult
        """
        return self.collection.delete_one({
            'student_id': ObjectId(student_id),
            'date': date
        })