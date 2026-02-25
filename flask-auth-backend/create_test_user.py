from app import create_app
from app.models.user import User
from app.utils.password_utils import hash_password

app = create_app()

with app.app_context():
    user_model = User()
    email = "student@example.com"
    
    # Check if user exists
    existing_user = user_model.find_by_email(email)
    
    if existing_user:
        print(f"User {email} already exists. Updating password...")
        user_model.update(existing_user['_id'], {
            'password': hash_password("password123")
        })
        print("Password updated to 'password123'")
    else:
        print(f"Creating new user {email}...")
        user_data = {
            'name': "Test Student",
            'email': email,
            'password': hash_password("password123"),
            'role': "student",
            'department': "CSE",
            'college_name': "Engineering College",
            'profile_completed': True
        }
        user_model.create(user_data)
        print("User created successfully!")
        print("Email: student@example.com")
        print("Password: password123")
