from app.models.student_insight import StudentInsight
from app.models.student_profile import StudentProfile
from app.models.user import User
from app.utils.performance_analyzer import *
from bson import ObjectId

class InsightsGenerator:
    """Generate AI-powered insights for students"""
    
    def __init__(self):
        self.insight_model = StudentInsight()
        self.profile_model = StudentProfile()
        self.user_model = User()
    
    def generate_insights(self, user_id):
        """
        Generate comprehensive insights for a student
        
        Args:
            user_id (str): Student's user ID
        
        Returns:
            dict: Generated insights
        """
        # Get student data
        user = self.user_model.find_by_id(user_id)
        profile = self.profile_model.find_by_user_id(user_id)
        
        if not profile:
            raise ValueError("Student profile not found")
        
        # Extract data
        semester_marks = profile.get('semester_marks', [])
        attendance_percentage = profile.get('attendance_percentage', 0)
        
        # For demo, create subject-wise marks (you should store this in profile)
        # Assuming semester_marks is a list of overall marks
        subject_marks = {
            "Machine Learning": semester_marks[0] if len(semester_marks) > 0 else 0,
            "Database Systems": semester_marks[1] if len(semester_marks) > 1 else 0,
            "Web Development": semester_marks[2] if len(semester_marks) > 2 else 0,
            "Data Structures": semester_marks[3] if len(semester_marks) > 3 else 0,
        }
        
        # Calculate learning level
        learning_level, average_marks = calculate_learning_level(semester_marks)
        
        # Analyze strengths and weaknesses
        strengths, weak_areas = analyze_strengths_weaknesses(subject_marks)
        
        # Analyze trend (compare with previous semester - for now using same data)
        trend, trend_percentage = analyze_performance_trend(
            semester_marks,
            []  # You should store previous semester marks
        )
        
        # Analyze attendance impact
        attendance_impact = analyze_attendance_impact(attendance_percentage, average_marks)
        
        # Generate recommendations
        recommendations = generate_recommendations(
            learning_level,
            weak_areas,
            attendance_percentage,
            trend
        )
        
        # Build insight document
        insight_data = {
            'user_id': ObjectId(user_id),
            'learning_level': learning_level,
            'average_marks': average_marks,
            'strengths': strengths,
            'weak_areas': weak_areas,
            'performance_trend': trend,
            'trend_percentage': trend_percentage,
            'attendance_percentage': attendance_percentage,
            'attendance_impact': attendance_impact,
            'recommendations': recommendations
        }
        
        # Save to database
        insight_id = self.insight_model.create(insight_data)
        
        return insight_data