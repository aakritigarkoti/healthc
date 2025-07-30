# 🩺 Healthcare Chatbot – NLP-Based Symptom Checker

A simple NLP-based healthcare chatbot that allows users to describe their symptoms in natural language and receive basic suggestions, including possible diseases and precautions.

This project helped me explore the basics of **Natural Language Processing (NLP)** — like text tokenization, keyword extraction, and symptom matching — using Python and Flask.

---

## 🚀 Features

- Users can enter symptoms in plain text (e.g., "I have headache and fever").
- Text is processed using **NLTK** (stopword removal, keyword extraction).
- Flask API processes input and matches symptoms to possible diseases.
- Responds with disease name, description, and precautionary advice.
- Supports multiple symptoms and basic error handling.

---

## ⚙️ Technologies Used

- **Python**
- **Flask** – backend API for chatbot
- **NLTK** – for text processing and keyword matching
- **Scikit-learn** – model training and predictions
- **Pandas** – dataset handling


---

## 🧠 NLP Techniques Applied

- Text preprocessing: stopword removal, lowercasing
- Tokenization and keyword matching
- Symptom mapping and disease prediction

---

## 📁 File Overview

📦 HealthcareBot/
┣ 📄 healthcare_bot_gui.py ← GUI application (Tkinter-based)
┣ 📄 train.py ← Model training script
┣ 📄 predict.py ← Prediction + text processing logic
┣ 📄 label_encoder.pkl ← Label encoder for diseases
┣ 📄 trained_model.pkl ← Trained ML model (RandomForest/DecisionTree)
┣ 📄 dataset.csv ← Combined training dataset
┣ 📄 Training.csv / Testing.csv ← Raw CSVs
┣ 📄 Symptom_severity.csv ← Numerical severity of each symptom
┣ 📄 symptom_Description.csv ← Descriptions of predicted diseases
┣ 📄 symptom_precaution.csv ← Precautions per disease
┗ 📄 health.png ← Logo used in the GUI

yaml
Copy
Edit

---

## 🛠️ How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/healthcare-chatbot.git
   cd healthcare-chatbot
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the chatbot GUI:

bash
Copy
Edit
python healthcare_bot_gui.py
Or run the Flask backend:

bash
Copy
Edit
python predict.py
🙋‍♀️ Developed By
Aakriti Garkoti

This project was built to learn the foundations of NLP and apply them to a real-world use case in healthcare.

