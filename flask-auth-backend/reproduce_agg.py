from app import create_app, get_db
from bson import ObjectId
import json

def reproduce_aggregation():
    app = create_app()
    with app.app_context():
        db = get_db()
        tasks = db['tasks']
        
        department = "COMPUTER SCIENCE"
        college_name = "ENGINEERING COLLEGE"
        
        all_students = list(db['users'].find({"role": "student"}))
        print(f"\nTotal students in collection: {len(all_students)}")
        for s in all_students:
            sid_str = str(s['_id'])
            print(f"Student: '{s.get('name')}', ID: {repr(sid_str)} (len: {len(sid_str)})")
            
        all_tasks = list(tasks.find())
        print(f"\nTotal tasks in collection: {len(all_tasks)}")
        
        for t in all_tasks:
            uid = t.get('user_id')
            title = t.get('title')
            print(f"\nChecking Task: '{title}' with user_id: {repr(uid)}")
            
            try:
                target_id = ObjectId(uid) if isinstance(uid, str) and len(uid)==24 else uid
                
                # Check against our pre-fetched list
                match_found = False
                for s in all_students:
                    if s['_id'] == target_id:
                        print(f"  MATCH FOUND manually with student: '{s.get('name')}'")
                        match_found = True
                        break
                
                if not match_found:
                    print(f"  NO MATCH found in the pre-fetched student list")
            except Exception as e:
                print(f"  Result: Error in comparison: {e}")

if __name__ == "__main__":
    reproduce_aggregation()
