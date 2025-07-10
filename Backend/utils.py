import cv2
import numpy as np

def preprocess_image(img):
    # Convert to grayscale if not already
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    # Resize to 28x28 (or whatever input size your model expects)
    img = cv2.resize(img, (28, 28))

    # Normalize
    img = img / 255.0

    # Reshape to (1, 28, 28, 1) if model expects channel last
    img = img.reshape(1, 28, 28, 1)

    return img
