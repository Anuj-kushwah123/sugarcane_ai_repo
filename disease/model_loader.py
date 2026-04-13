import os
import tensorflow as tf
import numpy as np
import cv2
from django.conf import settings

# Load model only once
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_model', 'sugarcane_model.h5')
print("Model Path:",MODEL_PATH)
model = tf.keras.models.load_model(MODEL_PATH)

class_names = ['Healthy', 'Mosaic', 'RedRot', 'Yellow']
solutions = {
    "Healthy": "Plant healthy. Use proper irrigation and organic manure.",
    "Mosaic": "Use virus-free seed material. Control aphids using Imidacloprid (0.3 ml/L water).",
    "RedRot": "Remove infected plants. Spray Carbendazim (1g/L water).",
    "Yellow": "Apply Nitrogen fertilizer and remove infected leaves",
}

def predict_disease(image_path):

    img = cv2.imread(image_path)

    if img is None:
        return "Invalid Image", 0, "Image not readable"

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (128, 128)) 
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)

    class_index = np.argmax(prediction)
    confidence = float(np.max(prediction) * 100)

    disease = class_names[class_index] 
    solution = solutions.get(disease, "No solution available")
    return disease, round(confidence, 2), solution







    