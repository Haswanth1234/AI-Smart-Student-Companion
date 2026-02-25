import os
import sys
from flask import Flask
from pymongo import MongoClient
from datetime import datetime

# Add current directory to path so we can import app
sys.path.append(os.getcwd())

from app import create_app, get_db
from app.aggregations.admin_dashboard import get_student_stats_pipeline, get_learning_levels_pipeline

app = create_app()

def verify_aggregations():
    with app.app_context():
        db = get_db()
        
        # Find a valid student to test with
        student = db.users.find_one({"role": "student"})
        if not student:
            print("No students found in DB to test with.")
            return

        department = student.get('department')
        college_name = student.get('college_name')
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        print(f"--- Testing Aggregation for {department} / {college_name} ---")
        
        # 1. Check Raw Student Count
        raw_student_count = db.users.count_documents({
            "role": "student",
            "department": department,
            "college_name": college_name
        })
        print(f"Raw Student Count in DB: {raw_student_count}")
        
        # 2. Run Student Stats Pipeline
        pipeline = get_student_stats_pipeline(department, college_name, today_str)
        results = list(db.users.aggregate(pipeline))
        
        print("\n--- Student Stats Pipeline Result ---")
        if results:
            print(results[0])
            print(f"Total calculated: {results[0].get('total')}")
            print(f"Raw count: {raw_student_count}")
            if results[0].get('total') == raw_student_count:
                print("[SUCCESS] Pipeline count matches raw DB count.")
            else:
                print(f"[FAILURE] Mismatch! Pipeline: {results[0].get('total')} vs Raw: {raw_student_count}")
        else:
            print("No results found.")
            
        # 3. Check for potential 1:N explosion source
        # Check if any student has multiple profiles
        pipeline_check_profiles = [
            {"$match": {"role": "student", "department": department, "college_name": college_name}},
            {"$lookup": {
                "from": "student_profiles",
                "localField": "_id",
                "foreignField": "user_id",
                "as": "profiles"
            }},
            {"$project": {"profile_count": {"$size": "$profiles"}}},
            {"$match": {"profile_count": {"$gt": 1}}}
        ]
        duplicates = list(db.users.aggregate(pipeline_check_profiles))
        if duplicates:
            print(f"\n[WARNING] Found {len(duplicates)} students with multiple profiles! This causes duplication.")
            for d in duplicates[:5]:
                print(d)
        else:
            print("\n[OK] No students with multiple profiles found.")

if __name__ == "__main__":
    verify_aggregations()
