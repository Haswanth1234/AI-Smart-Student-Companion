def calculate_learning_level(marks_list):
    """
    Calculate student's learning level based on average marks
    
    Args:
        marks_list (list): List of marks
    
    Returns:
        tuple: (level_name, average_marks)
    """
    if not marks_list:
        return "Unknown", 0
    
    avg_marks = sum(marks_list) / len(marks_list)
    
    if avg_marks < 35:
        level = "Below Average"
    elif avg_marks < 40:
        level = "Slow Learner"
    elif avg_marks <= 70:
        level = "Intermediate Learner"
    else:
        level = "Advanced Learner"
    
    return level, round(avg_marks, 2)


def analyze_strengths_weaknesses(subject_marks):
    """
    Identify strengths and weak areas
    
    Args:
        subject_marks (dict): {"subject_name": marks}
    
    Returns:
        tuple: (strengths, weak_areas)
    """
    strengths = []
    weak_areas = []
    
    for subject, marks in subject_marks.items():
        if marks >= 85:
            strengths.append({
                "subject": subject,
                "marks": marks,
                "insight": f"Outstanding performance in {subject}"
            })
        elif marks < 40:
            weak_areas.append({
                "subject": subject,
                "marks": marks,
                "insight": f"Needs significant improvement in {subject}"
            })
        elif marks < 50:
            weak_areas.append({
                "subject": subject,
                "marks": marks,
                "insight": f"Requires focus on {subject} fundamentals"
            })
    
    return strengths, weak_areas


def analyze_performance_trend(current_marks, previous_marks):
    """
    Analyze if performance is improving, declining, or consistent
    
    Args:
        current_marks (list): Current semester marks
        previous_marks (list): Previous semester marks
    
    Returns:
        tuple: (trend, percentage_change)
    """
    if not previous_marks:
        return "consistent", 0
    
    current_avg = sum(current_marks) / len(current_marks)
    previous_avg = sum(previous_marks) / len(previous_marks)
    
    change = current_avg - previous_avg
    percentage_change = (change / previous_avg) * 100 if previous_avg > 0 else 0
    
    if percentage_change > 5:
        trend = "improving"
    elif percentage_change < -5:
        trend = "declining"
    else:
        trend = "consistent"
    
    return trend, round(percentage_change, 2)


def analyze_attendance_impact(attendance_percentage, average_marks):
    """
    Analyze how attendance affects performance
    
    Args:
        attendance_percentage (float): Student's attendance %
        average_marks (float): Student's average marks
    
    Returns:
        str: positive/neutral/negative
    """
    if attendance_percentage >= 85 and average_marks >= 70:
        return "positive"
    elif attendance_percentage < 75 and average_marks < 50:
        return "negative"
    else:
        return "neutral"


def generate_recommendations(learning_level, weak_areas, attendance_percentage, trend):
    """
    Generate personalized recommendations
    
    Args:
        learning_level (str): Student's learning level
        weak_areas (list): List of weak subjects
        attendance_percentage (float): Attendance %
        trend (str): Performance trend
    
    Returns:
        list: List of recommendation strings
    """
    recommendations = []
    
    # Attendance recommendations
    if attendance_percentage < 75:
        recommendations.append("⚠️ Urgent: Improve attendance to at least 75% to maintain eligibility")
    elif attendance_percentage < 85:
        recommendations.append("📊 Aim for 85%+ attendance for better academic outcomes")
    
    # Performance trend recommendations
    if trend == "declining":
        recommendations.append("📉 Performance declining - schedule consultation with faculty")
    elif trend == "improving":
        recommendations.append("🎯 Great progress! Keep up the momentum")
    
    # Weak areas recommendations
    if weak_areas:
        subjects = [w['subject'] for w in weak_areas[:2]]
        recommendations.append(f"📚 Focus extra time on: {', '.join(subjects)}")
    
    # Learning level specific recommendations
    if learning_level == "Advanced Learner":
        recommendations.append("🚀 Pursue advanced projects, research, or competitive programming")
    elif learning_level == "Intermediate Learner":
        recommendations.append("💪 Practice more problems and work on real-world projects")
    elif learning_level in ["Slow Learner", "Below Average"]:
        recommendations.append("📖 Focus on building strong fundamentals step-by-step")
    
    return recommendations