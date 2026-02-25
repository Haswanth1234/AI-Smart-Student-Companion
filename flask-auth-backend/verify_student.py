
import requests

BASE_URL = "http://localhost:5000/api"

def test_student_flow():
    # 1. Login
    print("Attempting Student Login...")
    login_payload = {
        "email": "student@test.com",
        "password": "student123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
        
        if response.status_code == 200:
            print("Login Successful!")
            data = response.json()
            token = data.get('token')
            print(f"Token received: {token[:20]}...")
            
            # 2. Access Protected Route
            print("\nAttempting to access Student Profile...")
            headers = {"Authorization": f"Bearer {token}"}
            profile_response = requests.get(f"{BASE_URL}/student_profile/profile", headers=headers)
            
            if profile_response.status_code == 200:
                print("Student Profile Access Successful!")
                print(profile_response.json())
            else:
                print(f"Profile Access Failed: {profile_response.status_code}")
                print(profile_response.text)
        else:
            print(f"Login Failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_student_flow()
