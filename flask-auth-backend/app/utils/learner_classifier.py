def calculate_average_marks(semester_marks):
    """
    Calculate average marks from semester marks array
    
    Args:
        semester_marks (list): Array of marks
    
    Returns:
        float: Average marks or 0 if empty
    """
    # Handle new dictionary structure
    if len(semester_marks) > 0 and isinstance(semester_marks[0], dict):
        marks_values = [item['marks'] for item in semester_marks if 'marks' in item]
    else:
        # Legacy list of numbers
        marks_values = semester_marks
        
    if not marks_values:
        return 0.0
        
    return round(sum(marks_values) / len(marks_values), 2)


def classify_learner(average_marks):
    """
    Classify learner based on average marks
    
    Classification:
    - Slow Learner: 35-39
    - Intermediate Learner: 40-70
    - Advanced Learner: 71-100
    - Below Average: < 35
    
    Args:
        average_marks (float): Average of semester marks
    
    Returns:
        str: Learner category
    """
    if average_marks < 35:
        return "Below Average"
    elif 35 <= average_marks <= 39:
        return "Slow Learner"
    elif 40 <= average_marks <= 70:
        return "Intermediate Learner"
    elif 71 <= average_marks <= 100:
        return "Advanced Learner"
    else:
        return "Unknown"


def get_learner_insights(learner_category, average_marks):
    """
    Get learning recommendations based on category
    
    Args:
        learner_category (str): Learner classification
        average_marks (float): Average marks
    
    Returns:
        dict: Insights and recommendations
    """
    insights = {
        "Below Average": {
            "tone": "encouraging and supportive",
            "focus": "Build strong fundamentals, one step at a time",
            "recommendation": "Focus on understanding basics, practice regularly, seek help from teachers"
        },
        "Slow Learner": {
            "tone": "motivational and patient",
            "focus": "Steady progress with structured learning",
            "recommendation": "Follow step-by-step learning, revise concepts multiple times, use visual aids"
        },
        "Intermediate Learner": {
            "tone": "encouraging and guiding",
            "focus": "Skill improvement and practical application",
            "recommendation": "Work on projects, practice problem-solving, explore advanced topics"
        },
        "Advanced Learner": {
            "tone": "challenging and inspiring",
            "focus": "Advanced learning and competitive preparation",
            "recommendation": "Pursue internships, research projects, competitive coding, higher studies"
        }
    }
    
    return insights.get(learner_category, insights["Intermediate Learner"])
