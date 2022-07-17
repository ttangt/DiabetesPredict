import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import os
import pyrebase
import datetime

from global_variables import *
from process_case import *
from predict import load_model_predict
from admin_table import *
from user_table import *
from output_csv import *

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

# Login Page
class LoginPage(QDialog):
    def __init__(self):
        super(LoginPage, self).__init__()
        loadUi("login.ui", self)

        self.signup_btn.clicked.connect(self.goto_signup_page)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_btn.clicked.connect(self.process_login)

    def goto_signup_page(self):
        signup_page = SignupPage()
        widget.addWidget(signup_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def process_login(self):
        email = self.emailfield.text()
        password = self.passwordfield.text()
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            self.goto_query_page(user)
        except Exception as e:
            self.error.setText("Invalid email or password")

    def goto_query_page(self, user):
        global start_time # Time start at every login or refresh authenication token
        start_time = datetime.datetime.now()
        query_page = QueryPage(user)
        widget.addWidget(query_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# SignupPage(Qidalog)
class SignupPage(QDialog):
    def __init__(self):
        super(SignupPage, self).__init__()
        loadUi("signup.ui", self)
        
        self.login_btn.clicked.connect(self.goto_login_page)
        self.signup_btn.clicked.connect(self.process_signup)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)

    def process_signup(self):
        email = self.emailfield.text()
        name = self.namefield.text()
        if self.passwordfield.text() == self.confirmpasswordfield.text():
            password = self.passwordfield.text()
            try:
                user = auth.create_user_with_email_and_password(email, password)
                self.initialize_database(user, name, email)
                self.goto_login_page()
                QMessageBox.information(self, "Congrulation", "Account is created successfully!")
            except Exception as e:
                self.error.setText("Invalid name or email")
        else:
            self.error.setText("Passwords do not match")

    def initialize_database(self, user, name, email):
        data = {"Name": name, "Email": email, "Cases": ""}
        db.child("users").child(user["localId"]).set(data, user["idToken"])

    def goto_login_page(self):
        login_page = LoginPage()
        widget.addWidget(login_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class QueryPage(QDialog):
    def __init__(self, login_user, mytimer = None):
        super(QueryPage, self).__init__()
        loadUi("query.ui", self)
        self.login_user = login_user

        # Set up logging in timer in Query Page
        if mytimer != None:
            self.mytimer = mytimer
        else:
            self.mytimer = QTimer(self)
            self.mytimer.timeout.connect(self.precess_token) # action for every counting
            self.mytimer.start(1000) # count every second

        self.logout_btn.clicked.connect(self.goto_login_page) 
        self.add_btn.clicked.connect(self.goto_add_page)
        
        
        self.edit_btn.clicked.connect(self.goto_edit_page)
        self.delete_2_btn.clicked.connect(self.goto_delete_page)

        self.query_table.cellClicked.connect(self.cell_clicked)
        if db.child("users").child(self.login_user["localId"]).child("Email").get(self.login_user["idToken"]).val() != admin_email:
            self.edit_btn.hide()
            self.delete_2_btn.hide()
            self.comboBox.hide()
        else:
            self.input_combo_box()
            self.comboBox.currentTextChanged.connect(self.initialize_table)
        self.initialize_table()
        self.save_btn.clicked.connect(self.save_table)

    def precess_token(self):
        now_time = datetime.datetime(
            int(QDateTime.currentDateTime().toString("yyyy")),
            int(QDateTime.currentDateTime().toString("MM")),
            int(QDateTime.currentDateTime().toString("dd")),
            int(QDateTime.currentDateTime().toString("hh")),
            int(QDateTime.currentDateTime().toString("mm")),
            int(QDateTime.currentDateTime().toString("ss")))
 
        login_sec = (now_time - start_time).total_seconds() # Loginned time within refresh period
        self.refresh_token(self.login_user, login_sec)

    # Refresh firebase token every 30 mins
    def refresh_token(self, user, login_sec):
        # print("Logined in count: ", login_sec)    
        if login_sec > REFRESH_PERIOD: 
            auth.refresh(user["refreshToken"])
            # print("FRESHED")
            global start_time 
            start_time = datetime.datetime.now()

    def goto_login_page(self):
        mbox = QMessageBox.question(self, "Warning!!!", "Sure to Logout?", QMessageBox.Yes | QMessageBox.No)
        if mbox == QMessageBox.Yes:
            self.mytimer.stop()
            login_page = LoginPage()
            widget.addWidget(login_page)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_add_page(self, mytimer):
        case_page = CasePage(self.login_user, self.mytimer, "add")
        widget.addWidget(case_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def cell_clicked(self, row, column):
        global query_row_items
        query_row_items = []
        for j in range(len(case_all)):
            query_row_items.append(self.query_table.item(row, j).text())

    def input_combo_box(self):
        self.comboBox.addItem(ALL_STR)
        for user_dict in db.child("users").get(self.login_user["idToken"]).each():
            if user_dict.val()["Email"] != admin_email:
                self.comboBox.addItem(user_dict.val()["Email"])

    def initialize_table(self, query_person_email = None):
        global csv_data
        # not admin
        if db.child("users").child(self.login_user["localId"]).child("Email").get(self.login_user["idToken"]).val() != admin_email:
            data = db.child("users").child(self.login_user["localId"]).get(self.login_user["idToken"])
            user_id = self.login_user["localId"]
            self.query_table, csv_data = insert_data_to_table(self.query_table, user_id, data, case_extra, case_all)
        else: # admin user
            total_rows = return_table_row_number(db.child("users").get(self.login_user["idToken"]).each(), admin_email, query_person_email, ALL_STR)
            setup_tableframe(self.query_table, total_rows, len(case_all), case_all)
            self.query_table, csv_data = insert_data_to_admin_table(self.query_table,\
                db.child("users").get(self.login_user["idToken"]).each(), admin_email, query_person_email, case_extra, case_all, ALL_STR)

        self.query_table = hide_table_headers(self.query_table)

    def save_table(self):
        if len(csv_data) > 0:
            write_csv(csv_data, case_all)
            QMessageBox.information(self, "Congrulation", "Data is exported successfully!")
        else:
            QMessageBox.information(self, "Alert", "No record!")

    def goto_edit_page(self, mytimer):
        if len(query_row_items) > 0:
            case_page = CasePage(self.login_user, self.mytimer, "edit")
            widget.addWidget(case_page)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            mbox = QMessageBox.information(self, "Warning!!!", "No case is selected!")

    def goto_delete_page(self, mytimer):
        delete_page = DeletePage(self.login_user, self.mytimer)
        widget.addWidget(delete_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# Every Case Page
class CasePage(QDialog):
    def __init__(self, login_user, mytimer, action=None):
        super(CasePage, self).__init__()
        loadUi("case.ui", self)
        
        self.login_user = login_user
        self.timer = mytimer
        self.back.clicked.connect(self.goto_query_page)

        self.caseID.setReadOnly(True)
        self.patientID.setReadOnly(True)
        self.name.setReadOnly(True)
        self.email.setReadOnly(True)
        self.dprob.setReadOnly(True)
        self.dclass.setReadOnly(True)

        self.action = action
        self.display_case_items()

        self.submit.clicked.connect(self.submit_data)

    def goto_query_page(self):
        query_page = QueryPage(self.login_user, self.timer)
        widget.addWidget(query_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def display_case_items(self):
        if self.action == "add": # add case 
            self.datetime.setText(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            self.datetime.setReadOnly(True)
            self.caseID.setText("###")
            # Only admin can see patientID, name, email
            if db.child("users").child(self.login_user["localId"]).child("Email").get(self.login_user["idToken"]).val() != admin_email:
                self.comboBox.hide()
                self.patientID.setText(self.login_user["localId"])
                self.name.setText(db.child("users").child(self.login_user["localId"]).child("Name").get(self.login_user["idToken"]).val())
                self.email.setText(self.login_user["email"])
            else:
                self.input_combo_box()
                self.comboBox.currentTextChanged.connect(self.combo_box_changed)
        else: # edit case
            self.comboBox.hide()
            self.caseID.setText(query_row_items[0])
            self.patientID.setText(query_row_items[1])
            self.name.setText(query_row_items[2])
            self.email.setText(query_row_items[3])

            self.datetime.setText(query_row_items[4])
            self.pregnacies.setText(query_row_items[5])
            self.glucose.setText(query_row_items[6])
            self.bloodpressure.setText(query_row_items[7])
            self.skinthickness.setText(query_row_items[8])
            self.insulin.setText(query_row_items[9])
            self.bmi.setText(query_row_items[10])
            self.dpf.setText(query_row_items[11])
            self.age.setText(query_row_items[12])
            self.dprob.setText(query_row_items[13])
            self.dclass.setText(query_row_items[14])

    def input_combo_box(self):
        self.comboBox.addItem("---Choose---")
        for user_obj in db.child("users").get(self.login_user["idToken"]).each():
            if user_obj.val()["Email"] != admin_email:
                user_id = user_obj.key()
                user_name = user_obj.val()["Name"]
                user_email = user_obj.val()["Email"]
                self.comboBox.addItem(user_email)

    # Display user info for selected combo box
    def combo_box_changed(self, value):
        for user_obj in db.child("users").get(self.login_user["idToken"]).each():
            if value != "---Choose---" and user_obj.val()["Email"] != admin_email:
                user_email = user_obj.val()["Email"] # pyrebase obj -> dict
                if value == user_email:
                    user_id = user_obj.key()
                    user_name = user_obj.val()["Name"]
                    self.patientID.setText(user_id)
                    self.name.setText(user_name)
                    self.email.setText(user_email)

    def submit_data(self):
        case_id = self.caseID.text()
        checkingdatetime = self.datetime.text()

        if db.child("users").child(self.login_user["localId"]).child("Email").get(self.login_user["idToken"]).val() != admin_email:
            user_id = self.login_user["localId"]
        else:
            user_id = self.patientID.text()

        name = self.name.text()
        email = self.email.text()
        pregnacies = self.pregnacies.text()
        glucose = self.glucose.text()
        bloodpressure = self.bloodpressure.text()
        skinthickness = self.skinthickness.text()
        insulin = self.insulin.text()
        bmi = self.bmi.text()
        diabetespedigreefunction = self.dpf.text()
        age = self.age.text()
        diabetesprobability = self.dprob.text()
        diabetesclass = self.dclass.text()

        # Build class object to store case info
        case_info = CaseInfo(checkingdatetime, pregnacies, glucose, bloodpressure, skinthickness, insulin,\
            bmi, diabetespedigreefunction, age, diabetesprobability, diabetesclass)
        case_data_dict = case_info.return_data_dict()
        case_data_empty_item = case_info.check_empty_key()

        if case_data_empty_item== False:
            mbox = QMessageBox.question(self, "Warning!!!", "Sure to submit?", QMessageBox.Yes | QMessageBox.No)
            if mbox == QMessageBox.Yes:
                predict = load_model_predict([float(pregnacies),  float(glucose), float(bloodpressure), float(skinthickness),\
                            float(insulin), float(bmi), float(diabetespedigreefunction), float(age)])
                self.dprob.setText(predict[0])
                self.dclass.setText(predict[1])
                case_data_dict["DiabetesProbability"] = predict[0]
                case_data_dict["DiabetesClass"] = predict[1]
                if self.action == "add":
                    db.child("users").child(user_id).child("Cases").push(case_data_dict, self.login_user["idToken"])
                else:
                    db.child("users").child(user_id).child("Cases").child(case_id).set(case_data_dict, self.login_user["idToken"])
                QMessageBox.information(self, "Result", f"DiabetesProbability: {predict[0]} \nDiabetesClass: {predict[1]}")
                self.goto_query_page()

# Delete page
class DeletePage(QDialog):
    def __init__(self, login_user, mytimer):
        super(DeletePage, self).__init__()
        loadUi("delete.ui", self)
        self.login_user = login_user
        self.timer = mytimer

        if len(query_row_items) > 0:
            self.caseid.setText(query_row_items[0])
            self.patientid.setText(query_row_items[1])
            self.patientname.setText(query_row_items[2])
            self.patientemail.setText(query_row_items[3])
            self.checkingdatetime.setText(query_row_items[4])

            self.delete_2_btn.clicked.connect(self.delete_case)

            self.query_btn.clicked.connect(self.goto_query_page)

    def delete_case(self):
        mbox = QMessageBox.question(self, "Warning!!!", "Sure to Delete?", QMessageBox.Yes | QMessageBox.No)
        if mbox == QMessageBox.Yes:
            db.child("users").child(query_row_items[1]).child("Cases").child(query_row_items[0]).remove(self.login_user["idToken"])
            self.goto_query_page()

    def goto_query_page(self):
        query_page = QueryPage(self.login_user, self.timer)
        widget.addWidget(query_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

def main():
    login_page = LoginPage()
    widget.addWidget(login_page)
    widget.setFixedWidth(800)
    widget.setFixedHeight(600)
    widget.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()