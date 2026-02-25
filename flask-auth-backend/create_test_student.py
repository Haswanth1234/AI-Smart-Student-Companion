
from app import create_app
from app.models.user import User
from app.utils.password_utils import hash_password

app = create_app()

with app.app_context():
    user_model = User()
    
    # delete if exists
    existing = user_model.find_by_email('student@test.com')
    if existing:
        user_model.collection.delete_one({'email': 'student@test.com'})
        print("Deleted existing student@test.com")

    # Create new
    student_data = {
        'name': 'Test Student',
        'email': 'student@test.com',
        'password': hash_password('student123'),
        'role': 'student',
        'department': 'COMPUTER SCIENCE',
        'college_name': 'ENGINEERING COLLEGE',
        'roll_number': 'TEST001'
    }
    
    user_id = user_model.create(student_data)
    print(f"Created student user: student@test.com / student123 with ID: {user_id}")
