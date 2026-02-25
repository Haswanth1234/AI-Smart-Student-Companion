from app import create_app, get_db
import os

app = create_app()
with app.app_context():
    db = get_db()
    users = db['users']
    
    print("\n--- Production Users Check ---")
    for user in users.find():
        print(f"Name: {user.get('name')}")
        print(f"Email: {user.get('email')}")
        print(f"Role: {user.get('role')}")
        print(f"Dept: {user.get('department')}")
        print(f"College: {user.get('college_name')}")
        print(f"Has Password: {'password' in user}")
        print("-" * 20)
