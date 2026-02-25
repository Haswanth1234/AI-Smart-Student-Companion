from app import get_db
from bson import ObjectId
from app.services.admin_dashboard_service import AdminDashboardService
import json

def debug_db():
    db = get_db()
    users = db['users']
    tasks = db['tasks']
    
    print("\n--- Users (Students) Sample ---")
    for u in users.find({"role": "student"}).limit(3):
        print(f"ID: {u['_id']}, Name: {u.get('name')}, Dept: {u.get('department')}, College: {u.get('college_name')}")
        
    print("\n--- Tasks Sample ---")
    for t in tasks.find().limit(3):
        print(f"ID: {t['_id']}, Title: {t.get('title')}, user_id: {t.get('user_id')}, type(user_id): {type(t.get('user_id'))}")

    print("\n--- Student Alerts Sample ---")
    for a in db['student_alerts'].find().limit(3):
        print(f"ID: {a['_id']}, Msg: {a.get('message')}, student_id: {a.get('student_id')}, type(student_id): {type(a.get('student_id'))}")

    # Check match for a specific admin dept/college
    # Using admin@test.com's dept if available
    admin = users.find_one({"email": "admin@test.com"})
    if admin:
        dept = admin.get('department')
        college = admin.get('college_name')
        print(f"\nAdmin Dept: {dept}, College: {college}")
        
        # Count tasks for students in this dept manually (robustly)
        students = list(users.find({"department": dept, "college_name": college, "role": "student"}))
        print(f"Students in this dept: {len(students)}")
        
        # Check tasks by both ObjectId and String to see what matches
        obj_ids = [s['_id'] for s in students]
        str_ids = [str(s['_id']) for s in students]
        
        task_count_obj = tasks.count_documents({"user_id": {"$in": obj_ids}})
        task_count_str = tasks.count_documents({"user_id": {"$in": str_ids}})
        
        print(f"Tasks for these students (as ObjectId): {task_count_obj}")
        print(f"Tasks for these students (as String): {task_count_str}")

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        debug_db()
