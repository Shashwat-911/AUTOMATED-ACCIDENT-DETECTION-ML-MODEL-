import gradio as gr
import requests

API_URL = "https://detect.roboflow.com/car-damage-detection-t0g92-qd7x2/1"
API_KEY = "# YOUR OWN API KEY FROM ROBOFLOW WEBSITE"

def predict_damage(image_path):
    with open(image_path, "rb") as f:
        files = {"file": f}
        params = {"api_key": API_KEY}
        response = requests.post(API_URL, params=params, files=files)
    
    try:
        return response.json()
    except:
        return {"error": "Failed to get prediction"}

iface = gr.Interface(
    fn=predict_damage,
    inputs=gr.Image(type="filepath", label="Upload Car Image"),
    outputs=gr.JSON(label="Prediction"),
    title="Car Damage Detection",
    description="Upload a car image and get damage detection from your Roboflow-trained model."
)

iface.launch(server_name="0.0.0.0",server_port="7860",share=True)
