"""
Flask routes for the Baby Safety Monitoring System
"""
from flask import Response, jsonify
from camera import get_camera_handler
from utils import get_local_ip
from templates import HTML_TEMPLATE


def register_routes(app):
    """Register all Flask routes"""
    
    @app.route('/')
    def index():
        """Serve the main HTML page"""
        return HTML_TEMPLATE
    
    @app.route('/video_feed')
    def video_feed():
        """Stream video feed with object detection"""
        camera = get_camera_handler()
        return Response(
            camera.generate_frames(),
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )
    
    @app.route('/get_ip')
    def get_ip():
        """Get the server's IP address"""
        return jsonify({
            'ip': get_local_ip(),
            'port': 5001
        })
    
    @app.route('/get_alerts')
    def get_alerts():
        """Get current alerts from the detection system"""
        camera = get_camera_handler()
        summary = camera.detection.get_alerts_summary()
        return jsonify(summary)
