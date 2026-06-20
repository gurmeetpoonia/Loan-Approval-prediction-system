# 🏦 Loan Approval Prediction System

A full-stack Machine Learning project that predicts loan approval using a trained ML model, FastAPI backend, and Streamlit frontend.

---
## 🚀 Live App
👉 https://loan-approval-prediction-system-ap.streamlit.app/ 

## 🚀 Project Overview

This project predicts whether a loan application will be **Approved or Rejected** based on applicant details like income, credit history, education, and property area.

It includes:
- 🧠 Machine Learning Model (Gradient Boosting)
- ⚡ FastAPI Backend (REST API)
- 🎨 Streamlit Frontend (Interactive UI)
- 📊 Real-time Prediction Visualization

---

## 🧰 Tech Stack

- Python
- Pandas, NumPy
- Scikit-learn
- FastAPI
- Streamlit
- Matplotlib
- Requests

---

## 📁 Project Structure
- Loan-Approval-Project/

│── model_training.py

│── api.py

│── app.py (Streamlit)

│── loan_model.pkl

│── loan.csv

│── requirements.txt

│── README.md

---

## ⚙️ How to Run Locally

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

## 2️⃣ Run FastAPI backend
- uvicorn api:app --reload

## API runs at:

 http://127.0.0.1:8000
## 3️⃣ Run Streamlit app

  streamlit run app.py
## 📊 Features
- Real-time loan prediction
- Approval & rejection probability
- Input validation
- Prediction history
- Interactive dashboard
## 🧠 Model Info
- Algorithm: Gradient Boosting Classifier
- Preprocessing: Pipeline + ColumnTransformer
- Encoding: OneHotEncoder
- Imputation: Median & Most Frequent

#$  📸 UI Preview


<img width="1917" height="1077" alt="loan_approval1" src="https://github.com/user-attachments/assets/cc27d52a-0d81-41ab-86ee-4e58b497d884" />


## 👨‍💻 Author

Gurmeet Punia
