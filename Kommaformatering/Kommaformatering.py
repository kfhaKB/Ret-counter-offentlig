import pandas as pd
import os
import streamlit as st

def load_data(sti, skip_rækker=13):
    """Indlæser data fra en fil (csv, xlsx, txt)."""
    try:
        filtype = os.path.splitext(sti)[-1]
        if filtype == ".csv":
            df = pd.read_csv(sti, skiprows=skip_rækker, sep=',')
            df.columns = [col.replace(";", "") for col in df.columns]

        elif filtype == ".xlsx":
            df_org = pd.read_excel(sti, skiprows=0)
            col = df_org.columns.values[0].split(",")
            col = [f.replace("'", "").replace('"', '') for f in col]
            df = pd.DataFrame(columns=col)
            data = df_org.iloc[:, 0]
            df['Title'] = data

        elif filtype == ".txt":
            rows = []
            read = False
            with open(sti, encoding="utf-16-le") as f:
                lines = f.readlines()
            for row in lines:
                row = row.strip()
                if len(''.join(e for e in row if e.isalnum())) < 2:
                    continue
                if "Title" in row and "Publisher" in row and "Publisher_ID" in row:
                    read = True
                    header = row.split(",")
                    header = [f.replace('\t\t\n', '') for f in header]
                    nr_commas = len(header) - 1
                    rows.append(header)
                    continue
                elif read:
                    parts = row.rsplit(',', nr_commas)
                    rows.append(parts)
            df = pd.DataFrame(rows[1:], columns=rows[0])

        else:
            raise ValueError(f"Ukendt filtype: {filtype}. Upload venligst en .csv, .xlsx eller .txt fil.")

        return df, filtype

    except FileNotFoundError:
        raise FileNotFoundError(f"Filen {sti} blev ikke fundet.")
    except Exception as e:
        raise Exception(f"Der opstod en fejl under indlæsning af data: {e}")

def læs_rækker(række):
    """Renser og læser rækker fra DataFrame."""
    try:
        titel_dele = række['Title'].split(',"')
        titel_dele = [f.replace('"', '').replace("'", '').replace(";", '') for f in titel_dele]
        første_værdi = titel_dele[0]
        if første_værdi.endswith(','):
            første_værdi = [første_værdi[:len(første_værdi) - 1], '', '']
        else:
            første_værdi = [første_værdi]
        titel_dele = [f.split(",") for f in titel_dele[1:]]
        flad_liste = [værdi for liste in titel_dele for værdi in liste]
        titel_dele = første_værdi + flad_liste
        if len(titel_dele) < 10:
            return None
        if 'Press' in titel_dele[2]:
            titel_dele[1] = titel_dele[1] + titel_dele[2]
            titel_dele.pop(2)
        return titel_dele
    except Exception as e:
        raise Exception(f"Der opstod en fejl under behandling af rækker: {e}")

def main(sti):
    """Hovedfunktion til at behandle data og gemme som Excel."""
    try:
        st.info("Indlæser data...") 
        df, filtype = load_data(sti)
        if filtype == ".txt":
            df_cleaned = df
        else:
            rækker = [læs_rækker(row) for _, row in df.iterrows()]
            rækker = [r for r in rækker if r]
            if not rækker:
                raise ValueError("Ingen gyldige rækker fundet efter behandling.")
            df_cleaned = pd.DataFrame(rækker, columns=df.columns[:len(rækker[0])])
        output_file = "rettet_fil.xlsx"
        st.info("Gemmer filen...") 
        df_cleaned.to_excel(output_file, index=False)
        return output_file
    except Exception as e:
        raise Exception(f"Der opstod en fejl under databehandlingen: {e}")

if __name__ == "__main__":
    sti =...
    main(sti)