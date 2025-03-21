import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image

# Suppress TensorFlow warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all frontend requests

# Load trained model
MODEL_PATH = r"F:\Webapp\Alzheimer_model.h5"
model = load_model(MODEL_PATH)

# Define Alzheimer's stage names
ALZHEIMERS_STAGE_NAMES = ['MildDemented', 'ModerateDemented', 'NonDemented', 'VeryMildDemented']

def classify_image(image):
    """Preprocess image and make predictions."""
    try:
        # Convert image to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Resize image to match model input size
        input_image = image.resize((180, 180))
        
        # Convert to array and normalize pixel values
        input_image_array = img_to_array(input_image)
        input_image_exp_dim = np.expand_dims(input_image_array, axis=0)  # Add batch dimension

        # Make prediction
        predictions = model.predict(input_image_exp_dim)
        result = tf.nn.softmax(predictions[0])  # Convert to probabilities
        
        predicted_class = np.argmax(result)
        confidence_score = np.max(result) * 100  # Convert to percentage

        return {
            "stage": ALZHEIMERS_STAGE_NAMES[predicted_class],  # Stage first
            "confidence": f"{confidence_score:.2f}%"          # Confidence second
        }
    except Exception as e:
        return {"error": str(e)}
    
@app.route("/", methods=["GET"])
def home():
    """API Home Route"""
    return jsonify({"message": "Alzheimer's Stage Prediction API is running."})

@app.route("/predict", methods=["POST"])
def predict():
    """Handle image upload and return classification result."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    
    try:
        image = Image.open(file)  # Open image using PIL
        prediction_result = classify_image(image)
        return jsonify(prediction_result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask API
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
