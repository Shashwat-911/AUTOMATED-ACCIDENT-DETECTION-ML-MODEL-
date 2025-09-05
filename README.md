# fraud-damage-detection
A Gradio-based web app combining insurance fraud detection using IBM Watson ML API and car damage detection using Roboflow computer vision API.

# 🛡️ Fraud & Car Damage Detection

A **Gradio-based web application** that integrates:

- **Insurance Fraud Detection** powered by **IBM Watson ML API**  
- **Car Damage Detection** powered by **Roboflow Computer Vision API**  

This project demonstrates how AI/ML models can be combined into a single interface for real-world insurance claim verification.

---

## 🚀 Features
- Predict if an insurance claim is **Legit** or **Fraud** with confidence scores.  
- Upload a car image and detect **damaged parts** with bounding boxes & confidence levels.  
- Simple **Gradio UI** with **two interactive tabs**:
  - Fraud Detection
  - Damage Detection

---

## 🛠️ Tech Stack
- **Python 3.9+**
- **Gradio** (for UI)
- **Requests** (for API calls)
- **IBM Watson Machine Learning**
- **Roboflow API**
- **pillow-heif** (for HEIF/HEIC image support)

---

## 📂 Project Structure
fraud-damage-detection/
│
├── app.py # Main Gradio application
├── requirements.txt # Python dependencies
├── README.md # Project documentation


---

## ⚙️ Installation & Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/fraud-damage-detection.git
   cd fraud-damage-detection


Create a virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows


Install dependencies

pip install -r requirements.txt


Add your API keys

Create a .env file in the root folder:

IBM_API_KEY=your-ibm-api-key
ROBOFLOW_API_KEY=your-roboflow-api-key


The app automatically loads keys from .env.

Run the app

python app.py


The app will be live at:
👉 http://127.0.0.1:7860

✨ Acknowledgements

IBM Watson Machine Learning

Roboflow

Gradio
