"""
HTML template for the web interface
"""

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>👶 Baby Safety Monitor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .video-container {
            background: #000;
            border-radius: 15px;
            overflow: hidden;
            margin: 20px 0;
            position: relative;
        }
        video, img {
            width: 100%;
            height: auto;
            display: block;
        }
        .alert-banner {
            background: #ff4444;
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
            font-weight: bold;
            display: none;
        }
        .status-bar {
            display: flex;
            justify-content: space-around;
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
        }
        .status-item {
            text-align: center;
        }
        .status-label {
            font-size: 14px;
            color: #666;
        }
        .status-value {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }
        .mobile-instructions {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #2196f3;
        }
        .alerts-container {
            background: #fff3cd;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #ffc107;
        }
        .alert-item {
            background: white;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            border-left: 4px solid #ff4444;
            animation: slideIn 0.5s ease;
        }
        .critical-flash {
            animation: pulse 1s infinite;
            background: #ff4444 !important;
            color: white;
        }
        @keyframes slideIn {
            from { transform: translateX(-100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.02); opacity: 0.8; }
            100% { transform: scale(1); opacity: 1; }
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            margin: 5px;
        }
        button:hover {
            opacity: 0.9;
        }
        .button-group {
            text-align: center;
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>👶 Baby Safety Monitoring System</h1>
        <p class="subtitle">Real-time AI-powered hazard detection</p>
        
        <div class="alert-banner critical-flash" id="autoAlertBox" style="display: none;">
            🚨 <span id="alertMessage">ALERT: Hazard detected!</span>
        </div>
        
        <div class="status-bar">
            <div class="status-item">
                <div class="status-label">Status</div>
                <div class="status-value" id="statusText">Active ✅</div>
            </div>
            <div class="status-item">
                <div class="status-label">Camera</div>
                <div class="status-value" id="cameraStatus">Live 📹</div>
            </div>
            <div class="status-item">
                <div class="status-label">AI Model</div>
                <div class="status-value" id="modelStatus">Ready 🤖</div>
            </div>
        </div>
        
        <div class="video-container">
            <img src="/video_feed" id="videoFeed" alt="Live Camera Feed">
        </div>
        
        <div class="alerts-container">
            <h3>🔴 Live Alerts: <span id="alertCount">0</span></h3>
            <div id="realAlertsList">
                <p style="text-align: center; color: #666;">No alerts detected yet</p>
            </div>
        </div>
        
        <div class="mobile-instructions">
            <h3>📱 Mobile Access Instructions:</h3>
            <p>1. Make sure your phone is on the same WiFi network</p>
            <p>2. Open browser and go to: <strong id="ipAddress">Loading...</strong></p>
            <p>3. Bookmark this page for easy access</p>
        </div>
        
        <div class="button-group">
            <button onclick="testAlert()">🚨 Test Alert Sound</button>
            <button id="autoAlertBtn" onclick="toggleAutoAlerts()">✅ Auto-Alerts: ON</button>
        </div>
    </div>

    <script>
        // System variables
        let autoAlertsEnabled = true;
        let lastAlertCheck = 0;
        let isPlayingSound = false;
        let alertCheckInterval;
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            getLocalIP();
            requestNotificationPermission();
            startAutoAlertCheck();
        });
        
        // Get local IP address
        async function getLocalIP() {
            try {
                const response = await fetch('/get_ip');
                const data = await response.json();
                document.getElementById('ipAddress').innerHTML = 
                    `<a href="http://${data.ip}:5001" target="_blank">http://${data.ip}:5001</a>`;
            } catch (error) {
                document.getElementById('ipAddress').innerHTML = 
                    'Could not get IP. Use your computer\\'s IP address';
            }
        }
        
        // Request notification permission
        function requestNotificationPermission() {
            if ("Notification" in window && Notification.permission === "default") {
                Notification.requestPermission();
            }
        }
        
        // Start automatic alert checking
        function startAutoAlertCheck() {
            checkForAlerts();
            alertCheckInterval = setInterval(checkForAlerts, 2000);
        }
        
        // Stop automatic alert checking
        function stopAutoAlertCheck() {
            if (alertCheckInterval) {
                clearInterval(alertCheckInterval);
            }
        }
        
        // Toggle auto-alerts
        function toggleAutoAlerts() {
            autoAlertsEnabled = !autoAlertsEnabled;
            const btn = document.getElementById('autoAlertBtn');
            
            if (autoAlertsEnabled) {
                btn.innerHTML = '✅ Auto-Alerts: ON';
                btn.style.background = '#4CAF50';
                startAutoAlertCheck();
            } else {
                btn.innerHTML = '❌ Auto-Alerts: OFF';
                btn.style.background = '#666';
                stopAutoAlertCheck();
            }
        }
        
        // Main function: Check for alerts
        async function checkForAlerts() {
            if (!autoAlertsEnabled) return;
            
            try {
                const response = await fetch('/get_alerts');
                const data = await response.json();
                
                // Update alert count
                document.getElementById('alertCount').textContent = data.total;
                
                // Update alerts list
                updateAlertsList(data.alerts);
                
                // Check if we have new critical alerts
                if (data.alerts && data.alerts.length > 0) {
                    const latestAlert = data.alerts[0];
                    const alertTime = latestAlert.timestamp * 1000;
                    
                    if (Date.now() - alertTime < 10000) {
                        triggerAutomaticAlert(latestAlert);
                    }
                }
            } catch (error) {
                console.error('Error checking alerts:', error);
            }
        }
        
        // Update the alerts list on the page
        function updateAlertsList(alerts) {
            const alertsList = document.getElementById('realAlertsList');
            
            if (!alerts || alerts.length === 0) {
                alertsList.innerHTML = '<p style="text-align: center; color: #666;">No alerts detected yet</p>';
                return;
            }
            
            alertsList.innerHTML = '';
            
            // Show latest 5 alerts
            alerts.slice(0, 5).forEach(alert => {
                const alertDiv = document.createElement('div');
                alertDiv.className = 'alert-item';
                const time = new Date(alert.timestamp * 1000).toLocaleTimeString();
                alertDiv.innerHTML = `
                    <strong>${alert.type}</strong> - ${time}<br>
                    ${alert.message}<br>
                    <small>Distance: ${alert.distance?.toFixed(1) || 'N/A'}px</small>
                `;
                alertsList.appendChild(alertDiv);
            });
        }
        
        // Trigger automatic alert
        function triggerAutomaticAlert(alert) {
            const alertBox = document.getElementById('autoAlertBox');
            const alertMessage = document.getElementById('alertMessage');
            
            alertMessage.textContent = alert.message;
            alertBox.style.display = 'block';
            
            playAlertSound();
            vibratePhone();
            showBrowserNotification(alert);
            
            setTimeout(() => {
                alertBox.style.display = 'none';
            }, 10000);
        }
        
        // Play alert sound
        function playAlertSound() {
            if (isPlayingSound) return;
            
            isPlayingSound = true;
            
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
            oscillator.frequency.setValueAtTime(600, audioContext.currentTime + 0.1);
            oscillator.frequency.setValueAtTime(800, audioContext.currentTime + 0.2);
            oscillator.frequency.setValueAtTime(600, audioContext.currentTime + 0.3);
            
            gainNode.gain.setValueAtTime(0.5, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.5);
            
            setTimeout(() => {
                isPlayingSound = false;
            }, 500);
        }
        
        // Vibrate phone
        function vibratePhone() {
            if (navigator.vibrate) {
                navigator.vibrate([200, 100, 200, 100, 200, 100, 200]);
            }
        }
        
        // Show browser notification
        function showBrowserNotification(alert) {
            if ("Notification" in window && Notification.permission === "granted") {
                new Notification("🚨 Infant Safety Alert!", {
                    body: alert.message,
                    icon: 'https://img.icons8.com/color/96/000000/baby.png',
                    tag: 'safety-alert',
                    requireInteraction: true
                });
            }
        }
        
        // Manual test alert function
        function testAlert() {
            const testAlert = {
                type: 'TEST',
                message: 'Test alert - System is working!',
                timestamp: Date.now() / 1000,
                distance: 50
            };
            
            triggerAutomaticAlert(testAlert);
            
            setTimeout(() => {
                if (!isPlayingSound) {
                    const audio = new Audio('https://assets.mixkit.co/sfx/preview/mixkit-warning-alarm-buzzer-957.mp3');
                    audio.volume = 0.7;
                    audio.play().catch(e => console.log('Audio error:', e));
                }
            }, 600);
        }
        
        // Auto-refresh video every 30 seconds
        setInterval(() => {
            const video = document.getElementById('videoFeed');
            video.src = '/video_feed?t=' + new Date().getTime();
        }, 30000);
    </script>
</body>
</html>
'''
