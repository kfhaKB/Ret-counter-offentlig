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