from PyQt5.QtWidgets import QTableWidgetItem

from admin_table import setup_tableframe

def insert_data_to_table(table, user_id, data, case_extra, case_all):
    csv_data = []
    try:
        cases_dict = data.val()["Cases"]
        cases_ids = list(cases_dict.keys())
        setup_tableframe(table, len(cases_ids), len(case_all), case_all)
        for i in range(len(cases_ids)):
            csv_row = []
            table.setItem(i, 0, QTableWidgetItem(cases_ids[i]))
            csv_row.append(cases_ids[i])
            table.setItem(i, 1, QTableWidgetItem(user_id))
            csv_row.append(user_id)
            table.setItem(i, 2, QTableWidgetItem(data.val()["Name"]))
            csv_row.append(data.val()["Name"])
            table.setItem(i, 3, QTableWidgetItem(data.val()["Email"]))
            csv_row.append(data.val()["Email"])
            for j in range(len(case_extra)):
                table.setItem(i, j + 4, QTableWidgetItem(cases_dict[cases_ids[i]][case_extra[j]]))
                csv_row.append(cases_dict[cases_ids[i]][case_extra[j]])

            csv_data.append(csv_row)

    except Exception as e: # No case
        pass
        print(e)

    return table, csv_data