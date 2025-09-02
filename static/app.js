const form = document.getElementById('upload-form');
const resultDiv = document.getElementById('result');
const uploadLabel = document.querySelector('.upload-label');
const videoInput = document.getElementById('video-upload');
const uploadProgress = document.getElementById('upload-progress');
const progressBar = document.getElementById('progress-bar');
const progressStatus = document.getElementById('progress-status');
const analyzeOnlyBtn = document.getElementById('analyzeOnlyBtn');

// Drag-and-drop support
['dragenter', 'dragover'].forEach(evt => {
  uploadLabel.addEventListener(evt, e => {
    e.preventDefault();
    uploadLabel.style.background = '#2c2e30';
    uploadLabel.style.borderColor = '#ff4b4b';
  });
});
['dragleave', 'drop'].forEach(evt => {
  uploadLabel.addEventListener(evt, e => {
    e.preventDefault();
    uploadLabel.style.background = '';
    uploadLabel.style.borderColor = '';
  });
});
uploadLabel.addEventListener('drop', e => {
  const files = e.dataTransfer.files;
  if (files.length) {
    videoInput.files = files;
  }
});

// Lottie animation for logo
if (window.lottie) {
  lottie.loadAnimation({
    container: document.getElementById('lottie-logo'),
    renderer: 'svg',
    loop: true,
    autoplay: true,
    // Example Lottie animation URL (replace with your own if desired)
    path: 'https://assets2.lottiefiles.com/packages/lf20_2ks3pjua.json'
  });
}

const loadingDiv = document.getElementById('loading');
const analyzeBtn = document.getElementById('analyzeBtn');

let selectedFile = null;
let fileUploaded = false;

videoInput.addEventListener('change', (e) => {
  selectedFile = e.target.files[0];
  if (selectedFile) {
    uploadProgress.style.display = 'block';
    progressBar.value = 0;
    progressStatus.textContent = 'Ready to upload...';
    analyzeBtn.style.display = 'none';
    analyzeOnlyBtn.style.display = 'inline-block';
    fileUploaded = false;
  }
});

analyzeOnlyBtn.addEventListener('click', async () => {
  if (!selectedFile) return;
  uploadProgress.style.display = 'block';
  progressBar.value = 0;
  progressStatus.textContent = 'Uploading...';
  resultDiv.innerHTML = '';
  loadingDiv.style.display = 'none';

  const formData = new FormData();
  formData.append('video', selectedFile);

  // Use XMLHttpRequest for progress
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/upload', true);

  xhr.upload.onprogress = function (e) {
    if (e.lengthComputable) {
      const percent = Math.round((e.loaded / e.total) * 100);
      progressBar.value = percent;
      progressStatus.textContent = `Uploading... ${percent}%`;
    }
  };

  xhr.onload = function () {
    uploadProgress.style.display = 'none';
    analyzeOnlyBtn.style.display = 'none';
    analyzeBtn.style.display = 'inline-block';
    fileUploaded = true;
    if (xhr.status === 200) {
      const data = JSON.parse(xhr.responseText);
      resultDiv.innerHTML = '';
      if (data.length === 0) {
        resultDiv.innerHTML = "<div class='event-card'><div class='event-label'>No emergency events detected.</div></div>";
      } else {
        data.forEach(event => {
          resultDiv.innerHTML += `
            <div class="event-card">
              <div class="event-label">🛑 ${event.label.toUpperCase()}</div>
              <div class="event-time">⏰ ${event.timestamp}</div>
              <div class="event-confidence">Confidence: ${parseFloat(event.confidence * 100).toFixed(0)}%</div>
            </div>
          `;
        });
      }
      if (window.Toastify) {
        Toastify({
          text: "Analysis Complete ✅",
          backgroundColor: "#ff4b4b",
          duration: 3000
        }).showToast();
      }
    } else {
      resultDiv.innerHTML = '<div class="event-card"><div class="event-label">Upload failed.</div></div>';
    }
  };

  xhr.onerror = function () {
    uploadProgress.style.display = 'none';
    resultDiv.innerHTML = '<div class="event-card"><div class="event-label">Upload failed.</div></div>';
  };

  xhr.send(formData);
});

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  if (!fileUploaded) return;
  // This is a fallback for when the user reloads and the file is already uploaded
});

// Webcam logic
const webcamBtn = document.getElementById('webcam-btn');
const webcamSection = document.querySelector('.webcam-section');
const webcamVideo = document.getElementById('webcam-video');
const stopWebcamBtn = document.getElementById('stop-webcam-btn');
let webcamStream = null;
let webcamInterval = null;

webcamBtn.addEventListener('click', async () => {
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    try {
      webcamStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      webcamVideo.srcObject = webcamStream;
      webcamSection.style.display = '';
      webcamBtn.style.display = 'none';
      webcamInterval = setInterval(sendWebcamFrame, 1000);
    } catch (err) {
      alert('Webcam access denied or not available.');
    }
  } else {
    alert('Webcam not supported in this browser.');
  }
});

stopWebcamBtn.addEventListener('click', () => {
  if (webcamStream) {
    webcamStream.getTracks().forEach(track => track.stop());
    webcamStream = null;
  }
  webcamSection.style.display = 'none';
  webcamBtn.style.display = '';
  clearInterval(webcamInterval);
});

async function sendWebcamFrame() {
  if (!webcamVideo || webcamVideo.readyState !== 4) return;
  loadingDiv.style.display = 'block';
  const canvas = document.createElement('canvas');
  canvas.width = webcamVideo.videoWidth;
  canvas.height = webcamVideo.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(webcamVideo, 0, 0, canvas.width, canvas.height);
  const dataUrl = canvas.toDataURL('image/jpeg');
  // Send to backend
  resultDiv.innerHTML = '';
  try {
    const response = await fetch('/process_frame', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: dataUrl })
    });
    const data = await response.json();
    loadingDiv.style.display = 'none';
    resultDiv.innerHTML = '';
    if (data.length === 0) {
      resultDiv.innerHTML = "<div class='event-card'><div class='event-label'>No emergency events detected.</div></div>";
    } else {
      data.forEach(event => {
        resultDiv.innerHTML += `
          <div class="event-card">
            <div class="event-label">🛑 ${event.label.toUpperCase()}</div>
            <div class="event-time">⏰ ${event.timestamp}</div>
            <div class="event-confidence">Confidence: ${parseFloat(event.confidence * 100).toFixed(0)}%</div>
          </div>
        `;
      });
    }
    // Toast notification
    if (window.Toastify) {
      Toastify({
        text: "Webcam Frame Analyzed ✅",
        backgroundColor: "#ff4b4b",
        duration: 2000
      }).showToast();
    }
  } catch (err) {
    loadingDiv.style.display = 'none';
    resultDiv.innerHTML = '<div class="event-card"><div class="event-label">Webcam frame processing failed.</div></div>';
  }
}

// Spinner CSS (inject if not present)
if (!document.getElementById('spinner-style')) {
  const style = document.createElement('style');
  style.id = 'spinner-style';
  style.innerHTML = `
    .spinner {
      border: 4px solid #f3f3f3;
      border-top: 4px solid #ff4b4b;
      border-radius: 50%;
      width: 36px;
      height: 36px;
      animation: spin 1s linear infinite;
      margin: 0 auto 1em auto;
      display: block;
    }
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  `;
  document.head.appendChild(style);
}
