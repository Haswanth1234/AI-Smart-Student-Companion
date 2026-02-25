import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key: {api_key[:10]}...")

genai.configure(api_key=api_key)

# Use the correct model from your list
model = genai.GenerativeModel('models/gemini-2.5-flash')

try:
    response = model.generate_content("Say hello in one sentence")
    print("✅ SUCCESS!")
    print("Response:", response.text)
except Exception as e:
    print("❌ FAILED!")
    print("Error:", str(e))