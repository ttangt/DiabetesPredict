from PyQt5.QtWidgets import QTableWidgetItem

def return_table_row_number(user_db, admin_email, query_person_email, ALL_STR):
    total_rows = 0

    for user_dict in user_db:
        for _ in user_dict.val()["Cases"]:
            if query_person_email == None or query_person_email == ALL_STR:
                if user_dict.val()["Email"] != admin_email:
                    total_rows += 1
            else:
                if user_dict.val()["Email"] == query_person_email:
                    total_rows += 1

    return total_rows

def setup_tableframe(table, row_number, column_number, headers):
    table.setRowCount(row_number)
    table.setColumnCount(column_number)
    table.setHorizontalHeaderLabels(headers)
    table.verticalHeader().hide()

def insert_data_to_admin_table(table, user_db, admin_email, query_person_email, case_extra, case_all, ALL_STR):
    row_ind = 0
    csv_data = []

    for user_dict in user_db:
        if query_person_email == None or query_person_email == ALL_STR:
            if user_dict.val()["Email"] != admin_email:
                try:
                    for key, value_dict in user_dict.val()["Cases"].items():
                        csv_row = []
                        table.setItem(row_ind, 0, QTableWidgetItem(key))
                        csv_row.append(key)
                        table.setItem(row_ind, 1, QTableWidgetItem(user_dict.key()))
                        csv_row.append(user_dict.key())
                        table.setItem(row_ind, 2, QTableWidgetItem(user_dict.val()["Name"]))
                        csv_row.append(user_dict.val()["Name"])
                        table.setItem(row_ind, 3, QTableWidgetItem(user_dict.val()["Email"]))
                        csv_row.append(user_dict.val()["Email"])

                        for j in range(len(case_extra)):
                            table.setItem(row_ind, j + 4, QTableWidgetItem(value_dict[case_extra[j]]))
                            csv_row.append(value_dict[case_extra[j]])
                        
                        row_ind += 1
                        csv_data.append(csv_row)
                except:
                    pass
        else:
            if user_dict.val()["Email"] == query_person_email:
                try:
                    for key, value_dict in user_dict.val()["Cases"].items():
                        csv_row = []
                        table.setItem(row_ind, 0, QTableWidgetItem(key))
                        csv_row.append(key)
                        table.setItem(row_ind, 1, QTableWidgetItem(user_dict.key()))
                        csv_row.append(user_dict.key())
                        table.setItem(row_ind, 2, QTableWidgetItem(user_dict.val()["Name"]))
                        csv_row.append(user_dict.val()["Name"])
                        table.setItem(row_ind, 3, QTableWidgetItem(user_dict.val()["Email"]))
                        csv_row.append(user_dict.val()["Email"])

                        for j in range(len(case_extra)):
                            table.setItem(row_ind, j + 4, QTableWidgetItem(value_dict[case_extra[j]]))
                            csv_row.append(value_dict[case_extra[j]])
                        
                        row_ind += 1
                        csv_data.append(csv_row)
                except:
                    pass
                
    return table, csv_data

def hide_table_headers(table):
    table.setColumnHidden(0, True)
    table.setColumnHidden(1, True)
    for i in range(5, 13):
        table.setColumnHidden(i, True)
    table.resizeColumnsToContents()

    return table