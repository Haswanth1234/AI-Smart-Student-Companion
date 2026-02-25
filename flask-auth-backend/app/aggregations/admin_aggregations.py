from bson import ObjectId

class AdminAggregations:
    """
    Admin Aggregation Pipelines
    Complex queries for admin dashboard
    """
    
    @staticmethod
    def get_students_with_profiles(department, college_name):
        """
        Get all students with their profile and attendance data
        
        Pipeline joins:
        - users collection
        - student_profiles collection
        - Calculates attendance from attendance collection
        
        Args:
            department (str): Department name
            college_name (str): College name
        
        Returns:
            Aggregation pipeline
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
            
            # Step 2: Join with student_profiles
            {
                '$lookup': {
                    'from': 'student_profiles',
                    'localField': '_id',
                    'foreignField': 'user_id',
                    'as': 'profile'
                }
            },
            
            # Step 3: Unwind profile (optional)
            {
                '$unwind': {
                    'path': '$profile',
                    'preserveNullAndEmptyArrays': True  # Include students without profiles
                }
            },
            
            # Step 4: Project needed fields
            {
                '$project': {
                    '_id': 1,
                    'name': 1,
                    'email': 1,
                    'phone': 1,
                    'roll_number': 1,
                    'department': 1,
                    'college_name': 1,
                    'profile_completed': 1,
                    'created_at': 1,
                    'attendance_percentage': {
                        '$ifNull': ['$profile.attendance_percentage', 0]
                    },
                    'studying_year': '$profile.studying_year',
                    'semester': '$profile.semester',
                    'interested_domain': '$profile.interested_domain'
                }
            },
            
            # Step 5: Sort by name
            {
                '$sort': {'name': 1}
            }
        ]
        
        return pipeline