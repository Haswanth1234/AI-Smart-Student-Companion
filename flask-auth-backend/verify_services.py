import os
import sys
from bson import ObjectId

# Add current directory to path
sys.path.append(os.getcwd())

from app import create_app, get_db
from app.services.admin_student_service import AdminStudentService
from app.services.admin_dashboard_service import AdminDashboardService

app = create_app()

def verify_services():
    with app.app_context():
        db = get_db()
        
        # 1. Find an Admin
        admin = db.users.find_one({"role": "admin"})
        if not admin:
            print("[ERROR] No admin found in DB.")
            return
            
        print(f"Testing with Admin: {admin.get('name')} ({admin.get('_id')})")
        admin_id = str(admin.get('_id'))
        
        # 2. Test AdminStudentService.get_students_list
        print("\n--- Testing AdminStudentService.get_students_list ---")
        try:
            student_service = AdminStudentService()
            students_result = student_service.get_students_list(admin_id)
            print(f"[SUCCESS] Got {len(students_result.get('students', []))} students.")
            if students_result.get('students'):
                print(f"Sample Student: {students_result['students'][0]['name']}")
            else:
                print("[WARNING] Student list is empty.")
        except Exception as e:
            print(f"[ERROR] Student Service failed: {e}")
            import traceback
            traceback.print_exc()

        # 3. Test AdminDashboardService.get_attendance_summary
        print("\n--- Testing AdminDashboardService.get_attendance_summary ---")
        try:
            dashboard_service = AdminDashboardService()
            # This is the method I just added/fixed
            summary_result = dashboard_service.get_attendance_summary(admin_id)
            print("[SUCCESS] Got summary result:")
            print(summary_result.get('summary'))
            print(f"Defaulters count: {len(summary_result.get('defaulters', []))}")
        except Exception as e:
            print(f"[ERROR] Dashboard Service (Attendance Summary) failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    verify_services()
