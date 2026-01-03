"""
Baby Safety Monitoring System - Main Entry Point
"""
import sys
from app import create_app

if __name__ == '__main__':
    app = create_app()
    
    print("\n" + "="*60)
    print("🚨 AUTOMATIC ALERT SYSTEM - Baby Safety Monitor")
    print("="*60)
    
    import socket
    
    # Get local IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "localhost"
    
    print(f"\n✅ Server starting...")
    print(f"🌐 Local access:  http://localhost:5001")
    print(f"📱 Mobile access: http://{local_ip}:5001")
    print(f"\n🔔 AUTOMATIC ALERTS ENABLED:")
    print(f"   • Visual alerts on video feed")
    print(f"   • Sound alerts every 2 seconds")
    print(f"   • Phone vibration (if supported)")
    print(f"   • Browser notifications")
    print(f"   • No clicking needed!")
    print("\n" + "="*60)
    print("Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
