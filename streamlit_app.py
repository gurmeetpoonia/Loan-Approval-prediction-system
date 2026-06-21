import streamlit as st
import time
import requests
import matplotlib.pyplot as plt

import pandas as pd

import matplotlib.pyplot as plt
from datetime import datetime

if "history" not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="Loan Approval Predictor", page_icon="🏦",layout="wide")
API_URL = "https://loan-approval-prediction-system-mnx6.onrender.com"

if "api_checked" not in st.session_state:
    st.session_state.api_checked = False

if "api_status" not in st.session_state:
    st.session_state.api_status = False



tab1, tab2, tab3 = st.tabs([
    "🏦 Predictor",
    "📜 History",
    "ℹ️ About"
])
with tab1:
    with st.container(border=True):

        st.header("Applicant Details")


        col1, col2 = st.columns(2)

        with col1:
            Gender = st.selectbox(
        "Gender",
        ["Select", "Male", "Female"],
        key="gender"
    )

            Dependents = st.selectbox(
        "Dependents",
        ["Select", "0", "1", "2", "3+"],
        key="dependents"
    )

            Self_Employed = st.selectbox(
        "Self Employed",
        ["Select", "No", "Yes"],
        key="self_employed"
    )

            Credit_History = st.selectbox(
        "Credit History",
        ["Select", "Good", "Bad"],
        key="credit_history"
    )


        with col2:
            Married = st.selectbox(
        "Married",
        ["Select", "Yes", "No"],
        key="married"
    )

            Education = st.selectbox(
        "Education",
        ["Select", "Graduate", "Not Graduate"],
        key="education"
    )

            Property_Area = st.selectbox(
        "Property Area",
        ["Select", "Urban", "Semiurban", "Rural"],
        key="property_area"
    )

            Loan_Amount_Term = st.selectbox(
        "Loan Term",
        ["Select", 12, 36, 60, 84, 120, 180, 240, 300, 360],
        key="loan_term"
    )


        ApplicantIncome = st.number_input(
    "Applicant Income",
    min_value=1,
    value=120, key="app_income"
)

        CoapplicantIncome = st.number_input("Coapplicant Income",min_value=0,
    value=0,  key="coapp_income" )

        LoanAmount = st.number_input(
    "Loan Amount",
    min_value=0,
    value=5000,key="loan_amount"
)

        credit_value = None


        if Credit_History=="Good":
            credit_value=1.0

        elif Credit_History=="Bad":
            credit_value=0.0

        col1,col2=st.columns(2)

        left, center, right = st.columns([1,2,1])

        with center:
            predict = st.button(
        "Predict Loan Status",
        use_container_width=True,
        type="primary"
    )
        
        input_df = pd.DataFrame({

            'Gender': [Gender],

            'Married': [Married],

            'Dependents': [Dependents],

            'Education': [Education],

            'Self_Employed': [Self_Employed],

            'ApplicantIncome': [ApplicantIncome],

            'CoapplicantIncome': [CoapplicantIncome],

            'LoanAmount': [LoanAmount],

            'Loan_Amount_Term': [Loan_Amount_Term],

            'Credit_History': [credit_value],
            'Property_Area': [Property_Area]

})
        if  predict:
     #condition of select    
            if ("Select" in [Gender, Married, Education , Dependents,Self_Employed,Loan_Amount_Term,Credit_History,Property_Area]):

                st.toast("⚠️ Please fill all required fields.")
                st.stop()
            elif ApplicantIncome<= 0:
                st.toast("⚠️ Applicant Income must be greater than 0.")
                st.stop()
            elif CoapplicantIncome < 0:
                st.toast("⚠️ Coapplicant Income cannot be negative.")
                st.stop()

            elif LoanAmount <= 0:
                st.toast(" Enter valid amount")
                st.stop()  
         
    

            #predication 
            try:
                response = requests.post(
        f"{API_URL}/predict",json=input_df.iloc[0].to_dict(),timeout=30)

                result = response.json()

                prediction = result["prediction"]

                approval_prob = result["approval_probability"]

                rejection_prob = result["rejection_probability"]

                record = input_df.copy()

                record["Prediction"] = prediction
                record["Approval_Probability"] = approval_prob
                record["Rejection_Probability"] = rejection_prob
                record["Time"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                st.session_state.history.append(record)
            except Exception:
                st.error("⚠️ API is not running.")
                st.stop()

            st.subheader("Prediction")


            if prediction == "Approved":

                st.markdown("""
<div style="
width:260px;
background:#0b3d20;
padding:18px;
border-radius:12px;
text-align:center;
box-shadow:0 2px 10px rgba(0,0,0,0.2);
margin-bottom:15px;
">

<h3 style="
color:#4ade80;
margin:0;
font-size:28px;
font-weight:700;
">
✅ Loan Approved
</h3>

</div>
""", unsafe_allow_html=True)
            else:

                st.markdown("""
<div style="
width:260px;
background:#4a1515;
padding:18px;
border-radius:12px;
text-align:center;
box-shadow:0 2px 10px rgba(0,0,0,0.2);
margin-bottom:15px;
">

<h3 style="
color:#ff6b6b;
margin:0;
font-size:28px;
font-weight:700;
">
❌ Loan Rejected
</h3>

</div>
""", unsafe_allow_html=True)
       

    

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"Approval • {approval_prob:.2f}%")
                st.progress(approval_prob/100)

            with col2:
                st.write(f"Rejection • {rejection_prob:.2f}%")
                st.progress(rejection_prob/100)

            st.subheader("Applicant Details")


            st.dataframe(input_df)


        st.markdown("---")

        st.caption("Built by Gurmeet Punia 🚀")    

with tab2:

    st.subheader("Prediction History")

    if st.session_state.history:


        history = pd.concat(
                st.session_state.history,
                ignore_index=True
            )
        last = history.iloc[-1]

        
        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Latest Prediction",
                last["Prediction"]
            )

        with c2:
            st.metric(
                "Approval %",
                f"{last['Approval_Probability']:.2f}%"
            )

        with c3:
            st.metric(
                "Rejection %",
                f"{last['Rejection_Probability']:.2f}%"
            )

        st.markdown("---")

        st.dataframe(history,width="stretch")


        st.download_button("📥 Download History",

                history.to_csv(index=False),file_name="prediction_history.csv",

                mime="text/csv")


        if st.button("🗑 Clear History"):

            st.session_state.history=[]

            st.rerun()



    else:

        st.info("No predictions available.")  



with tab3:
    st.subheader("About Project")
    st.markdown(
"""

This application predicts loan approval using Machine Learning.




### Tech Stack




✅ Scikit Learn



✅ Gradient Boosting



✅ Pipeline



✅ FastAPI



✅ Pydantic



✅ Streamlit



✅ Requests



✅ Prediction Logging





### Features




• Real Time Prediction



• Approval Probability



• Prediction History



• API Integration




• Downloadable Logs





Built by



### Gurmeet Punia 🚀




"""

)        