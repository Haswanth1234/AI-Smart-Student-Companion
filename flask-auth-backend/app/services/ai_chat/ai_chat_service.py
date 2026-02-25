from app.models.user import User
from app.models.student_profile import StudentProfile
from app.services.ai_chat.prompt_builder import PromptBuilder
from app.services.ai_chat.grok_client import GrokClient
from app.services.insights.insights_generator import InsightsGenerator
from app.services.alerts.alert_generator import AlertGenerator
from app.models.student_insight import StudentInsight
from datetime import datetime, timedelta

class AIChatService:
    """
    AI Chat Service
    Orchestrates AI chat functionality with auto insights/alerts
    """
    
    def __init__(self):
        self.user_model = User()
        self.profile_model = StudentProfile()
        self.prompt_builder = PromptBuilder()
        self.grok_client = GrokClient()
        self.insights_generator = InsightsGenerator()
        self.alert_generator = AlertGenerator()
        self.insight_model = StudentInsight()
    
    def chat(self, student_id, user_message):
        """
        Process chat request with auto insights/alerts generation
        
        Flow:
        1. Validate student
        2. Fetch student data
        3. Check if insights need refresh (daily)
        4. Build AI prompt
        5. Get AI response
        6. Auto-generate alerts if needed
        7. Return response
        
        Args:
            student_id (str): Student's user_id from JWT
            user_message (str): Student's question
        
        Returns:
            dict: AI response with optional insight/alert notifications
        """
        
        # Step 1: Validate student
        student = self.user_model.find_by_id(student_id)
        if not student:
            raise ValueError('Student not found')
        
        if student['role'] != 'student':
            raise ValueError('Only students can use AI chat')
        
        # Step 2: Fetch student profile
        profile = self.profile_model.find_by_user_id(student_id)
        
        # Step 3: Auto-generate insights/alerts (once per day)
        self._auto_generate_insights_and_alerts(student_id, profile)
        
        # Step 4: Prepare student data
        student_data = {
            'name': student.get('name'),
            'email': student.get('email'),
            'department': student.get('department'),
            'college_name': student.get('college_name'),
            'profile': {
                'studying_year': profile.get('studying_year') if profile else None,
                'semester': profile.get('semester') if profile else None,
                'semester_marks': profile.get('semester_marks', []) if profile else [],
                'attendance_percentage': profile.get('attendance_percentage', 0) if profile else 0,
                'interested_domain': profile.get('interested_domain') if profile else None,
                'skills': profile.get('skills', []) if profile else [],
                'passout_year': profile.get('passout_year') if profile else None
            }
        }
        
        # Step 5: Build prompts
        system_prompt = self.prompt_builder.build_system_prompt(student_data)
        formatted_message = self.prompt_builder.build_user_message(user_message)
        
        # Step 6: Get AI response
        try:
            ai_reply = self.grok_client.chat(system_prompt, formatted_message)
        except Exception as e:
            raise Exception(f"AI service error: {str(e)}")
        
        # Step 7: Return response
        return {
            'reply': ai_reply
        }
    
    def _auto_generate_insights_and_alerts(self, student_id, profile):
        """
        Auto-generate insights and alerts if needed
        
        Logic:
        - Generate insights once per day
        - Generate alerts whenever profile changes
        
        Args:
            student_id (str): Student's user ID
            profile (dict): Student's profile data
        """
        if not profile:
            return  # Skip if no profile exists
        
        try:
            # Check if insights need refresh (older than 24 hours)
            latest_insight = self.insight_model.find_by_user_id(student_id)
            
            should_generate = False
            
            if not latest_insight:
                # No insights exist - generate
                should_generate = True
            else:
                # Check if older than 24 hours
                generated_at = latest_insight.get('generated_at')
                if generated_at:
                    time_diff = datetime.utcnow() - generated_at
                    if time_diff > timedelta(hours=24):
                        should_generate = True
            
            # Generate if needed
            if should_generate:
                # Generate insights
                self.insights_generator.generate_insights(student_id)
                
                # Generate alerts
                self.alert_generator.generate_alerts_for_student(student_id)
                
        except Exception as e:
            # Log error but don't fail the chat
            print(f"Auto-generate insights/alerts error: {str(e)}")