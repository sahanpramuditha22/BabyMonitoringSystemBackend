from flask import Blueprint, render_template, jsonify, Response, stream_with_context
import requests
from config import BACKEND_URL
main = Blueprint('main', __name__)
@main.route('/')
def index():
    return render_template('index.html', backend_url=BACKEND_URL)
@main.route('/alerts')
def alerts():
    try:
        r = requests.get(f"{BACKEND_URL}/get_alerts", timeout=3)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({'alerts': [], 'total': 0, 'error': str(e)})
@main.route('/video')
def video():
    def generate():
        with requests.get(f"{BACKEND_URL}/video_feed", stream=True) as r:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk
    return Response(stream_with_context(generate()), mimetype='multipart/x-mixed-replace; boundary=frame')
from flask import Blueprint, jsonify, request

mobile_app = Blueprint('mobile_app', __name__)

@mobile_app.route('/api/data', methods=['GET'])
def get_data():
    # Example data response
    data = {
        'message': 'Welcome to the mobile app API!',
        'status': 'success'
    }
    return jsonify(data)

@mobile_app.route('/api/data', methods=['POST'])
def post_data():
    # Example of handling POST request
    json_data = request.get_json()
    return jsonify({
        'received': json_data,
        'status': 'success'
    }), 201

@mobile_app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({'status': 'Mobile app is running'})