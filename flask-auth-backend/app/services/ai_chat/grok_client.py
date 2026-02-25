import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GrokClient:
    """Google Gemini Client - Using Gemini 2.5 Flash"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found")
        
        genai.configure(api_key=self.api_key)
        
        # ✅ USE THE LATEST MODEL FROM YOUR LIST
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    def chat(self, system_prompt, user_message):
        """Send chat to Gemini"""
        
        full_prompt = f"""{system_prompt}

Student Question: {user_message}

Respond in 2-4 sentences, friendly and supportive tone."""
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")