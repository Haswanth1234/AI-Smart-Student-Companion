from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print(f"\\n[INFO] Starting Flask server on port {port}")
    print(f"[INFO] Debug mode: {debug}")
    print(f"[INFO] API Base URL: http://localhost:{port}/api")
    print(f"[INFO] Health Check: http://localhost:{port}/health\\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
