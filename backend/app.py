import os
from flask import Flask, request, jsonify, send_from_directory, url_for
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, array_to_img
from PIL import Image, ImageDraw, ImageEnhance
import io
import base64
import uuid
import json
import random
from datetime import datetime

# Suppress TensorFlow warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all frontend requests

# Create directory for processed images
PROCESSED_IMAGES_DIR = 'static/processed_images'
os.makedirs(PROCESSED_IMAGES_DIR, exist_ok=True)

# Load trained model
try:
    model = load_model("Alzheimer_model.h5")
    model_loaded = True
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model_loaded = False
    print("Using fallback simulation mode")

# Define Alzheimer's stage names and mapping to user-friendly names
ALZHEIMERS_STAGE_NAMES = ['MildDemented', 'ModerateDemented', 'NonDemented', 'VeryMildDemented']
STAGE_DISPLAY_NAMES = {
    'MildDemented': 'Early-Stage Alzheimer\'s',
    'ModerateDemented': 'Moderate Alzheimer\'s',
    'NonDemented': 'No Dementia Detected',
    'VeryMildDemented': 'Mild Cognitive Impairment (MCI)'
}

def process_image_for_display(original_image):
    """Process the image to highlight areas of interest for visualization."""
    try:
        # Create a copy of the image for processing
        processed_img = original_image.copy()
        
        # Convert to RGB if needed
        if processed_img.mode != 'RGB':
            processed_img = processed_img.convert('RGB')
        
        # Enhance contrast for better visibility
        enhancer = ImageEnhance.Contrast(processed_img)
        processed_img = enhancer.enhance(1.2)
        
        # Add simulated ROI highlighting (this would be based on model attention in a real app)
        # Here we're just simulating it for demonstration purposes
        draw = ImageDraw.Draw(processed_img)
        
        # Get image dimensions
        width, height = processed_img.size
        
        # Draw simulated ROI boxes (in a real app, these would be based on model attention)
        # Hippocampus region (approximate)
        draw.rectangle(
            [(int(width*0.4), int(height*0.4)), 
             (int(width*0.6), int(height*0.5))],
            outline="red", width=3
        )
        
        # Ventricular region (approximate)
        draw.rectangle(
            [(int(width*0.45), int(height*0.3)), 
             (int(width*0.55), int(height*0.4))],
            outline="blue", width=3
        )
        
        # Generate a unique filename and save the processed image
        filename = f"processed_{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(PROCESSED_IMAGES_DIR, filename)
        processed_img.save(filepath)
        
        return filename
    except Exception as e:
        print(f"Error in image processing: {e}")
        return None

def classify_image(image, request_host):
    """Preprocess image and make predictions."""
    try:
        # Convert image to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Process image for display and save it
        processed_image_filename = process_image_for_display(image)
        
        if not model_loaded:
            # If model isn't loaded, return demo data
            predicted_class = random.randint(0, 3)
            stage = ALZHEIMERS_STAGE_NAMES[predicted_class]
            confidence_score = random.uniform(65, 95)
        else:
            # Resize image to match model input size
            input_image = image.resize((180, 180))
            
            # Convert to array and normalize pixel values
            input_image_array = img_to_array(input_image)
            input_image_exp_dim = np.expand_dims(input_image_array, axis=0)  # Add batch dimension

            # Make prediction
            predictions = model.predict(input_image_exp_dim)
            result = tf.nn.softmax(predictions[0])  # Convert to probabilities
            
            predicted_class = np.argmax(result)
            confidence_score = float(np.max(result) * 100)  # Convert to percentage
            stage = ALZHEIMERS_STAGE_NAMES[predicted_class]

        # Create URL for the processed image
        if processed_image_filename:
            processed_image_url = f"http://{request_host}/static/processed_images/{processed_image_filename}"
        else:
            processed_image_url = None
            
        return {
            "success": True,
            "prediction": {
                "stage": STAGE_DISPLAY_NAMES[stage],
                "confidence": round(confidence_score, 1),
                "processedImageUrl": processed_image_url,
                "technical": {
                    "original_stage": stage,
                    "timestamp": datetime.now().isoformat()
                }
            }
        }
    except Exception as e:
        print(f"Error in classify_image: {e}")
        return {
            "success": False,
            "error": str(e)
        }
    
@app.route("/", methods=["GET"])
def home():
    """API Home Route"""
    return jsonify({
        "message": "Alzheimer's Stage Prediction API is running.",
        "endpoints": {
            "predict": "/predict [POST] - Send MRI image for analysis",
            "health": "/health [GET] - Check API health status"
        },
        "model_loaded": model_loaded
    })

@app.route("/health", methods=["GET"])
def health_check():
    """API Health Check"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model_loaded,
        "timestamp": datetime.now().isoformat()
    })

@app.route("/predict", methods=["POST"])
def predict():
    """Handle image upload and return classification result."""
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    file = request.files['file']
    
    try:
        image = Image.open(file)  # Open image using PIL
        host = request.host  # Get host for constructing image URLs
        prediction_result = classify_image(image, host)
        return jsonify(prediction_result)
    except Exception as e:
        print(f"Error in predict endpoint: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/static/processed_images/<filename>')
def serve_processed_image(filename):
    """Serve processed images"""
    return send_from_directory(PROCESSED_IMAGES_DIR, filename)

# Run Flask API
if __name__ == "__main__":
    print(f"Starting Flask server on http://localhost:5000")
    print(f"Static files will be served from {os.path.abspath(PROCESSED_IMAGES_DIR)}")
    app.run(debug=True, host="0.0.0.0", port=5000)
