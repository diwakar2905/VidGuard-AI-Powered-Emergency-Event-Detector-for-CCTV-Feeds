# 🔒 VidGuard — AI-Powered Emergency Event Detector for CCTV Feeds
VidGuard is an intelligent, AI-powered surveillance assistant designed to monitor real-time or pre-recorded CCTV footage for potential emergency events. Built using computer vision, it detects critical anomalies such as **large motion** (e.g., fights or accidents), **fire**, and **no motion** (e.g., falls or unconsciousness). VidGuard can be configured to trigger **instant alerts via SMS and email** to ensure rapid emergency response.

---
<img width="1890" height="905" alt="image" src="https://github.com/user-attachments/assets/37566c21-070f-4423-9665-935709405698" />
<img width="1883" height="858" alt="image" src="https://github.com/user-attachments/assets/b01c8c07-3d5a-4a38-8ec4-9bb48d93dd31" />
<img width="1886" height="853" alt="image" src="https://github.com/user-attachments/assets/b5868a61-4ff5-404d-acc9-4f6e795a61a8" />
<img width="1919" height="911" alt="image" src="https://github.com/user-attachments/assets/610aed7b-45f7-4943-86b8-63adf8467a30" />


## 🚀 Features

- 🎥 **Video Analysis** – Upload and analyze pre-recorded videos for emergency detection.
- 📡 **Live Frame Processing** – Analyze webcam/CCTV feed frame-by-frame in real-time.
- 🕴️ **Motion Detection** – Detects significant movement signaling accidents or conflicts.
- 🔥 **Fire Detection** – Color-based detection of fire-like hues (red/orange).
- 💤 **No Motion Detection** – Flags prolonged inactivity that could indicate a collapse.
- 📲 **Alert System** – Optional SMS (Twilio) and Email (SendGrid) alerts on detection.
- 🧠 **Flask Backend** – Lightweight backend for video upload and event reporting.
- 📁 **Event Logging** – Stores detected events in JSON for audit and analysis.

---

## 🛠️ Tech Stack

| Tool         | Purpose                          |
|--------------|----------------------------------|
| Python 3.8+  | Core language                    |
| Flask        | Backend API                      |
| OpenCV       | Video processing and detection   |
| NumPy        | Image matrix operations          |
| Twilio       | SMS alert integration            |
| SendGrid     | Email alert integration          |
| dotenv       | Environment variable management  |

---

## 📦 Installation & Setup

### ✅ Prerequisites

- Python 3.8 or higher
- `pip` installed

### 🔧 1. Clone the Repository

```bash
git clone https://github.com/your-username/VidGuard.git
cd VidGuard
🌐 2. Create and Activate Virtual Environment
bash
Copy
Edit
python -m venv venv

# On Windows
.\venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
📥 3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
🔐 4. Configure Environment Variables (Optional Alerts)
Create a .env file in the project root to enable SMS and email alerts:

env
Copy
Edit
# Twilio (SMS)
TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_API_KEY="SKxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_API_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_FROM_NUMBER="+1234567890"
TWILIO_TO_NUMBER="+1987654321"

# SendGrid (Email)
SENDGRID_API_KEY="SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
FROM_EMAIL="your_sender@example.com"
TO_EMAIL="recipient@example.com"
Note: Alerting functions are commented out in app.py. To activate:

Uncomment send_sms_alert(msg) and send_email_alert(subject, msg)

Ensure .env is properly configured

▶️ Running the Application
Start the Flask server:

bash
Copy
Edit
python app.py
Access the application at:
📍 http://127.0.0.1:5000/

📁 Event Logging
Detected events are logged into event_log.json with:

Event type (e.g., "fire", "motion")

Timestamp

Frame ID

📌 Example Use Cases
Monitor hospital wards for patient falls or unconsciousness

Alert fire emergencies in factories or parking lots

Detect brawls or disturbances in public areas via CCTV

🛡️ Disclaimer
This is a research and prototype-level project. For production use:

Harden the system

Optimize detection algorithms

Use secure credential storage

📫 Contact
For queries, contributions, or suggestions:

📧 Email: your_email@example.com

🧑‍💻 GitHub: your-username
