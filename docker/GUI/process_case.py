case_header_names = ["CheckingDatetime", "Pregnacies",
                "Glucose", "BloodPressure", "SkinThickness", "Insulin", 
                "BMI", "DiabetesPedigreeFunction", "Age", "DiabetesProbability", "DiabetesClass"]

class CaseInfo:
    def __init__(self, checkingdatetime , pregnacies, glucose, bloodpressure, skinthickness, insulin,\
        bmi, diabetespedigreefunction, age, diabetesprobability, diabetesclass):
        self.checkingdatetime = checkingdatetime
        self.pregnacies = pregnacies
        self.glucose = glucose
        self.bloodpressure = bloodpressure
        self.skinthickness = skinthickness
        self.insulin = insulin
        self.bmi = bmi
        self.diabetespedigreefunction = diabetespedigreefunction
        self.age = age
        self.diabetesprobability = diabetesprobability
        self.diabetesclass = diabetesclass

    def check_empty_key(self):
        case_array = [self.checkingdatetime, self.pregnacies, self.glucose, self.bloodpressure, \
            self.skinthickness, self.insulin, self.bmi, self.diabetespedigreefunction, self.age]

        for item in case_array:
            if len(item) == 0:
                return True

        return False

    def return_data_dict(self):
        data_dict = {}

        case_array = [self.checkingdatetime, self.pregnacies, self.glucose, self.bloodpressure, \
            self.skinthickness, self.insulin, self.bmi, self.diabetespedigreefunction, self.age, \
            self.diabetesprobability, self.diabetesclass]

        for i  in range(len(case_array)):
            data_dict[case_header_names[i]] = case_array[i]
        
        return data_dict

    