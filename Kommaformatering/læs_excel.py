from læs_csv import process_row
import pandas as pd

def konverter_excel_tr(df):
    columns = df.columns
    nr_commas = len(columns) - 1
    processed_rows = [process_row(row, nr_commas) for _, row in df.iterrows()]
    processed_rows = [row for row in processed_rows if row]

    if not processed_rows:
        raise ValueError("Ingen gyldige rækker fundet efter behandling.")

    return pd.DataFrame(processed_rows, columns=columns)

def excel_header(df):
    header_data = []
    for value in df.iloc[:, 0]: 
        if pd.notna(value):
            header_data.append(value)
        if isinstance(value, float):
            break 

    if not header_data:
        return None  
    data_dict = {}
    for item in header_data:
        if isinstance(item, str): 
            try:
                key, value = item.split(',', 1)
                data_dict[key.strip('"')] = value.strip('"')
            except ValueError:
                print(f"Advarsel: Forkert header '{item}'")
        else:
            break 

    if not data_dict:
        return None

    result_df = pd.DataFrame([data_dict]).T
    result_df.columns = ["Værdier"]
    return result_df