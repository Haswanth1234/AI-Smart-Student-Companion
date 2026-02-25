from app.models.attendance import Attendance
from app.models.student_profile import StudentProfile
from app.models.user import User
from bson import ObjectId
from datetime import datetime

class AttendanceService:
    """
    Attendance Service - Handles all attendance business logic
    Separates business rules from routes for cleaner code
    """
    
    def __init__(self):
        self.attendance_model = Attendance()
        self.student_profile_model = StudentProfile()
        self.user_model = User()
    
    def mark_attendance(self, student_id, date, status, admin_id):
        """
        Mark attendance for a student
        
        Steps:
        1. Validate student exists and is a student role
        2. Validate date format
        3. Validate status value
        4. Check for duplicate attendance
        5. Mark attendance
        6. Recalculate and update attendance percentage
        
        Args:
            student_id (str): Student's user_id
            date (str): YYYY-MM-DD format
            status (str): 'present' or 'absent'
            admin_id (str): Admin's user_id from JWT
        
        Returns: dict with success message and updated percentage
        Raises: ValueError for validation errors
        """
        
        # Step 1: Validate student exists and is a student
        student = self.user_model.find_by_id(student_id)
        if not student:
            raise ValueError('Student not found')
        
        if student['role'] != 'student':
            raise ValueError('User is not a student')
        
        # Step 2: Validate date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Invalid date format. Use YYYY-MM-DD')
        
        # Step 3: Validate status
        if status not in ['present', 'absent']:
            raise ValueError('Status must be either "present" or "absent"')
        
        # Step 4: Check for duplicate attendance
        existing = self.attendance_model.find_by_student_and_date(student_id, date)
        if existing:
            raise ValueError(f'Attendance already marked for {date}. Please update instead of creating new.')
        
        # Step 5: Mark attendance
        attendance_data = {
            'student_id': ObjectId(student_id),
            'date': date,
            'status': status,
            'marked_by': ObjectId(admin_id)
        }
        
        try:
            self.attendance_model.mark_attendance(attendance_data)
        except Exception as e:
            if 'duplicate key error' in str(e).lower():
                raise ValueError('Attendance already exists for this date')
            raise e
        
        # Step 6: Recalculate attendance percentage and update profile
        stats = self.attendance_model.calculate_attendance_stats(student_id)
        
        # Update student profile with new percentage
        self.student_profile_model.create_or_update(
            student_id,
            {'attendance_percentage': stats['attendance_percentage']}
        )
        
        return {
            'message': f'Attendance marked as {status} for {date}',
            'attendance_percentage': stats['attendance_percentage'],
            'total_days': stats['total_days']
        }
    
    def get_student_attendance(self, student_id):
        """
        Get complete attendance information for a student
        
        Steps:
        1. Validate student exists
        2. Get attendance history
        3. Calculate statistics
        4. Format and return data
        
        Args: student_id (str): Student's user_id
        Returns: dict with stats and history
        """
        
        # Step 1: Validate student exists
        student = self.user_model.find_by_id(student_id)
        if not student:
            raise ValueError('Student not found')
        
        if student['role'] != 'student':
            raise ValueError('User is not a student')
        
        # Step 2: Get attendance history
        attendance_history = self.attendance_model.get_student_attendance_history(student_id)
        
        # Step 3: Calculate statistics
        stats = self.attendance_model.calculate_attendance_stats(student_id)
        
        # Step 4: Format history for response
        formatted_history = []
        for record in attendance_history:
            formatted_history.append({
                'date': record['date'],
                'status': record['status'],
                'marked_at': record['created_at'].isoformat()
            })
        
        # Step 5: Return complete attendance data
        return {
            'student_id': str(student['_id']),
            'student_name': student['name'],
            'statistics': {
                'total_days': stats['total_days'],
                'present_days': stats['present_days'],
                'absent_days': stats['absent_days'],
                'attendance_percentage': stats['attendance_percentage']
            },
            'history': formatted_history
        }
