import joblib
import numpy as np
import os

# Get project root
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Load scaler and model
scaler = joblib.load(os.path.join(BASE_DIR, "models", "scaler.pkl"))
model = joblib.load(os.path.join(BASE_DIR, "models", "heart_disease_model.pkl"))


def predict_heart_disease(form_data):

    data = np.array([[
        form_data["age"],
        form_data["sex"],
        form_data["cp"],
        form_data["trestbps"],
        form_data["chol"],
        form_data["fbs"],
        form_data["restecg"],
        form_data["thalach"],
        form_data["exang"],
        form_data["oldpeak"],
        form_data["slope"],
        form_data["ca"],
        form_data["thal"]
    ]], dtype=float)

    scaled_data = scaler.transform(data)

    prediction = model.predict(scaled_data)[0]

    probability = model.predict_proba(scaled_data)[0][1]

    return prediction, probability