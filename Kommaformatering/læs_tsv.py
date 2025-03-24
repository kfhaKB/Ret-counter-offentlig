import pandas as pd
import os

def konverter_tsv_tr(lines):
    """Konverterer en TSV-fil til Excel, springer rækker over indtil 'Title' findes."""

    start_row = None
    for i, line in enumerate(lines):
        if "Publisher" in line:
            start_row = i
            break

    if start_row is None:
        print("Fejl: 'Publisher' blev ikke fundet i filen.")
        return

    data = [line.strip().split('\t') for line in lines[start_row:]]
    if len(data[1:][0]) == 1:
        tom_række = [["" for _ in range(len(data[0]))]]
        return pd.DataFrame(tom_række, columns=data[0])

    df = pd.DataFrame(data[1:], columns=data[0])
    df.columns = [col.replace('"', '') for col in df.columns]

    def remove_first_quote(s):
        if isinstance(s, str):
            return s.replace('"', '', 1)
        return s
    df = df.map(remove_first_quote)
    
    def remove_last_quote(s):
        if isinstance(s, str):
            return s[:s.rfind('"')] + s[s.rfind('"')+1:]
        return s
    df = df.map(remove_last_quote)

    df = df.dropna()

    if 'Metric_Type' in df.columns:
        metric_type_index =  list(df.columns).index('Metric_Type')
        for col in df.columns[metric_type_index+1:]:
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                df[col] = df[col]    

    return df

def konverter_tsv_dr(lines):
    """Konverterer en TSV-fil til Excel, springer rækker over indtil 'Platform' findes."""

    start_row = None
    for i, line in enumerate(lines):
        if "Platform" in line:
            start_row = i
            break

    if start_row is None:
        print("Fejl: 'Platform' blev ikke fundet i filen.")
        return

    data = [line.strip().split('\t') for line in lines[start_row:]]
    
    if len(data[1:][0]) == 1:
        tom_række = [["" for _ in range(len(data[0]))]]
        return pd.DataFrame(tom_række, columns=data[0])
    
    df = pd.DataFrame(data[1:], columns=data[0])
    df.columns = [col.replace('"', '') for col in df.columns]
    df = df.replace({'"': ''}, regex=True)
    
    def remove_first_quote(s):
        if isinstance(s, str):
            return s.replace('"', '', 1)
        return s
    df = df.map(remove_first_quote)
    
    def remove_last_quote(s):
        if isinstance(s, str):
            return s[:s.rfind('"')] + s[s.rfind('"')+1:]
        return s
    df = df.map(remove_last_quote)
    
    df = df.dropna()

    if 'Metric_Type' in df.columns:
        metric_type_index =  list(df.columns).index('Metric_Type')
        for col in df.columns[metric_type_index+1:]:
            df[col] = pd.to_numeric(df[col])
        
    index_names = df[ df['Publisher'] == 'None'].index 
    df.drop(index_names, inplace = True) 

    return df

def tsv_header(lines):
    end_row = None
    for i, line in enumerate(lines):
        if "Platform" in line:
            end_row = i
            break
    
    data = [line.strip().split('\t') for line in lines[:end_row]]
    data_dict = {item[0].strip('"'): item[1].strip('"') if len(item) > 1 else None for item in data}

    df = pd.DataFrame([data_dict]).T
    df.columns = ["Værdier"]
    return df    

if __name__ == "__main__":
    base_sti = os.path.join("F:", "BP", "ALF", "ALF organisation", "Grupper", "Analysegruppen", "Kommaformatering", "Filer med dårligt format", "reports.tsv")

    with open(base_sti, 'r', encoding='utf-8') as file:
            lines = file.readlines()

    #df = konverter_tsv_dr(lines)
    df = konverter_tsv_tr(lines)
    df.to_excel("output.xlsx", index=False)

    #print(lines)