import os
import pandas as pd
import chardet
import json
import os
from læs_json import json_header, konverter_json_dr_d2, konverter_json_tr_b3, konverter_json_tr_master, konverter_json_tr_j1, konverter_json_tr_j3, konverter_json_tr_j4
from læs_txt import konverter_txt_tr, txt_header
from læs_tsv import konverter_tsv_tr, konverter_tsv_dr, tsv_header
from læs_csv import konverter_csv_tr, konverter_csv_header
from læs_excel import konverter_excel_tr, excel_header
import streamlit as st

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding'] 


class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

        file_type_mapping = {
            ".csv": "CSV",
            ".xlsx": "Excel",
            ".txt": "TXT",
            ".json": "JSON",
            ".tsv": "TSV",
        }

        file_ext = os.path.splitext(self.file_path)[-1].lower()

        if file_ext not in file_type_mapping:
            raise ValueError(f"Ikke-understøttet filtype: {file_ext}. Upload venligst en .csv, .xlsx, .txt, .json eller .tsv fil.")

        self.base_output_dir = os.path.join(
            "F:", "BP", "ALF", "ALF organisation", "Grupper",
            "Analysegruppen", "Kommaformatering", "Filer med dårligt format",
            file_type_mapping[file_ext], "Rettede filer"
        )

    def load_data(self):
        file_ext = os.path.splitext(self.file_path)[-1].lower()

        if file_ext == ".csv":
            return self._load_csv()
        elif file_ext == ".xlsx":
            return self._load_excel()
        elif file_ext == ".txt":
            return self._load_txt()
        elif file_ext == ".json":
            return self._load_json()
        elif file_ext == ".tsv":
            return self._load_tsv()
        else:
            raise ValueError(f"Ikke-understøttet filtype: {file_ext}. Upload venligst en .csv, .xlsx eller .txt fil.")

    def _load_csv(self):
        for skip in range(20):
            
            df = pd.read_csv(self.file_path, skiprows=skip, sep=',', on_bad_lines='skip')
            df.columns = [col.replace(";", "") for col in df.columns]

            if "Report_Name" in df.columns[0] or "Report_Name" in df.columns:
                header = konverter_csv_header(df)

            if "Title" in df.columns and "Publisher" in df.columns or (len(df.columns) > 0 and "Title" in df.columns[0] or "Publisher" in df.columns[0]):
                df_counter = konverter_csv_tr(df)
                return df_counter, header

        raise ValueError("Kunne ikke finde 'Title'-kolonnen i filen.")

    def _load_excel(self):
        for skip in range(20):

            df_org = pd.read_excel(self.file_path, skiprows=skip, nrows=50)
            if "Report_Name" in df_org.columns[0] or "Report_Name" in df_org.columns:
                header = excel_header(df_org)
            
            if "Title" in df_org.columns and "Publisher" in df_org.columns and not df_org['Publisher'].isnull().all() and not df_org['YOP'].isnull().all():
                df = pd.read_excel(self.file_path, skiprows=skip)
                return df, header
    
            col = df_org.columns.values[0].split(",")
            col = [field.replace("'", "").replace('"', '') for field in col]
            df = pd.DataFrame(columns=col)

            if "Title" in df.columns and "Publisher" in df.columns:
                df_org = pd.read_excel(self.file_path, skiprows=skip)
                col = df_org.columns.values[0].split(",")
                col = [field.replace("'", "").replace('"', '') for field in col]
                df = pd.DataFrame(columns=col)
                data = df_org.iloc[:, 0]
                df['Title'] = data
                df = konverter_excel_tr(df)
                return df, header
            
        raise ValueError("Kunne ikke finde 'Title'-kolonnen i filen.")

    def _load_txt(self):
        fil_encoding = detect_encoding(self.file_path)
        with open(self.file_path, encoding=fil_encoding) as f:
            lines = f.readlines()
        header = txt_header(lines)
        df = konverter_txt_tr(lines)
        return df, header
    
    def _load_json(self):
        fil_encoding = detect_encoding(self.file_path)
        with open(self.file_path, encoding=fil_encoding) as f:
            json_data = json.load(f)

        header = json_header(json_data)

        if json_data['Report_Header']['Report_ID'] == "TR":
            df = konverter_json_tr_master(json_data['Report_Items'])
        elif json_data['Report_Header']['Report_ID'] == "TR_J1":
            df = konverter_json_tr_j1(json_data['Report_Items'])
        elif json_data['Report_Header']['Report_ID'] == "TR_J3":
            df = konverter_json_tr_j3(json_data['Report_Items'])
        elif json_data['Report_Header']['Report_ID'] == "TR_J4":
            df = konverter_json_tr_j4(json_data['Report_Items'])
        elif json_data['Report_Header']['Report_ID'] == "TR_B3":
            df = konverter_json_tr_b3(json_data['Report_Items'])
        elif json_data['Report_Header']['Report_ID'] == "DR_D2":
            df = konverter_json_dr_d2(json_data['Report_Items'])
        
        else:
            raise ValueError(f"Ukendt rapporttype: {json_data['Report_Header']['Report_ID']}")
        return df, header
    
    def _load_tsv(self):
        fil_encoding = detect_encoding(self.file_path)
        with open(self.file_path, 'r', encoding=fil_encoding) as file:
            lines = file.readlines()

        header = tsv_header(lines)   
        if "DR" in lines[1]:
            df = konverter_tsv_dr(lines)
        elif "TR" in lines[1]:
            df = konverter_tsv_tr(lines)

        return df, header

    def gem_result(self, df, header):
        base_filename = os.path.basename(self.file_path).split(".")[0]
        output_filename = f"{base_filename}.xlsx"
        if header is not None:
            index_bool = True if len(header.columns) == 1 else False
        try:
            output_path = os.path.join(self.base_output_dir, output_filename)
            with pd.ExcelWriter(output_path) as writer:
                df.to_excel(writer, sheet_name='Counter', index=False)
                if header is not None:
                    header.to_excel(writer, sheet_name='Meta data', index=index_bool) 

        except Exception:
            output_path = output_filename
            with pd.ExcelWriter(output_path) as writer:
                df.to_excel(writer, sheet_name='Counter',index=False)
                if header is not None:
                    header.to_excel(writer, sheet_name='Meta data', index=index_bool)

        return output_path

    def run(self):
        df_cleaned, header = self.load_data()
        output_path = self.gem_result(df_cleaned, header)
    
        return output_path, df_cleaned

def main(file_path):
    try:
        processor = DataProcessor(file_path)
        output_path, df_cleaned = processor.run()

        return output_path, df_cleaned

    except Exception as e:
        print(f"Der opstod en fejl: {e}")
        raise

if __name__ == "__main__":
    file_path = r'F:\BP\ALF\ALF organisation\Grupper\Analysegruppen\Kommaformatering\Filer med dårligt format\KU usage 2024.csv'
    main(file_path)