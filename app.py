from flask import Flask, render_template, request, session
from utils.predictor import predict_heart_disease
from flask import send_file
import tempfile
from utils.pdf_generator import generate_pdf

app = Flask(__name__)
app.secret_key = "CardioSenseAI2026"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/prediction")
def prediction():
    return render_template("prediction.html")

@app.route("/predict", methods=["POST"])
def predict():

    form_data = {

        "age": float(request.form["age"]),
        "sex": float(request.form["sex"]),
        "cp": float(request.form["cp"]),
        "trestbps": float(request.form["trestbps"]),
        "chol": float(request.form["chol"]),
        "fbs": float(request.form["fbs"]),
        "restecg": float(request.form["restecg"]),
        "thalach": float(request.form["thalach"]),
        "exang": float(request.form["exang"]),
        "oldpeak": float(request.form["oldpeak"]),
        "slope": float(request.form["slope"]),
        "ca": float(request.form["ca"]),
        "thal": float(request.form["thal"])

    }

    prediction, probability = predict_heart_disease(form_data)

    # Convert probability to percentage
    probability = round(probability * 100, 2)

    # Store data in session
    session["prediction"] = int(prediction)
    session["probability"] = probability
    session["form_data"] = form_data

    return render_template(
        "result.html",
        prediction=prediction,
        probability=probability
    )

@app.route("/download-report")
def download_report():

    form = session["form_data"]

    report_data = {

        "patient": form,

        "prediction":
            "Heart Disease Detected"
            if session["prediction"]
            else
            "No Heart Disease Detected",

        "probability": session["probability"],

        "risk":
            "High"
            if session["probability"] >= 80
            else
            "Moderate"
            if session["probability"] >= 40
            else
            "Low"
    }

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    generate_pdf(report_data, temp_file.name)
    return send_file(
        temp_file.name,
        as_attachment=True,
        download_name="CardioSenseAI_Report.pdf"
    )



if __name__ == "__main__":
    app.run(debug=True)