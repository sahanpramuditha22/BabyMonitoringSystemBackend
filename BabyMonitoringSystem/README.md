# Baby Safety Monitoring System

A real-time AI-powered baby safety monitoring system that uses YOLO object detection to identify hazards near infants and provides automatic alerts.

## Project Structure

```
BabyMonitoringSystem/
├── main.py                 # Entry point - start here to run the application
├── app.py                  # Flask application factory
├── config.py               # Configuration settings
├── camera.py               # Camera handler and frame generation
├── detection.py            # Detection logic and alert processing
├── models.py               # YOLO model initialization
├── routes.py               # Flask routes
├── templates.py            # HTML template
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Features

- **Real-time Object Detection**: Uses YOLO model to detect babies and hazards
- **Distance Calculation**: Calculates distance between baby and hazards
- **Automatic Alerts**: Visual, audio, and vibration alerts when hazards are detected
- **Web Interface**: Live video feed with detection overlay
- **Mobile Support**: Access from any device on the same network
- **Alert History**: Tracks and displays recent alerts

## Installation

1. **Clone or download this project**

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Place your YOLO model**:
   - Ensure `my_model4.pt` is in the project root directory
   - Or update the `MODEL_PATH` in [config.py](config.py)

## Running the Application

Simply run:

```bash
python main.py
```

The server will start at:

- **Local access**: http://localhost:5001
- **Mobile access**: http://<your-ip>:5001 (displayed in console)

## Configuration

Edit [config.py](config.py) to customize:

- Model path and detection thresholds
- Alert distance thresholds (CRITICAL_DISTANCE, WARNING_DISTANCE)
- Camera settings (resolution, frame rate)
- Server settings (host, port)

## File Descriptions

| File                         | Purpose                                          |
| ---------------------------- | ------------------------------------------------ |
| [main.py](main.py)           | Entry point - initializes and runs Flask app     |
| [app.py](app.py)             | Flask app factory and initialization             |
| [config.py](config.py)       | All configuration constants                      |
| [camera.py](camera.py)       | Camera capture and frame generation              |
| [detection.py](detection.py) | Object detection and alert logic                 |
| [models.py](models.py)       | YOLO model loading and management                |
| [routes.py](routes.py)       | Flask API routes                                 |
| [templates.py](templates.py) | HTML/JavaScript interface                        |
| [utils.py](utils.py)         | Helper functions (distance calc, IP, timestamps) |

## How It Works

1. **Camera Input**: Captures frames from webcam at 640x480
2. **Detection**: YOLO detects babies and hazards in each frame
3. **Distance Calculation**: Calculates distance between detected baby and hazards
4. **Alert Generation**: Creates alerts based on distance thresholds
5. **Visualization**: Draws detection boxes, lines, and alert status on video
6. **Notification**: Sends alerts to web interface with sound/vibration

## Alert Levels

- **GREEN (SAFE)**: Distance > 200px
- **ORANGE (WARNING)**: Distance 100-200px
- **RED (CRITICAL)**: Distance < 100px

## Browser Support

- Chrome/Edge: Full support (Web Audio API, vibration)
- Firefox: Full support
- Safari: Limited (audio API may have restrictions)
- Mobile: Full support (vibration works on compatible devices)

## Troubleshooting

- **Camera not found**: Check if webcam is connected and not in use
- **Model loading fails**: Ensure `my_model4.pt` exists in project root
- **Port 5001 in use**: Change `SERVER_PORT` in [config.py](config.py)
- **Alerts not working**: Check browser notification permissions

## Development

The code is organized with separation of concerns:

- Config in [config.py](config.py)
- Models in [models.py](models.py)
- Camera/frame logic in [camera.py](camera.py)
- Detection logic in [detection.py](detection.py)
- Web routes in [routes.py](routes.py)

This makes it easy to test, modify, or extend individual components.
