import requests
import gradio as gr
import pillow_heif

# ------------------------
# IBM Watson Fraud Detection Setup
# ------------------------
IBM_API_KEY = "kNy51yh8PCw3DouJHTua7l4Kx1RT7u4PSFMgt-GoPOzh"
IBM_DEPLOYMENT_URL = "https://au-syd.ml.cloud.ibm.com/ml/v4/deployments/technos/predictions?version=2021-05-01"

def get_token():
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"apikey": IBM_API_KEY, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"}
    resp = requests.post(url, headers=headers, data=data)
    return resp.json()["access_token"]

def call_ibm_model(*args):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    fields = [
        "age", "authorities_contacted", "auto_make", "auto_model", "auto_year",
        "bodily_injuries", "capital-gains", "capital-loss", "collision_type",
        "incident_city", "incident_date", "incident_hour_of_the_day", "incident_location",
        "incident_severity", "incident_state", "incident_type", "injury_claim",
        "insured_education_level", "insured_hobbies", "insured_occupation",
        "insured_relationship", "insured_sex", "insured_zip", "months_as_customer",
        "number_of_vehicles_involved", "police_report_available", "policy_annual_premium",
        "policy_bind_date", "policy_csl", "policy_deductable", "policy_number",
        "policy_state", "property_claim", "property_damage", "total_claim_amount",
        "umbrella_limit", "vehicle_claim", "witnesses"
    ]
    values = [list(args)]

    payload = {"input_data": [{"fields": fields, "values": values}]}
    resp = requests.post(IBM_DEPLOYMENT_URL, headers=headers, json=payload).json()

    try:
        prediction = resp["predictions"][0]["values"][0][0]
        prob = resp["predictions"][0]["values"][0][1]
        return f"""
        ### 🛡️ Fraud Prediction Result  
        **Prediction:** {prediction}  
        **Confidence:** Legit: {round(prob[0]*100,2)}% | Fraud: {round(prob[1]*100,2)}%
        """
    except:
        return "⚠️ Error while fetching prediction"


# ------------------------
# Car Damage Detection Setup
# ------------------------
pillow_heif.register_heif_opener()
API_URL = "https://detect.roboflow.com/car-damage-detection-t0g92-qd7x2/1"
API_KEY = "s1sereFwcK66zA6funIr"

def predict_damage(image_path):
    with open(image_path, "rb") as f:
        files = {"file": f}
        params = {"api_key": API_KEY}
        response = requests.post(API_URL, params=params, files=files).json()

    try:
        preds = response["predictions"]
        if not preds:
            return "✅ No major damage detected."
        result = "### 🚗 Car Damage Detection\n"
        for i, p in enumerate(preds, 1):
            result += f"**Damage {i}:** {p['class']} (Confidence: {round(p['confidence']*100,2)}%)\n"
        return result
    except:
        return "⚠️ Error in damage detection"


# ------------------------
# Gradio UI
# ------------------------
fraud_inputs = [
    gr.Number(label="Age"),
    gr.Textbox(label="Authorities Contacted"),
    gr.Textbox(label="Auto Make"),
    gr.Textbox(label="Auto Model"),
    gr.Number(label="Auto Year"),
    gr.Number(label="Bodily Injuries"),
    gr.Number(label="Capital Gains"),
    gr.Number(label="Capital Loss"),
    gr.Textbox(label="Collision Type"),
    gr.Textbox(label="Incident City"),
    gr.Textbox(label="Incident Date"),
    gr.Number(label="Incident Hour of the Day"),
    gr.Textbox(label="Incident Location"),
    gr.Textbox(label="Incident Severity"),
    gr.Textbox(label="Incident State"),
    gr.Textbox(label="Incident Type"),
    gr.Number(label="Injury Claim"),
    gr.Textbox(label="Insured Education Level"),
    gr.Textbox(label="Insured Hobbies"),
    gr.Textbox(label="Insured Occupation"),
    gr.Textbox(label="Insured Relationship"),
    gr.Textbox(label="Insured Sex"),
    gr.Number(label="Insured Zip"),
    gr.Number(label="Months as Customer"),
    gr.Number(label="Number of Vehicles Involved"),
    gr.Textbox(label="Police Report Available"),
    gr.Number(label="Policy Annual Premium"),
    gr.Textbox(label="Policy Bind Date"),
    gr.Textbox(label="Policy CSL"),
    gr.Number(label="Policy Deductible"),
    gr.Number(label="Policy Number"),
    gr.Textbox(label="Policy State"),
    gr.Number(label="Property Claim"),
    gr.Textbox(label="Property Damage"),
    gr.Number(label="Total Claim Amount"),
    gr.Number(label="Umbrella Limit"),
    gr.Number(label="Vehicle Claim"),
    gr.Number(label="Witnesses"),
]

fraud_tab = gr.Interface(
    fn=call_ibm_model,
    inputs=fraud_inputs,
    outputs=gr.Markdown(),
    title="🛡️ Insurance Fraud Detection",
    description="Fill in claim details below to check if the claim might be fraudulent."
)

damage_tab = gr.Interface(
    fn=predict_damage,
    inputs=gr.Image(type="filepath", label="Upload Car Image"),
    outputs=gr.Markdown(),
    title="🚗 Car Damage Detection",
    description="Upload a car image to detect possible damages."
)

demo = gr.TabbedInterface([fraud_tab, damage_tab], ["Fraud Detection", "Damage Detection"])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
