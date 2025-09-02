# VidGuard: AI-Powered Emergency Event Detector for CCTV Feeds

VidGuard is an AI-powered system that detects emergency events such as large motion, fire, and no motion in CCTV video feeds. It uses OpenCV for video analysis and provides a Flask-based API for integration.

<img width="1883" height="858" alt="Screenshot 2025-07-24 214709" src="https://github.com/user-attachments/assets/8fcda206-655a-45e4-9045-6df4f7ca689d" />

<img width="1886" height="853" alt="Screenshot 2025-07-24 214732" src="https://github.com/user-attachments/assets/f636b60d-424c-4f8b-8bfd-fe5538cab2a4" />

<img width="1919" height="911" alt="Screenshot 2025-07-24 214823" src="https://github.com/user-attachments/assets/c537ebe3-1b68-41c6-9533-136ca9648bd5" />

## Features

- **Emergency Event Detection:** Detects the following events:
    - `large_motion`: Significant movement, which could indicate a fight or accident.
    - `fire_detected`: Presence of fire-like colors in the video frames.
    - `no_motion_long`: Lack of movement for an extended period, which could indicate a fall or collapse.
- **Real-time Analysis:** A real-time analysis endpoint is available for processing individual frames.
- **Alerts:** Can be configured to send SMS and email alerts for detected emergencies (currently disabled).
- **API:** A simple Flask API to upload videos, get event data, and process frames.

## Getting Started

### Prerequisites

- Python 3.7+
- pip

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/VidGuard.git
    cd VidGuard
    ```
2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

To enable SMS and email alerts, you need to configure the following environment variables in `utils.py`:

-   **Twilio (for SMS alerts):**
    -   `TWILIO_ACCOUNT_SID`
    -   `TWILIO_API_KEY`
    -   `TWILIO_API_SECRET`
    -   `TWILIO_FROM_NUMBER`
    -   `TWILIO_TO_NUMBER`
-   **SendGrid (for email alerts):**
    -   `SENDGRID_API_KEY`
    -   `FROM_EMAIL`
    -   `TO_EMAIL`

## Usage

### Running the Application

To run the Flask application, execute the following command:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`.

### API Endpoints

-   **`POST /upload`**: Upload a video for analysis.
-   **`GET /get_events`**: Get the results of the last video analysis.
-   **`POST /process_frame`**: Process a single frame in real-time.

## Deployment on Render

To deploy this application on Render, you can use the following steps:

1.  **Create a new Web Service on Render.**
2.  **Connect your Git repository.**
3.  **Configure the build and start commands:**
    -   **Build Command:** `pip install -r requirements.txt`
    -   **Start Command:** `gunicorn app:app`
4.  **Add your environment variables** for Twilio and SendGrid in the Render dashboard.
5.  **Deploy the service.**

## Folder Structure

```
VidGuard/
├── app.py              # Main Flask application
├── detect_events.py    # Emergency event classifier
├── utils.py            # Helper functions (OpenCV, alerts)
├── videos/             # CCTV videos for analysis
├── outputs/            # Analysis results
├── requirements.txt    # Project dependencies
└── README.md           # This file
```
