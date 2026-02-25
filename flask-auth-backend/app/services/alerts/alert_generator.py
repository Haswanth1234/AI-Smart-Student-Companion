from app.models.student_alert import StudentAlert
from app.models.student_profile import StudentProfile
from app.models.user import User
from bson import ObjectId
from datetime import datetime, timedelta

class AlertGenerator:
    """Generate automated alerts for students"""
    
    def __init__(self):
        self.alert_model = StudentAlert()
        self.profile_model = StudentProfile()
        self.user_model = User()
    
    def generate_alerts_for_student(self, user_id):
        """
        Check all conditions and generate relevant alerts
        
        Args:
            user_id (str): Student's user ID
        
        Returns:
            list: List of generated alert IDs
        """
        profile = self.profile_model.find_by_user_id(user_id)
        
        if not profile:
            return []
        
        generated_alerts = []
        
        # Check each alert condition
        generated_alerts.extend(self._check_attendance_alert(user_id, profile))
        generated_alerts.extend(self._check_fail_risk_alert(user_id, profile))
        generated_alerts.extend(self._check_excellence_alert(user_id, profile))
        generated_alerts.extend(self._check_improvement_alert(user_id, profile))
        
        return generated_alerts
    
    def _check_attendance_alert(self, user_id, profile):
        """Check if attendance is below 75%"""
        alerts = []
        attendance = profile.get('attendance_percentage', 0)
        
        if attendance < 75:
            severity = "high" if attendance < 65 else "medium"
            
            alert_data = {
                'user_id': ObjectId(user_id),
                'alert_type': 'low_attendance',
                'severity': severity,
                'title': 'Attendance Alert',
                'message': f'Your attendance is {attendance}% - below the 75% requirement. Attend classes regularly to avoid eligibility issues.',
                'context': {
                    'current_value': attendance,
                    'threshold': 75,
                    'classes_needed': self._calculate_classes_needed(attendance)
                }
            }
            
            alert_id = self.alert_model.create(alert_data)
            alerts.append(alert_id)
        
        return alerts
    
    def _check_fail_risk_alert(self, user_id, profile):
        """Check if student is at risk of failing"""
        alerts = []
        marks = profile.get('semester_marks', [])
        
        if marks:
            # Handle list of dicts {subject, marks} or legacy list of ints
            if len(marks) > 0 and isinstance(marks[0], dict):
                marks_values = [m['marks'] for m in marks if 'marks' in m]
            else:
                marks_values = marks
                
            if marks_values:
                avg_marks = sum(marks_values) / len(marks_values)
            
            if avg_marks < 35:
                alert_data = {
                    'user_id': ObjectId(user_id),
                    'alert_type': 'fail_risk',
                    'severity': 'high',
                    'title': 'Academic Alert',
                    'message': f'Your average is {avg_marks:.1f}% - below passing marks. Schedule a meeting with your academic advisor immediately.',
                    'context': {
                        'average_marks': avg_marks,
                        'pass_mark': 35
                    }
                }
                
                alert_id = self.alert_model.create(alert_data)
                alerts.append(alert_id)
        
        return alerts
    
    def _check_excellence_alert(self, user_id, profile):
        """Check if student is performing excellently"""
        alerts = []
        marks = profile.get('semester_marks', [])
        attendance = profile.get('attendance_percentage', 0)
        
        if marks:
            # Handle list of dicts {subject, marks} or legacy list of ints
            if len(marks) > 0 and isinstance(marks[0], dict):
                marks_values = [m['marks'] for m in marks if 'marks' in m]
            else:
                marks_values = marks
                
            if marks_values:
                avg_marks = sum(marks_values) / len(marks_values)
            
            if avg_marks >= 85 and attendance >= 90:
                alert_data = {
                    'user_id': ObjectId(user_id),
                    'alert_type': 'excellence',
                    'severity': 'low',
                    'title': 'Excellence Recognition',
                    'message': f'Outstanding performance! {avg_marks:.1f}% average with {attendance}% attendance. Keep up the excellent work!',
                    'context': {
                        'average_marks': avg_marks,
                        'attendance': attendance
                    }
                }
                
                alert_id = self.alert_model.create(alert_data)
                alerts.append(alert_id)
        
        return alerts
    
    def _check_improvement_alert(self, user_id, profile):
        """Check if student has improved significantly"""
        alerts = []
        
        # Get current and previous insights to compare
        # For demo, skip this - you would compare with previous semester
        
        return alerts
    
    def _calculate_classes_needed(self, current_attendance):
        """Calculate classes needed to reach 75%"""
        if current_attendance >= 75:
            return 0
        
        # Simple calculation (assuming 100 total classes)
        total_classes = 100
        attended = (current_attendance / 100) * total_classes
        needed = (75 / 100) * total_classes - attended
        
        return max(0, int(needed))