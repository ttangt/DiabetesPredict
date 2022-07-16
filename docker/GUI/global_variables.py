import pyrebase
import datetime
import json
import os

# Firebase TOKEN
REFRESH_PERIOD = 180 # Refresh authentication every 30 mins

f = open("config.json")
firebaseConfig = json.load(f)

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
auth = firebase.auth()
# storage = firebase.storage()

# Query table

admin_email = "admin@gmail.com" # firebase admin can edit and delete case 

case_basics = ["CaseID", "PatientID", "Name", "Email"]
case_extra = ["CheckingDatetime", "Pregnacies",
                "Glucose", "BloodPressure", "SkinThickness", "Insulin", 
                "BMI", "DiabetesPedigreeFunction", "Age", "DiabetesProbability", "DiabetesClass"]
case_all = case_basics + case_extra

query_row_items = []
ALL_STR = "ALL"

csv_data = []

