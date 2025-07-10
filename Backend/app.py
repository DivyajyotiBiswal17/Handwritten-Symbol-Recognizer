# backend/app.py
from flask_cors import CORS
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import cv2

import base64
from io import BytesIO
from PIL import Image
from utils import preprocess_image

app = Flask(__name__)
CORS(app)

# Load the trained model
model = load_model("model/symbol_cnn_model.h5")

# Define class labels (update based on your model's output classes)
from string import digits, ascii_uppercase,ascii_lowercase
labels = list(digits + ascii_lowercase + ascii_uppercase)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        image_data = data["image"]

        # Decode base64 image
        image = Image.open(BytesIO(base64.b64decode(image_data.split(",")[1])))
        image = np.array(image)

        # Preprocess image for model
        processed = preprocess_image(image)

        # Predict
        prediction = model.predict(processed)
        predicted_class = labels[np.argmax(prediction)]
        print("Prediction vector:", prediction)
        print("Predicted index:", np.argmax(prediction))
        print("Predicted label:", predicted_class)


        return jsonify({"prediction": predicted_class})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
