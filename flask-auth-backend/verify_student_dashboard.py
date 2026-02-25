import requests
import json
import sys

BASE_URL = "http://localhost:5000/api"

def login_student():
    print("1. Logging in as Student...")
    try:
        # Register a test student if not exists (handling duplicate error)
        try:
            requests.post(f"{BASE_URL}/auth/register", json={
                "name": "Test Student",
                "email": "student@test.com",
                "password": "student123",
                "role": "student",
                "department": "CSE",
                "college_name": "ENGINEERING COLLEGE",
                "roll_number": "CSE101"
            })
        except:
            pass

        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "student@test.com",
            "password": "student123"
        })
        
        if response.status_code == 200:
            print("   [SUCCESS] Login successful")
            return response.json()['token']
        else:
            print(f"   [FAILED] Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"   [ERROR] {e}")
        return None

def test_dashboard_overview(token):
    print("\n2. Testing Student Dashboard Overview...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/student/dashboard/overview", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("   [SUCCESS] Dashboard data retrieved")
            print(f"\n--- Dashboard Data ---")
            print(json.dumps(data, indent=2))
            print("----------------------")
        else:
            print(f"   [FAILED] {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"   [ERROR] {e}")

def test_student_profile(token):
    print("\n3. Testing Student Profile Update...")
    headers = {"Authorization": f"Bearer {token}"}
    
    import random
    phone = f"9{random.randint(100000000, 999999999)}"
    
    # Update profile with phone
    payload = {
        "studying_year": 2,
        "phone": phone,
        "phone": phone,
        "skills": ["Python", "Flask", "React"],
        "semester_marks": [
            {"subject": "Math", "marks": 85},
            {"subject": "Physics", "marks": 90},
            {"subject": "Chemistry", "marks": 78}
        ]
    }
    
    try:
        response = requests.put(f"{BASE_URL}/student/profile", headers=headers, json=payload)
        
        if response.status_code == 200:
            print("   [SUCCESS] Profile updated")
            data = response.json()
            if data['user_info'].get('phone') == phone:
                 print("   [SUCCESS] Phone number verified in response")
            else:
                 print(f"   [FAILED] Phone number mismatch: {data['user_info'].get('phone')}")
            
            # Verify marks structure
            marks = data['profile'].get('semester_marks', [])
            if marks and isinstance(marks[0], dict) and 'subject' in marks[0]:
                 print("   [SUCCESS] Marks structure verified (Subject-Marks)")
            else:
                 print(f"   [FAILED] Marks structure mismatch: {marks}")
        else:
            print(f"   [FAILED] {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"   [ERROR] {e}")

if __name__ == "__main__":
    token = login_student()
    if token:
        test_dashboard_overview(token)
        test_student_profile(token)
