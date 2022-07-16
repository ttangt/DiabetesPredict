import pandas as pd
import numpy as np

output_data_file = "output.csv"

def write_csv(csv_data, case_all):
    transposed_csv_data = np.transpose(csv_data)

    csv_dict = {}

    for i in range(len(case_all)):
        csv_dict[case_all[i]] = transposed_csv_data[i]

    df = pd.DataFrame(csv_dict)
    df.drop(columns = ["CaseID", "PatientID"], inplace = True)
    
    df.to_csv(output_data_file, index=False)