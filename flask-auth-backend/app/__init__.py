from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize extensions
jwt = JWTManager()
mongo_client = None
db = None

def get_db():
    """Helper function to get MongoDB database instance"""
    return db

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 86400))
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/ai_student_companion')
    
    # Initialize extensions
    jwt.init_app(app)
    # CORS configuration - Allow all origins temporarily for debugging
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    
    # MongoDB connection
    global mongo_client, db
    try:
        uri = app.config['MONGO_URI']
        is_local = "localhost" in uri or "127.0.0.1" in uri
        
        # Log a masked version of the URI for debugging
        masked_uri = uri[:15] + "..." if len(uri) > 15 else uri
        print(f"[INFO] Connecting to MongoDB. URI starts with: {masked_uri}", flush=True)
        print(f"[INFO] Mode: {'LOCAL' if is_local else 'REMOTE'}", flush=True)
        
        mongo_client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        
        # Explicitly get the database name from the URI or fallback
        # This fixes issues where get_database() might return 'test'
        from pymongo.uri_parser import parse_uri
        parsed = parse_uri(uri)
        db_name = parsed['database'] or 'ai_student_companion'
        print(f"[INFO] Using database: {db_name}", flush=True)
        
        db = mongo_client[db_name]
        # We don't ping here to prevent startup crash; let routes handle errors
        print("[OK] MongoDB client initialized", flush=True)
    except Exception as e:
        print(f"[ERROR] MongoDB initialization failed: {e}", flush=True)
        # Don't raise here, allow the app to start so logs can be seen
    
    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.student_routes import student_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.attendance_routes import attendance_bp
    from app.routes.student_profile_routes import student_profile_bp
    from app.routes.admin_student_routes import admin_student_bp
    from app.routes.ai_chat_routes import ai_chat_bp
    from app.routes.insights_routes import insights_bp
    from app.routes.alerts_routes import alerts_bp
    from app.routes.task_reminder_routes import task_reminder_bp
    from app.routes.student_dashboard_routes import student_dashboard_bp
    from app.routes.admin_dashboard_routes import admin_dashboard_bp # NEW
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(student_bp, url_prefix='/api/student')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(attendance_bp, url_prefix='/api')
    app.register_blueprint(student_profile_bp, url_prefix='/api/student')
    app.register_blueprint(admin_student_bp, url_prefix='/api')
    app.register_blueprint(ai_chat_bp, url_prefix='/api')
    app.register_blueprint(insights_bp, url_prefix='/api')
    app.register_blueprint(alerts_bp, url_prefix='/api')
    app.register_blueprint(task_reminder_bp, url_prefix='/api/student')
    app.register_blueprint(student_dashboard_bp, url_prefix='/api/student')
    app.register_blueprint(admin_dashboard_bp, url_prefix='/api/admin') # NEW
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'error': 'Token has expired', 'message': 'Please login again'}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'error': 'Invalid token', 'message': 'Token verification failed'}, 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {'error': 'Authorization required', 'message': 'Token is missing'}, 401
    
    # Health check
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy'}, 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def index():
        return {
            'message': 'AI Student Companion API',
            'version': '2.0.0',
            'new_features': ['AI Insights', 'AI Alerts'],
            'endpoints': {
                'auth': {
                    'register': 'POST /api/auth/register',
                    'login': 'POST /api/auth/login'
                },
                'student': {
                    'profile': 'GET/PUT /api/student/profile',
                    'attendance': 'GET /api/student/attendance',
                    'ai_chat': 'POST /api/student/ai/chat',
                    'insights': 'GET /api/student/insights',
                    'insights_generate': 'POST /api/student/insights/generate',
                    'alerts': 'GET /api/student/alerts',
                    'alerts_generate': 'POST /api/student/alerts/generate'
                },
                'admin': {
                    'students': 'GET /api/admin/students',
                    'attendance_summary': 'GET /api/admin/attendance/summary',
                    'mark_attendance': 'POST /api/admin/attendance/mark'
                }
            }
        }, 200
    
    return app
