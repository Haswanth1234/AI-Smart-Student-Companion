from app import get_db
from app.models.user import User
from bson import ObjectId

class AdminStudentService:
    def __init__(self):
        self.db = get_db()
        self.users = self.db['users']
        self.user_model = User()
        
    def get_students_list(self, admin_id):
        """
        Get all students for an admin's department
        Returns: Dict with statistics and list of students
        """
        # 1. Get Admin Details
        admin = self.users.find_one({"_id": ObjectId(admin_id)})
        if not admin:
            raise ValueError("Admin not found")
            
        department = admin.get('department')
        college_name = admin.get('college_name')
        
        if not department or not college_name:
            raise ValueError("Admin profile incomplete (missing department/college)")
            
        # 2. Aggregation Pipeline to get students + profile stats
        pipeline = [
            # Match students in same dept/college
            {
                "$match": {
                    "role": "student",
                    "department": department,
                    "college_name": college_name
                }
            },
            # Lookup Profile for additional details
            {
                "$lookup": {
                    "from": "student_profiles",
                    "localField": "_id",
                    "foreignField": "user_id",
                    "as": "profile"
                }
            },
            # Safe unwind - preserve students without profiles
            {
                "$project": {
                    "name": 1,
                    "email": 1,
                    "phone": 1,
                    "roll_number": 1,
                    "department": 1,
                    "college_name": 1,
                    "profile_completed": 1,
                    "created_at": 1,
                    "profile": {"$arrayElemAt": ["$profile", 0]}
                }
            },
            # Sort by name
            {"$sort": {"name": 1}}
        ]
        
        students_raw = list(self.users.aggregate(pipeline))
        
        # 3. Format Output
        students_formatted = []
        stats = {
            "total_students": len(students_raw),
            "students_with_profile": 0,
            "students_without_profile": 0
        }
        
        for s in students_raw:
            profile = s.get('profile', {}) or {}
            has_profile = bool(profile)
            
            if has_profile:
                stats["students_with_profile"] += 1
            else:
                stats["students_without_profile"] += 1
                
            students_formatted.append({
                "id": str(s['_id']),
                "name": s.get('name'),
                "email": s.get('email'),
                "phone": s.get('phone'),
                "roll_number": s.get('roll_number', 'N/A'),
                "profile_completed": s.get('profile_completed', False),
                "attendance_percentage": profile.get('attendance_percentage', 0) if has_profile else 0,
                "studying_year": profile.get('studying_year', 'N/A') if has_profile else 'N/A',
                "semester": profile.get('current_semester', 'N/A') if has_profile else 'N/A',
                "cgpa": profile.get('cgpa', 'N/A') if has_profile else 'N/A'
            })
            
        return {
            "department": department,
            "college_name": college_name,
            "statistics": stats,
            "students": students_formatted
        }

    def get_student_details(self, admin_id, student_id):
        """
        Get full details of a specific student
        """
        # Verify Admin
        admin = self.users.find_one({"_id": ObjectId(admin_id)})
        if not admin:
            raise ValueError("Admin not found")
            
        # Get Student
        student = self.users.find_one({"_id": ObjectId(student_id)})
        if not student:
            raise ValueError("Student not found")
            
        # Verify Department Match
        if (student.get('department') != admin.get('department') or 
            student.get('college_name') != admin.get('college_name')):
            raise ValueError("Unauthorized: Student belongs to different department")
            
        # Get Profile
        profile = self.db.student_profiles.find_one({"user_id": ObjectId(student_id)}) or {}
        
        # Get Attendance Summary (Last 5 records)
        recent_attendance = list(self.db.attendance.find(
            {"student_id": ObjectId(student_id)}
        ).sort("date", -1).limit(5))
        
        formatted_attendance = []
        for att in recent_attendance:
            formatted_attendance.append({
                "date": att.get('date'),
                "status": att.get('status')
            })
            
        # Get Tasks Summary
        total_tasks = self.db.tasks.count_documents({"student_id": ObjectId(student_id)})
        pending_tasks = self.db.tasks.count_documents({"student_id": ObjectId(student_id), "status": "pending"})
        
        return {
            "student_info": {
                "id": str(student['_id']),
                "name": student.get('name'),
                "email": student.get('email'),
                "phone": student.get('phone'),
                "roll_number": student.get('roll_number'),
                "department": student.get('department'),
                "profile_completed": student.get('profile_completed')
            },
            "profile": {
                "studying_year": profile.get('studying_year'),
                "current_semester": profile.get('current_semester'),
                "attendance_percentage": profile.get('attendance_percentage', 0),
                "cgpa": profile.get('cgpa'),
                "skills": profile.get('skills', []),
                "sem_1_marks": profile.get('sem_1_marks'),
                # Add other sems as needed
            },
            "attendance_summary": {
                "recent": formatted_attendance
            },
            "tasks_summary": {
                "total": total_tasks,
                "pending": pending_tasks
            }
        }
