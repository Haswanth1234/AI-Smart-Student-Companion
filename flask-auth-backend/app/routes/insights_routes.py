from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.insights.insights_generator import InsightsGenerator
from app.models.student_insight import StudentInsight
from app.middleware.auth_middleware import role_required

insights_bp = Blueprint('insights', __name__)
insights_generator = InsightsGenerator()
insight_model = StudentInsight()


@insights_bp.route('/student/insights/generate', methods=['POST'])
@jwt_required()
@role_required(['student'])
def generate_insights():
    """
    Generate new insights for current student
    
    POST /api/student/insights/generate
    
    Response:
    {
        "message": "Insights generated successfully",
        "insights": {...}
    }
    """
    try:
        user_id = get_jwt_identity()
        insights = insights_generator.generate_insights(user_id)
        
        return jsonify({
            'message': 'Insights generated successfully',
            'insights': {
                'learning_level': insights['learning_level'],
                'average_marks': insights['average_marks'],
                'strengths': insights['strengths'],
                'weak_areas': insights['weak_areas'],
                'performance_trend': insights['performance_trend'],
                'attendance_percentage': insights['attendance_percentage'],
                'recommendations': insights['recommendations']
            }
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to generate insights', 'details': str(e)}), 500


@insights_bp.route('/student/insights', methods=['GET'])
@jwt_required()
@role_required(['student'])
def get_insights():
    """
    Get latest insights for current student
    
    GET /api/student/insights
    
    Response:
    {
        "insights": {...}
    }
    """
    try:
        user_id = get_jwt_identity()
        insights = insight_model.find_by_user_id(user_id)
        
        if not insights:
            return jsonify({'message': 'No insights available. Generate insights first.'}), 404
        
        # Format response
        return jsonify({
            'insights': {
                'learning_level': insights.get('learning_level'),
                'average_marks': insights.get('average_marks'),
                'strengths': insights.get('strengths', []),
                'weak_areas': insights.get('weak_areas', []),
                'performance_trend': insights.get('performance_trend'),
                'attendance_percentage': insights.get('attendance_percentage'),
                'recommendations': insights.get('recommendations', []),
                'generated_at': insights.get('generated_at').isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch insights', 'details': str(e)}), 500