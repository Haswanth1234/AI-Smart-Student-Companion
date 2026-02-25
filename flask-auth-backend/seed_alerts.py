from pymongo import MongoClient
from datetime import datetime, timedelta
import random
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/ai_student_companion')
client = MongoClient(MONGO_URI)
db = client.get_database()

def seed_alerts():
    print("Seeding alerts...")
    
    # 1. Get some students
    students = list(db.users.find({'role': 'student'}))
    
    if not students:
        print("No students found! Cannot seed alerts.")
        return

    alerts_collection = db.student_alerts
    # Clear existing alerts if you want, or just append
    # alerts_collection.delete_many({}) 

    alert_types = ['Attendance', 'Performance', 'Behavior', 'System']
    severities = ['high', 'medium', 'low']
    messages = [
        "Attendance dropped below 75%",
        "Failed mid-term exam",
        "Absent for 3 consecutive days",
        "Late submission of assignment",
        "Library books overdue",
        "Fees payment pending",
        "Excellent performance in project",
        "Disciplinary confirmation required"
    ]

    new_alerts = []
    
    for student in students:
        # Generate 1-3 alerts per student
        for _ in range(random.randint(1, 3)):
            alert = {
                "user_id": student['_id'],
                "student_id": student['_id'], # Legacy/Dual support depending on schema
                "type": random.choice(alert_types),
                "alert_type": random.choice(alert_types), # Schema variation support
                "title": "System Alert",
                "message": random.choice(messages),
                "severity": random.choice(severities),
                "is_read": random.choice([True, False]),
                "created_at": datetime.now() - timedelta(days=random.randint(0, 10)),
                "expires_at": datetime.now() + timedelta(days=30),
                "context": {"details": "Auto-generated alert"}
            }
            new_alerts.append(alert)

    if new_alerts:
        alerts_collection.insert_many(new_alerts)
        print(f"Successfully inserted {len(new_alerts)} alerts.")
    else:
        print("No alerts to insert.")

if __name__ == "__main__":
    seed_alerts()
