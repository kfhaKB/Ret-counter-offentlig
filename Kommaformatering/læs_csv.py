import pandas as pd

def process_row(row, number_of_columns):
    """Renser og behandler en enkelt række fra DataFrame."""
    row = row['Title'].rsplit(',', number_of_columns)

    if len(row) != number_of_columns + 1:
        return None
    
    row[-1] = row[-1].replace(';', '')

    for i in range(1, len(row)):
        row[i] = row[i].replace('"', '')
        row[i] = int(row[i]) if row[i].isdigit() else row[i]

    return row

def konverter_csv_tr(df):
    columns = df.columns
    nr_commas = len(columns) - 1

    if not df['Publisher'].isnull().all():
        return df

    processed_rows = [process_row(row, nr_commas) for _, row in df.iterrows()]
    processed_rows = [row for row in processed_rows if row]

    if not processed_rows:
        raise ValueError("Ingen gyldige rækker fundet efter behandling.")

    return pd.DataFrame(processed_rows, columns=columns)


def konverter_csv_header(df):
    
    for last in range(1, 16):
        komma_separeret_liste = str(df.iloc[last]).split(',')
        try:
            if 'Created_By' in komma_separeret_liste[-3]:
                break
        except:
            komma_separeret_liste = [i.split('\n') for i in komma_separeret_liste]
            if 'Created_By' in komma_separeret_liste[0][0]:
                break
        
    else:  
        print("Created_By ikke fundet, metadata ikke tilføjet...")
        last = 15
    
    df = df.iloc[0:last].copy()

    for col in df.columns:
        df.loc[:, col] = (df[col].astype(str)
                         .str.replace(';;$', '', regex=True)
                         .str.strip()
                         .replace('nan', ''))
    
    df = df.fillna('')

    return df

if __name__ == "__main__":
    from analyse import lav_overblik
    file_path = r"F:/BP/ALF/ALF organisation/Grupper/Analysegruppen/Kommaformatering/Filer med dårligt format/TRJ3_Springer_KBNL.csv"

    df = None
    for skip in range(11, 15):
        df_temp = pd.read_csv(file_path, skiprows=skip, sep=',')
        df_temp.columns = [col.replace(";", "") for col in df_temp.columns]
        
        if "Title" in df_temp.columns:
            print(f"Found Title at skip={skip}")
            print(df_temp.head())

            try:
                df = konverter_csv_tr(df_temp)
                print("Successfully converted data")
            except ValueError as e:
                print(f"Conversion failed: {e}")
            break 
    
    if df is not None:
        print(df.columns)
        print(lav_overblik(df))
    else:
        print("No valid data found")