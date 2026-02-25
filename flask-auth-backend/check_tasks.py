import requests

BASE_URL = "http://localhost:5000/api"

def check_task_overview():
    # 1. Login
    login_res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "admin@test.com",
        "password": "admin123"
    })
    token = login_res.json().get('token')
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Get Overview
    res = requests.get(f"{BASE_URL}/admin/dashboard/overview", headers=headers)
    data = res.json()
    
    print(f"\nAPI Response Info:")
    print(f"Department: '{data.get('department')}'")
    print(f"College: '{data.get('college_name')}'")
    
    print("\n--- Dashboard Overview: Tasks ---")
    tasks_data = data.get('tasks', {})
    print(f"Total: {tasks_data.get('total')}")
    print(f"Pending: {tasks_data.get('pending')}")
    print(f"Completed: {tasks_data.get('completed')}")
    print(f"Recent Count: {len(tasks_data.get('recent', []))}")
    
    if tasks_data.get('recent'):
        print("\nRecent Tasks Sample:")
        for t in tasks_data['recent']:
            print(f"- {t.get('title')} (Student: {t.get('student_name')}, Priority: {t.get('priority')})")

if __name__ == "__main__":
    check_task_overview()
