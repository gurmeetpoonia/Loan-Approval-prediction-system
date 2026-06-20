from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd


app = FastAPI(
    title="Loan Approval API",
    description="Loan Approval Prediction API",
    version="1.0"
)


model = pickle.load(open("loan_model.pkl", "rb"))


class LoanData(BaseModel):

    Gender: str
    Married: str
    Dependents: str
    Education: str
    Self_Employed: str

    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float

    Loan_Amount_Term: float
    Credit_History: float

    Property_Area: str


@app.get("/")
def home():

    return {
        "message": "Loan API Running"
    }


@app.post("/predict")
def predict(data: LoanData):


    df = pd.DataFrame([data.model_dump()])


    prediction = model.predict(df)

    probability = model.predict_proba(df)


    approval_prob = probability[0][1] * 100
    rejection_prob = probability[0][0] * 100


    return {


        "prediction":
            "Approved" if prediction[0] == 1 else "Rejected",


        "approval_probability":
            round(float(approval_prob), 2),


        "rejection_probability":
            round(float(rejection_prob), 2)

    }