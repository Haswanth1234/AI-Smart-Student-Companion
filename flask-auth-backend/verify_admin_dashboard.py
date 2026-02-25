import requests
import sys

BASE_URL = "http://localhost:5000/api"

def login_admin():
    print("1. Logging in as Admin...")
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "admin@test.com",
            "password": "admin123"
        })
        if response.status_code == 200:
            print("   [SUCCESS] Login successful")
            return response.json().get('token')
        else:
            print(f"   [FAILED] Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"   [ERROR] Connection refused: {e}")
        return None

def test_dashboard(token):
    print("\n2. Testing Admin Dashboard Overview...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/admin/dashboard/overview", headers=headers)
        
        if response.status_code == 200:
            print("   [SUCCESS] Dashboard data retrieved")
            data = response.json()
            print("\n--- Dashboard Data ---")
            print(f"Department: {data.get('department')}")
            print(f"College: {data.get('college_name')}")
            print("\nStudents:")
            for k, v in data.get('students', {}).items():
                print(f"  - {k}: {v}")
            print("\nLearning Levels:")
            for k, v in data.get('learning_levels', {}).items():
                print(f"  - {k}: {v}")
            print("\nAlerts:")
            for k, v in data.get('alerts', {}).items():
                print(f"  - {k}: {v}")
            print("----------------------")
        elif response.status_code == 403:
             print("   [FAILED] 403 Forbidden - Role check failed")
        else:
            print(f"   [FAILED] {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"   [ERROR] {e}")


def test_tasks(token):
    print("\n3. Testing Student Tasks Endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/admin/dashboard/tasks", headers=headers)
        
        if response.status_code == 200:
            print("   [SUCCESS] Tasks data retrieved")
            tasks = response.json()
            print(f"   [INFO] Found {len(tasks)} tasks")
            if len(tasks) > 0:
                print("\n   Sample Task:")
                t = tasks[0]
                print(f"   - Title: {t.get('title')}")
                print(f"   - Student: {t.get('student_name')}")
                print(f"   - Status: {t.get('status')}")
                print(f"   - Priority: {t.get('priority')}")
        else:
            print(f"   [FAILED] {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"   [ERROR] {e}")

    except Exception as e:
        print(f"   [ERROR] {e}")

def test_reports(token):
    print("\n4. Testing Reports Endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/admin/dashboard/reports", headers=headers)
        
        if response.status_code == 200:
            print("   [SUCCESS] Reports data retrieved")
            data = response.json()
            print("\n   Report Data Keys:")
            for k in data.keys():
                print(f"   - {k}")
                
            print(f"\n   Attendance Trend Items: {len(data.get('attendance_trend', []))}")
            print(f"   Top Performers: {len(data.get('top_performers', []))}")
            print(f"   At-Risk Students: {len(data.get('at_risk_students', []))}")
            
        else:
            print(f"   [FAILED] {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"   [ERROR] {e}")

def test_settings(token):
    print("\n5. Testing Settings (Password Change)...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Test Change Password (Mocking a change back to same password)
    # Be careful not to break login for future runs
    # We will change "admin123" to "admin123" to verify the flow works without locking us out
    
    try:
        response = requests.post(f"{BASE_URL}/admin/change-password", headers=headers, json={
            "current_password": "admin123",
            "new_password": "admin123"
        })
        
        if response.status_code == 200:
            print("   [SUCCESS] Password change endpoint working")
        else:
             print(f"   [FAILED] {response.status_code} - {response.text}")
             
    except Exception as e:
        print(f"   [ERROR] {e}")

if __name__ == "__main__":
    token = login_admin()
    if token:
        test_dashboard(token)
        test_tasks(token)
        test_reports(token)
        test_settings(token)
