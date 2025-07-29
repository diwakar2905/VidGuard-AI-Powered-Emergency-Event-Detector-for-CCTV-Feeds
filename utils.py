import cv2
import numpy as np
from twilio.rest import Client
import os
import requests

# --- Sirf OpenCV aur Twilio SMS alert use ho raha hai ---

# Twilio credentials (replace with your actual values)
TWILIO_ACCOUNT_SID = "SKc98169bffcf4df9c4a33a1dec370fb12"
TWILIO_API_KEY = "Vidguard_key"
TWILIO_API_SECRET = "eWwEXx2KtUA49sFVoG5LkUPsEluoeCDz"
TWILIO_FROM_NUMBER = "+918894804205"   # Your Twilio phone number
TWILIO_TO_NUMBER = "+918894804205"   # Your mobile number

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', 'YOUR_SENDGRID_API_KEY')
FROM_EMAIL = os.environ.get('FROM_EMAIL', 'your@email.com')
TO_EMAIL = os.environ.get('TO_EMAIL', 'your@email.com')

def send_sms_alert(message):
    """
    Twilio se SMS bhejne ka function.
    """
    try:
        client = Client(TWILIO_API_KEY, TWILIO_API_SECRET, TWILIO_ACCOUNT_SID)
        client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=TWILIO_TO_NUMBER
        )
        print("SMS alert bhej diya gaya!")
    except Exception as e:
        print("SMS bhejne me error:", e)

def send_email_alert(subject, message):
    """
    SendGrid se email bhejne ka function.
    """
    if SENDGRID_API_KEY == 'YOUR_SENDGRID_API_KEY':
        print('SendGrid API key not set. Email not sent.')
        return
    data = {
        "personalizations": [
            {"to": [{"email": TO_EMAIL}]}
        ],
        "from": {"email": FROM_EMAIL},
        "subject": subject,
        "content": [
            {"type": "text/plain", "value": message}
        ]
    }
    try:
        response = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={
                "Authorization": f"Bearer {SENDGRID_API_KEY}",
                "Content-Type": "application/json"
            },
            json=data
        )
        if response.status_code == 202:
            print("Email alert bhej diya gaya!")
        else:
            print("Email bhejne me error:", response.text)
    except Exception as e:
        print("Email bhejne me error:", e)

def analyze_video_opencv(video_path):
    """
    OpenCV se video analyze karo (motion, fire, no motion detection).
    """
    cap = cv2.VideoCapture(video_path)
    prev_frame = None
    events = []
    frame_count = 0
    no_motion_frames = 0
    fps = cap.get(cv2.CAP_PROP_FPS) or 25

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if prev_frame is None:
            prev_frame = gray
            continue

        # Motion detection
        frame_delta = cv2.absdiff(prev_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        motion = cv2.countNonZero(thresh)

        # Fire-like color detection (lots of red/orange)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_fire = np.array([10, 100, 100])
        upper_fire = np.array([25, 255, 255])
        fire_mask = cv2.inRange(hsv, lower_fire, upper_fire)
        fire_pixels = cv2.countNonZero(fire_mask)

        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) // 1000
        time_str = f"{int(timestamp//60):02d}:{int(timestamp%60):02d}"

        # Large motion = possible fight/accident
        if motion > 10000:
            events.append({
                "label": "large_motion",
                "timestamp": time_str,
                "score": float(motion) / (frame.shape[0]*frame.shape[1])
            })
            no_motion_frames = 0
        # Fire color detected
        elif fire_pixels > 5000:
            events.append({
                "label": "fire_detected",
                "timestamp": time_str,
                "score": float(fire_pixels) / (frame.shape[0]*frame.shape[1])
            })
            no_motion_frames = 0
        # No motion for 5 seconds = possible fall/collapse
        elif motion < 100:
            no_motion_frames += 1
            if no_motion_frames > fps * 5:
                events.append({
                    "label": "no_motion_long",
                    "timestamp": time_str,
                    "score": 1.0
                })
                no_motion_frames = 0
        else:
            no_motion_frames = 0

        prev_frame = gray
        frame_count += 1

    cap.release()
    return {"events": events}