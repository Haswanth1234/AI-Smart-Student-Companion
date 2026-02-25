import requests
import json
import sys
import uuid
import random

BASE_URL = 'http://localhost:5000/api'

def register_and_login():
    """Register a temp user and get token"""
    unique_id = str(uuid.uuid4())[:8]
    email = f"test_task_{unique_id}@example.com"
    password = "password123"
    
    # Generate 10 digit phone number
    phone = f"9{random.randint(100000000, 999999999)}"

    # 1. Register (ignore error if exists)
    print("1. Registering/Logging in user...")
    reg_response = requests.post(f"{BASE_URL}/auth/register", json={
        "name": "Test User",
        "email": email,
        "password": password,
        "confirm_password": password,
        "role": "student",
        "department": "CSE",
        "college_name": "Test College",
        "phone": phone
    })
    print(f"Register Response: {reg_response.status_code} - {reg_response.text}")
    
    # 2. Login
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password,
        "role": "student"
    })
    
    print(f"Login Response: {response.status_code} - {response.text}")

    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        sys.exit(1)
        
    # Check for 'token' or 'access_token'
    data = response.json()
    return data.get('access_token') or data.get('token')

def test_tasks(token):
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Create Task
    print("\n2. Creating Task...")
    task_data = {
        "title": "Study AI",
        "description": "Complete the agentic coding assignment",
        "due_date": "2023-12-31T23:59:59",
        "priority": "high",
        "is_ai_generated": False
    }
    response = requests.post(f"{BASE_URL}/student/tasks", json=task_data, headers=headers)
    print(f"Create Status: {response.status_code}")
    print(response.json())
    
    if response.status_code != 201:
        print("Create failed!")
        return

    task_id = response.json().get('task_id')

    # 4. List Tasks
    print("\n3. Listing Tasks...")
    response = requests.get(f"{BASE_URL}/student/tasks", headers=headers)
    print(f"List Status: {response.status_code}")
    print(response.json())
    
    # 5. Update Task
    print("\n4. Updating Task...")
    update_data = {"status": "completed"}
    response = requests.put(f"{BASE_URL}/student/tasks/{task_id}", json=update_data, headers=headers)
    print(f"Update Status: {response.status_code}")
    print(response.json())

    # 6. Delete Task
    print("\n5. Deleting Task...")
    response = requests.delete(f"{BASE_URL}/student/tasks/{task_id}", headers=headers)
    print(f"Delete Status: {response.status_code}")
    print(response.json())

    print("\n[DONE] verification complete!")

if __name__ == "__main__":
    try:
        token = register_and_login()
        test_tasks(token)
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Could not connect to server. Is it running?")
