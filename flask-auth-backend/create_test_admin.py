
from app import create_app
from app.models.user import User
from app.utils.password_utils import hash_password

app = create_app()

with app.app_context():
    user_model = User()
    
    # delete if exists
    existing = user_model.find_by_email('admin@test.com')
    if existing:
        user_model.collection.delete_one({'email': 'admin@test.com'})
        print("Deleted existing admin@test.com")

    # Create new
    admin_data = {
        'name': 'Test Admin',
        'email': 'admin@test.com',
        'password': hash_password('admin123'),
        'role': 'admin',
        'department': 'COMPUTER SCIENCE',
        'college_name': 'ENGINEERING COLLEGE'
    }
    
    user_id = user_model.create(admin_data)
    print(f"Created admin user: admin@test.com / admin123 with ID: {user_id}")
