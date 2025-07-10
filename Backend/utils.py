import cv2
import numpy as np

def preprocess_image(img):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    img = cv2.bitwise_not(img)

    # Threshold to get binary image
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Find contours to crop around actual drawing
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        x, y, w, h = cv2.boundingRect(contours[0])
        img = img[y:y+h, x:x+w]

    # Resize cropped symbol to 20x20
    img = cv2.resize(img, (20, 20))

    # Pad with zeros to make 28x28
    padded = np.pad(img, ((4,4), (4,4)), mode='constant', constant_values=0)

    # Normalize and reshape
    padded = padded / 255.0
    padded = padded.reshape(1, 28, 28, 1)

    return padded
    
