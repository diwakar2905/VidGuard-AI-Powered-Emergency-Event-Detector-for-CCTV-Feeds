# === app.py (Flask Backend) ===
from flask import Flask, render_template, request, jsonify
import os
import re
import json
import base64
import cv2
import numpy as np
from utils import analyze_video_opencv, send_sms_alert, send_email_alert
from detect_events import classify_emergency

app = Flask(__name__)
UPLOAD_FOLDER = 'videos'
OUTPUT_FOLDER = 'outputs'
SNAPSHOT_FOLDER = os.path.join(OUTPUT_FOLDER, 'snapshots')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SNAPSHOT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['video']
    filename = re.sub(r'\s+', '_', file.filename)
    video_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(video_path)

    analysis_result = analyze_video_opencv(video_path)
    events = analysis_result.get("events", [])
    emergency_events = classify_emergency(events)

    # Send alerts for each emergency event
    for event in emergency_events:
        msg = f"Emergency Detected: {event['label'].upper()} at {event['timestamp']} (Confidence: {event['confidence']:.2f})"
        # send_sms_alert(msg)  # SMS alert temporarily disabled
        # send_email_alert("VidGuard Emergency Alert", msg)  # Email alert temporarily disabled

    # Save results
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    with open(os.path.join(OUTPUT_FOLDER, 'emergency_events.json'), 'w') as f:
        json.dump({"events": emergency_events}, f, indent=2)

    return jsonify(emergency_events)

@app.route('/get_events', methods=['GET'])
def get_events():
    try:
        with open(os.path.join(OUTPUT_FOLDER, 'emergency_events.json')) as f:
            data = json.load(f)
            return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/process_frame', methods=['POST'])
def process_frame():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify([])
    # Decode base64 image
    image_data = data['image'].split(',')[1] if ',' in data['image'] else data['image']
    nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if frame is None:
        return jsonify([])
    # Analyze single frame (adapted from analyze_video_opencv)
    events = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    # Fire-like color detection (lots of red/orange)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_fire = np.array([10, 100, 100])
    upper_fire = np.array([25, 255, 255])
    fire_mask = cv2.inRange(hsv, lower_fire, upper_fire)
    fire_pixels = cv2.countNonZero(fire_mask)
    # Large motion detection (not possible with single frame, so skip)
    # No motion detection (not possible with single frame, so skip)
    timestamp = "LIVE"
    if fire_pixels > 5000:
        events.append({
            "label": "fire_detected",
            "timestamp": timestamp,
            "score": float(fire_pixels) / (frame.shape[0]*frame.shape[1])
        })
    # Classify and return
    emergency_events = classify_emergency(events)
    # Send alerts for each emergency event
    for event in emergency_events:
        msg = f"Emergency Detected: {event['label'].upper()} at {event['timestamp']} (Confidence: {event['confidence']:.2f})"
        # send_sms_alert(msg)  # SMS alert temporarily disabled
        # send_email_alert("VidGuard Emergency Alert", msg)  # Email alert temporarily disabled
    return jsonify(emergency_events)

if __name__ == '__main__':
    app.run(debug=True)
