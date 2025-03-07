import os
import pandas as pd
import chardet
import json
import os
from læs_json import konverter_dr_d2_til_excel, konverter_tr_j3_til_excel
# import streamlit as st

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding'] 


class DataProcessor:
    """Klasse til behandling og rensning af datafiler med problematisk kommaformatering."""

    def __init__(self, file_path, skip_rows=13):
        """Initialiserer med filsti og valgfrit antal rækker, der skal springes over."""
        self.file_path = file_path
        self.skip_rows = skip_rows
        self.base_output_dir = os.path.join(
            "F:", "BP", "ALF", "ALF organisation", "Grupper",
            "Analysegruppen", "Kommaformatering", "Filer med dårligt format", "Rettede filer"
        )

    def load_data(self):
        """Indlæser data fra en fil (csv, xlsx, txt) og returnerer dataframe og filtype."""
        file_ext = os.path.splitext(self.file_path)[-1].lower()

        if file_ext == ".csv":
            return self._load_csv(), file_ext
        elif file_ext == ".xlsx":
            return self._load_excel(), file_ext
        elif file_ext == ".txt":
            return self._load_txt(), file_ext
        elif file_ext == ".json":
            return self._load_json(), file_ext
        else:
            raise ValueError(f"Ikke-understøttet filtype: {file_ext}. Upload venligst en .csv, .xlsx eller .txt fil.")

    def _load_csv(self):
        """Indlæser og parser CSV-filer."""
        for skip in (self.skip_rows, self.skip_rows + 1):
            df = pd.read_csv(self.file_path, skiprows=skip, sep=',')
            df.columns = [col.replace(";", "") for col in df.columns]
            if "Title" in df.columns:
                return df

        raise ValueError("Kunne ikke finde 'Title'-kolonnen i filen.")

    def _load_excel(self):
        """Indlæser og parser Excel-filer."""
        for skip in (self.skip_rows, self.skip_rows + 1):
            df_org = pd.read_excel(self.file_path, skiprows=skip)
            col = df_org.columns.values[0].split(",")
            col = [field.replace("'", "").replace('"', '') for field in col]
            df = pd.DataFrame(columns=col)
            if "Title" in df.columns:
                data = df_org.iloc[:, 0]
                df['Title'] = data
                return df
            
        raise ValueError("Kunne ikke finde 'Title'-kolonnen i filen.")

    def _load_txt(self):
        """Indlæser og parser tekstfiler med UTF-16-LE-kodning."""
        rows = []
        read = False
        fil_encoding = detect_encoding(self.file_path)
        with open(self.file_path, encoding=fil_encoding) as f:
            lines = f.readlines()

        for row in lines:
            row = row.strip()
            if len(''.join(char for char in row if char.isalnum())) < 2:
                continue

            if "Title" in row and "Publisher" in row and "Publisher_ID" in row:
                read = True
                header = row.split(",")
                header = [field.replace('\t\t\n', '') for field in header]
                nr_commas = len(header) - 1
                rows.append(header)
                continue
            elif read:
                parts = row.rsplit(',', nr_commas)
                rows.append(parts)

        return pd.DataFrame(rows[1:], columns=rows[0]) if rows else pd.DataFrame()
    
    def _load_json(self):
        fil_encoding = detect_encoding(self.file_path)
        with open(self.file_path, encoding=fil_encoding) as f:
            json_data = json.load(f)
        if json_data['Report_Header']['Report_ID'] == "DR_D2":
            df = konverter_dr_d2_til_excel(json_data['Report_Items'])
        else:
            df = konverter_tr_j3_til_excel(json_data['Report_Items'])

        return df

    def process_row(self, row):
        """Renser og behandler en enkelt række fra DataFrame."""
        try:
            title_parts = row['Title'].split(',"')
            title_parts = [part.replace('"', '').replace("'", '').replace(";", '') for part in title_parts]

            first_value = title_parts[0]
            if first_value.endswith(','):
                first_value = [first_value[:len(first_value) - 1], '', '']
            else:
                first_value = [first_value]

            title_parts = [part.split(",") for part in title_parts[1:]]
            flattened_list = [value for sublist in title_parts for value in sublist]
            title_parts = first_value + flattened_list

            if len(title_parts) < 10:
                return None

            if len(title_parts) > 2 and 'Press' in title_parts[2]:
                title_parts[1] = title_parts[1] + title_parts[2]
                title_parts.pop(2)

            return title_parts

        except Exception as e:
            print(f"Fejl ved behandling af række: {e}")
            return None

    def process_csv_og_excel_data(self):
        """Behandler data og returnerer renset DataFrame."""
        try:
            df, file_type = self.load_data()
            if file_type == ".txt" or file_type == ".json":
                return df
            else:
                columns = df.columns
                processed_rows = [self.process_row(row) for _, row in df.iterrows()]
                processed_rows = [row for row in processed_rows if row]

                if not processed_rows:
                    raise ValueError("Ingen gyldige rækker fundet efter behandling.")

                return pd.DataFrame(processed_rows, columns=columns)

        except Exception as e:
            raise Exception(f"Fejl under databehandling: {e}")

    def save_result(self, df):
        """Gemmer den behandlede DataFrame til Excel."""
        base_filename = os.path.basename(self.file_path).split(".")[0]
        output_filename = f"{base_filename}.xlsx"

        try:
            output_path = os.path.join(self.base_output_dir, output_filename)
            df.to_excel(output_path, index=False)
        except Exception as e:
            df.to_excel(output_filename, index=False)
            output_path = output_filename

        return output_path

    def run(self):
        """Kører den komplette databehandlingspipeline."""
        df_cleaned = self.process_csv_og_excel_data()
        output_path = self.save_result(df_cleaned)

        return output_path, df_cleaned

def main(file_path, skip_rows=13):
    """Hovedfunktion til at behandle data og gemme som Excel."""
    try:
        processor = DataProcessor(file_path, skip_rows)
        output_path, df_cleaned = processor.run()

        return output_path, df_cleaned

    except Exception as e:
        print(f"Der opstod en fejl: {e}")
        raise

if __name__ == "__main__":
    file_path = r'F:\BP\ALF\ALF organisation\Grupper\Analysegruppen\Kommaformatering\Filer med dårligt format\KU usage 2024.csv'
    main(file_path)