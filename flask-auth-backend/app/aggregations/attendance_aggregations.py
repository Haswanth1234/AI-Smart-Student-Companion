from datetime import datetime
from bson import ObjectId

class AttendanceAggregations:
    """
    Attendance Aggregation Pipelines
    Handles complex MongoDB queries for dashboard analytics
    """
    
    @staticmethod
    def get_today_attendance_by_department(department, college_name):
        """
        Get today's attendance summary for specific department & college
        
        Pipeline Logic:
        1. Match attendance records for today
        2. Lookup student details from users collection
        3. Filter by department and college
        4. Group by status and count
        
        Args:
            department (str): Department name (e.g., "MCA")
            college_name (str): College name (e.g., "SNS")
        
        Returns:
            Pipeline for aggregation
        """
        today = datetime.now().strftime('%Y-%m-%d')
        
        pipeline = [
            # Step 1: Match today's attendance records
            {
                '$match': {
                    'date': today
                }
            },
            
            # Step 2: Join with users collection to get student details
            {
                '$lookup': {
                    'from': 'users',
                    'localField': 'student_id',
                    'foreignField': '_id',
                    'as': 'student_info'
                }
            },
            
            # Step 3: Unwind the joined array
            {
                '$unwind': '$student_info'
            },
            
            # Step 4: Filter by department, college, and role
            {
                '$match': {
                    'student_info.role': 'student',
                    'student_info.department': department,
                    'student_info.college_name': college_name
                }
            },
            
            # Step 5: Group by status and count
            {
                '$group': {
                    '_id': '$status',
                    'count': {'$sum': 1}
                }
            }
        ]
        
        return pipeline
    
    @staticmethod
    def get_department_students_with_attendance(department, college_name):
        """
        Get all students in department with their attendance percentage
        
        Pipeline Logic:
        1. Match students in specific department & college
        2. Lookup their profiles to get attendance_percentage
        3. Return list with id, name, and percentage
        
        Args:
            department (str): Department name
            college_name (str): College name
        
        Returns:
            Pipeline for aggregation
        """
        pipeline = [
            # Step 1: Match students in department & college
            {
                '$match': {
                    'role': 'student',
                    'department': department,
                    'college_name': college_name
                }
            },
            
            # Step 2: Join with student_profiles to get attendance data
            {
                '$lookup': {
                    'from': 'student_profiles',
                    'localField': '_id',
                    'foreignField': 'user_id',
                    'as': 'profile'
                }
            },
            
            # Step 3: Project only needed fields
            {
                '$project': {
                    '_id': 1,
                    'name': 1,
                    'email': 1,
                    # Handle case where profile doesn't exist
                    'attendance_percentage': {
                        '$ifNull': [
                            {'$arrayElemAt': ['$profile.attendance_percentage', 0]},
                            0.0
                        ]
                    }
                }
            }
        ]
        
        return pipeline
    
    @staticmethod
    def get_average_attendance(department, college_name):
        """
        Calculate average attendance percentage for department
        
        Pipeline Logic:
        1. Match students in department & college
        2. Lookup their profiles
        3. Calculate average of attendance_percentage
        
        Args:
            department (str): Department name
            college_name (str): College name
        
        Returns:
            Pipeline for aggregation
        """
        pipeline = [
            # Step 1: Match students
            {
                '$match': {
                    'role': 'student',
                    'department': department,
                    'college_name': college_name
                }
            },
            
            # Step 2: Join with profiles
            {
                '$lookup': {
                    'from': 'student_profiles',
                    'localField': '_id',
                    'foreignField': 'user_id',
                    'as': 'profile'
                }
            },
            
            # Step 3: Unwind profiles
            {
                '$unwind': {
                    'path': '$profile',
                    'preserveNullAndEmptyArrays': True  # Include students with no profile
                }
            },
            
            # Step 4: Calculate average
            {
                '$group': {
                    '_id': None,
                    'average': {
                        '$avg': {
                            '$ifNull': ['$profile.attendance_percentage', 0.0]
                        }
                    }
                }
            }
        ]
        
        return pipeline