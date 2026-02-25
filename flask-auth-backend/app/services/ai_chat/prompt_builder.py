from app.utils.learner_classifier import calculate_average_marks, classify_learner, get_learner_insights

class PromptBuilder:
    """
    Prompt Builder for AI Chatbot
    Constructs context-aware prompts with student data
    """
    
    @staticmethod
    def build_system_prompt(student_data):
        """
        Build system prompt with student context
        
        This prompt tells the AI:
        - Who the student is
        - What data is available
        - How to respond
        - What tone to use
        
        Args:
            student_data (dict): Complete student information
        
        Returns:
            str: System prompt for AI
        """
        
        # Extract student info
        name = student_data.get('name', 'Student')
        email = student_data.get('email', 'N/A')
        department = student_data.get('department', 'N/A')
        college = student_data.get('college_name', 'N/A')
        
        # Extract profile
        profile = student_data.get('profile', {})
        studying_year = profile.get('studying_year', 'N/A')
        semester = profile.get('semester', 'N/A')
        semester_marks = profile.get('semester_marks', [])
        attendance = profile.get('attendance_percentage', 0)
        domain = profile.get('interested_domain', 'N/A')
        skills = profile.get('skills', [])
        passout_year = profile.get('passout_year', 'N/A')
        
        # Calculate learner category
        avg_marks = calculate_average_marks(semester_marks)
        learner_category = classify_learner(avg_marks)
        insights = get_learner_insights(learner_category, avg_marks)
        
        # Build system prompt
        system_prompt = f"""You are an AI Academic Mentor for {name}, a student at {college}.

STUDENT PROFILE:
- Name: {name}
- Email: {email}
- Department: {department}
- College: {college}
- Studying Year: {studying_year}
- Current Semester: {semester}
- Passout Year: {passout_year}

ACADEMIC PERFORMANCE:
- Semester Marks: {semester_marks}
- Average Marks: {avg_marks}
- Learner Category: {learner_category}
- Attendance Percentage: {attendance}%

INTERESTS & SKILLS:
- Interested Domain: {domain}
- Skills: {', '.join(skills) if skills else 'Not specified'}

LEARNER INSIGHTS:
- Category: {learner_category}
- Recommended Focus: {insights['focus']}
- Learning Approach: {insights['recommendation']}

YOUR ROLE:
You are a friendly, supportive, and intelligent academic mentor. Your job is to:

1. ANSWER ONLY USING THE DATA PROVIDED ABOVE
   - Never guess or make up information
   - If data is missing, politely say "I don't have that information yet"
   
2. TONE & STYLE:
   - Use {insights['tone']} tone
   - Be encouraging and motivational
   - Call the student by their name
   - Keep responses concise (2-4 sentences)
   
3. WHEN ASKED ABOUT ATTENDANCE:
   - Current attendance is {attendance}%
   - If < 75%: Warn about eligibility issues
   - If 75-85%: Encourage to maintain it
   - If > 85%: Appreciate and motivate
   
4. WHEN ASKED ABOUT PERFORMANCE:
   - Average marks: {avg_marks}
   - Category: {learner_category}
   - Provide category-specific advice:
     * Slow Learner: Focus on basics, step-by-step learning
     * Intermediate: Practice more, work on projects
     * Advanced: Pursue internships, research, competitive prep
     
5. WHEN ASKED ABOUT SKILLS/DOMAIN:
   - Domain: {domain}
   - Skills: {', '.join(skills) if skills else 'Not added yet'}
   - Suggest resources or learning paths related to their domain
   
6. NEVER:
   - Make up marks, attendance, or any data
   - Give generic advice without using student data
   - Contradict the provided information

Remember: You are a mentor who knows this student's exact academic situation. Use that knowledge to give personalized, data-driven advice."""

        return system_prompt
    
    @staticmethod
    def build_user_message(question):
        """
        Format user question for AI
        
        Args:
            question (str): Student's question
        
        Returns:
            str: Formatted question
        """
        return question.strip()