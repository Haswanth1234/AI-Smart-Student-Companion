from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to MongoDB
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/ai_student_companion')
client = MongoClient(mongo_uri)
db = client.get_database()

print("Updating existing users...")

# Update all users without profile_completed field
result = db['users'].update_many(
    {'profile_completed': {'$exists': False}},  # Find users without the field
    {'$set': {'profile_completed': False}}      # Set it to False
)

print(f"✓ Updated {result.modified_count} users")

# Check if hasw@student.com has a profile
user = db['users'].find_one({'email': 'hasw@student.com'})
if user:
    print(f"\nUser: {user['email']}")
    print(f"Profile completed: {user.get('profile_completed', 'MISSING')}")
    
    # Check if they have a profile in student_profiles
    profile = db['student_profiles'].find_one({'user_id': user['_id']})
    
    if profile:
        print(f"✓ User HAS a profile in student_profiles collection")
        # Update to profile_completed = True since they have a profile
        db['users'].update_one(
            {'_id': user['_id']},
            {'$set': {'profile_completed': True}}
        )
        print(f"✓ Marked profile as completed for {user['email']}")
    else:
        print(f"✗ User does NOT have a profile yet")

print("\nDone! Now restart Flask and login again.")
client.close()