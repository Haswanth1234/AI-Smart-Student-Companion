from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.ai_chat.ai_chat_service import AIChatService
from app.middleware.auth_middleware import role_required

ai_chat_bp = Blueprint('ai_chat', __name__)
ai_chat_service = AIChatService()


@ai_chat_bp.route('/student/ai/chat', methods=['POST'])
@jwt_required()
@role_required(['student'])
def chat():
    """
    AI Chatbot endpoint for students
    
    Access: Student only
    
    Request Headers:
        Authorization: Bearer <JWT_TOKEN>
    
    Request Body:
        {
            "message": "What is my attendance percentage?"
        }
    
    Response (200):
        {
            "reply": "Your attendance percentage is 87.5%, which is considered good. Keep maintaining it to stay eligible for exams."
        }
    
    Example Questions:
        - "What is my attendance?"
        - "What type of learner am I?"
        - "How can I improve my performance?"
        - "What is my interested domain?"
        - "What skills do I have?"
        - "Am I doing well academically?"
    
    Logic Flow:
        1. Extract student_id from JWT token
        2. Get user message from request
        3. Fetch student profile from database
        4. Calculate learner category
        5. Build AI prompt with student context
        6. Send to Grok AI
        7. Return AI response
    
    AI Behavior:
        - Uses ONLY student's actual data
        - No hallucination or guessing
        - Personalized based on learner category
        - Friendly, supportive tone
        - Concise responses
    
    Security:
        - JWT required
        - Student role required
        - Cannot access other students' data
    
    Errors:
        400: Missing or invalid message
        401: Token missing/invalid
        403: Not a student
        404: Student not found
        500: AI service error
    """
    try:
        # Get student_id from JWT
        student_id = get_jwt_identity()
        
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body required'}), 400
        
        message = data.get('message')
        
        if not message or not message.strip():
            return jsonify({'error': 'Message is required'}), 400
        
        # Process chat
        result = ai_chat_service.chat(student_id, message)
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({
            'error': 'AI chat failed',
            'details': str(e)
        }), 500
