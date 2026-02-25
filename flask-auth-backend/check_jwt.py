import requests
import jwt # PyJWT

BASE_URL = "http://localhost:5000/api"

def check_jwt():
    # 1. Login
    login_res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "admin@test.com",
        "password": "admin123"
    })
    token = login_res.json().get('token')
    
    # 2. Decode (without verification just to see claims)
    decoded = jwt.decode(token, options={"verify_signature": False})
    print("\n--- JWT Claims ---")
    for k, v in decoded.items():
        print(f"{k}: '{v}'")

if __name__ == "__main__":
    check_jwt()
