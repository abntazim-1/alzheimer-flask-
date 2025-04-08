# Alzheimer's Prediction System

A web application for predicting Alzheimer's disease stages from MRI images.

## Project Structure

```
alzheimer-prediction/
├── backend/                 # Flask backend
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── gunicorn_config.py  # Gunicorn configuration
│   ├── render.yaml         # Render deployment config
│   └── static/             # Static files
│       └── processed_images/
└── frontend/               # Frontend files
    ├── index.html          # Main page
    ├── about.html          # About page
    ├── prediction-tool.html # Prediction tool
    ├── success-stories.html # Success stories
    ├── styles.css          # Styles
    ├── package.json        # Frontend dependencies
    └── vercel.json         # Vercel deployment config
```

## Local Development Setup

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```bash
   python app.py
   ```

### Frontend Setup
The frontend consists of static HTML files. You can serve them using any static file server or open them directly in a browser.

## Deployment

### Backend (Render)
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the service:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. Add environment variables if needed
5. Deploy

### Frontend (Vercel)
1. Create a new project on Vercel
2. Connect your GitHub repository
3. Configure the project:
   - Root Directory: `frontend`
   - Framework Preset: Static
4. Deploy

## Environment Variables

### Backend (Render)
- `PYTHON_VERSION`: 3.9.0
- Add any other environment variables as needed

## API Endpoints

- `GET /`: API home route
- `GET /health`: Health check
- `POST /predict`: Image prediction endpoint

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Features

- Upload brain MRI images for analysis
- Capture MRI scans directly using device camera
- AI-powered prediction of Alzheimer's disease stages
- Detailed analysis of brain health metrics
- Visual highlighting of regions of interest
- User-friendly interface with responsive design

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Web browser (Chrome, Firefox, Edge recommended)
- Webcam (optional, for capturing MRI scans)

### Running the Application

#### Windows:

1. Simply double-click the `run_app.bat` file
2. The application will:
   - Set up a Python virtual environment (if needed)
   - Install required dependencies
   - Start the backend API server
   - Open the web application in your default browser

#### Manual Setup:

1. Create a virtual environment:
   ```
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Start the Flask API:
   ```
   python app.py
   ```

5. Open `prediction-tool.html` in your web browser

## Using the Tool

1. Upload a brain MRI scan:
   - Drag and drop an image file into the upload area
   - Click "Browse Files" to select an image from your device
   - Use the camera feature to capture a physical MRI scan

2. Click "Analyze Scan" to process the image

3. View the detailed analysis results, including:
   - Predicted Alzheimer's stage
   - Confidence score
   - Hippocampal volume assessment
   - Ventricular enlargement evaluation
   - Cortical thickness measurement
   - White matter integrity analysis
   - Brain age estimate

## Technology Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- ML Model: TensorFlow, Keras
- Image Processing: PIL (Python Imaging Library)

## Disclaimer

This tool is provided for research and educational purposes only. It is not intended to diagnose or treat any medical condition. Always consult with a healthcare professional for medical advice.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 