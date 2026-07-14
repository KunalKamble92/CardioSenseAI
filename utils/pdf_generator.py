SEX_MAP = {
    0: "Female",
    1: "Male"
}

CP_MAP = {
    1: "Typical Angina",
    2: "Atypical Angina",
    3: "Non-anginal Pain",
    4: "Asymptomatic"
}


FBS_MAP = {
    0: "No",
    1: "Yes"
}

RESTECG_MAP = {
    0: "Normal",
    1: "ST-T Abnormality",
    2: "Left Ventricular Hypertrophy"
}

EXANG_MAP = {
    0: "No",
    1: "Yes"
}

SLOPE_MAP = {
    1: "Upsloping",
    2: "Flat",
    3: "Downsloping"
}


THAL_MAP = {
    3: "Normal",
    6: "Fixed Defect",
    7: "Reversible Defect"
}


from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from datetime import datetime


PRIMARY_RED = colors.HexColor("#E63946")
PRIMARY_BLUE = colors.HexColor("#1D3557")
LIGHT_BG = colors.HexColor("#F8FBFF")


styles = getSampleStyleSheet()

title_style = styles["Title"]
title_style.textColor = PRIMARY_RED
title_style.alignment = TA_CENTER

heading_style = styles["Heading2"]
heading_style.textColor = PRIMARY_BLUE

normal_style = styles["BodyText"]


def create_table(title, data):

    table_data = [[title, ""]]

    for key, value in data:
        table_data.append([key, str(value)])

    table = Table(table_data, colWidths=[220, 250])

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),PRIMARY_RED),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,0),13),

        ("BACKGROUND",(0,1),(-1,-1),LIGHT_BG),

        ("GRID",(0,0),(-1,-1),0.5,colors.grey),

        ("BOTTOMPADDING",(0,0),(-1,0),10),

        ("TOPPADDING",(0,1),(-1,-1),8),
        ("BOTTOMPADDING",(0,1),(-1,-1),8),

    ]))

    return table


def generate_pdf(report_data, filename):

    pdf = SimpleDocTemplate(filename)

    story = []

    # -------------------------------------------------

    Paragraph(
        "<b>CardioSense AI</b>",
        title_style
    )

    story.append(
        Paragraph(
            "Heart Disease Assessment Report",
            heading_style
        )
    )

    story.append(
        Paragraph(
            datetime.now().strftime(
                "Generated on %d %B %Y | %I:%M %p"
            ),
            normal_style
        )
    )

    story.append(Spacer(1,20))

    # -------------------------------------------------
    # Patient Information

    form = report_data["patient"]

    patient_table = create_table(

        "Patient Information",

        [

        ("Age", form["age"]),
        ("Sex", SEX_MAP[int(form["sex"])]),
        ("Chest Pain", CP_MAP[int(form["cp"])]),
        ("Blood Pressure", f"{form['trestbps']} mmHg"),
        ("Cholesterol", f"{form['chol']} mg/dL"),
        ("Fasting Blood Sugar", FBS_MAP[int(form["fbs"])]),
        ("Rest ECG", RESTECG_MAP[int(form["restecg"])]),
        ("Maximum Heart Rate", f"{form['thalach']} bpm"),
        ("Exercise Angina", EXANG_MAP[int(form["exang"])]),
        ("Old Peak", form["oldpeak"]),
        ("Slope", SLOPE_MAP[int(form["slope"])]),
        ("Major Vessels", int(form["ca"])),
        ("Thalassemia", THAL_MAP[int(form["thal"])])

        ]

    )

    story.append(patient_table)

    story.append(Spacer(1,20))

    # -------------------------------------------------
    # Prediction

    prediction_table = create_table(

        "AI Assessment",

        [

            ("Prediction", report_data["prediction"]),
            ("Risk Level", report_data["risk"]),
            ("Probability", f'{report_data["probability"]}%')

        ]

    )

    story.append(prediction_table)

    story.append(Spacer(1,20))

    # -------------------------------------------------
    # Model Information

    model_table = create_table(

        "Model Information",

        [

            ("Algorithm","Logistic Regression"),
            ("Accuracy","85.85%"),
            ("ROC-AUC","0.91"),
            ("Feature Scaling","StandardScaler")

        ]

    )

    story.append(model_table)

    story.append(Spacer(1,20))



    story.append(Spacer(1,15))

    summary = (
        "Based on the clinical parameters provided, "
        "CardioSense AI predicts a "
        f"{report_data['risk'].lower()} probability "
        "of heart disease. "
        "This result should be considered an AI-assisted "
        "screening outcome and not a medical diagnosis."
    )

    story.append(
        Paragraph("<b>AI Summary</b>", heading_style)
    )

    story.append(
        Paragraph(summary, normal_style)
    )

    story.append(Spacer(1,20))

    story.append(
        Paragraph("<b>Recommendations</b>", heading_style)
    )

    if report_data["prediction"] == "Heart Disease Detected":

        recommendations = [

            "• Consult a cardiologist.",

            "• Monitor blood pressure regularly.",

            "• Reduce cholesterol intake.",

            "• Exercise under medical supervision.",

            "• Avoid smoking and excessive alcohol."

        ]

    else:

        recommendations = [

            "• Continue regular exercise.",

            "• Maintain healthy weight.",

            "• Eat a balanced diet.",

            "• Schedule routine health checkups.",

            "• Continue healthy lifestyle."

        ]

    for item in recommendations:

        story.append(
            Paragraph(item, normal_style)
        )
    # -------------------------------------------------

    story.append(
        Paragraph(
            "<b>Medical Disclaimer</b>",
            heading_style
        )
    )

    story.append(

        Paragraph(

            "This report is generated using CardioSense AI. "
            "It is intended for educational and screening purposes "
            "only and should not replace professional medical advice.",

            normal_style

        )

    )



    

    story.append(Spacer(1,25))

    story.append(
        Paragraph(
            "<font color='#666666' size='9'>"
            "<b>Generated by CardioSense AI</b><br/>"
            "AI-Powered Heart Disease Prediction System<br/>"
            "Machine Learning Model : Logistic Regression<br/>"
            "This report is computer generated and intended "
            "for educational purposes only.<br/><br/>"
            "© 2026 CardioSense AI. All Rights Reserved."
            "</font>",
            normal_style
        )
    )

    pdf.build(story)

    return filename