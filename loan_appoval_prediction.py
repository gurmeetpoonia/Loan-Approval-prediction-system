import pandas as pd 
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay,accuracy_score
import matplotlib.pyplot as plt
import pickle
df=pd.read_csv("loan.csv")

#print(df.info()) 
#print(df.columns)
#print(df.isnull().sum())
df["Loan_Status"] = df["Loan_Status"].map({"Y": 1, "N": 0})

#print(df.isnull().sum())
df=df.drop("Loan_ID",axis=1)
X=df.drop("Loan_Status",axis=1)

y=df["Loan_Status"]

#Divide into two parts :numeric and Categorical features
numeric_features=[ 'ApplicantIncome','CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History']
Categorical_features=["Gender","Married","Dependents","Education","Self_Employed","Property_Area"]

#fill the missing values  and encoding 
numeric_transformer=Pipeline(steps=[("imputer",SimpleImputer(strategy="median"))])
categorical_transformer=Pipeline(steps=[("imputer",SimpleImputer(strategy="most_frequent")),("encoder",OneHotEncoder(handle_unknown="ignore"))])

#different columns ko ek object me compose karna 
preprocessor=ColumnTransformer(transformers=[("num",numeric_transformer,numeric_features),("cat",categorical_transformer,Categorical_features)])

#model ko define karna and pipeline saare kaam khud karta ha 
model=Pipeline(steps=[("preprocessor",preprocessor),("classifier",RandomForestClassifier(n_estimators=200,random_state=42))])


X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

model.fit(X_train,y_train)

y_proba = model.predict_proba(X_test)[:,1]
y_pred = (y_proba > 0.38).astype(int)

#print(model.score(X_test,y_test))
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Metrics:", classification_report(y_test, y_pred))
cm = confusion_matrix(y_test, y_pred)

print(cm)

scores = cross_val_score(model, X, y, cv=5)
print(scores.mean())


#  ROC-AUC score
auc = roc_auc_score(y_test, y_proba)

print("ROC-AUC Score:", auc)


pickle.dump(model, open("loan_model.pkl", "wb"))

print("Model saved successfully!")
