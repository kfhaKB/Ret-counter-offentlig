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
        print("Fejl: 'Title' blev ikke fundet i filen.")
        return

    data = [line.strip().split('\t') for line in lines[start_row:]]
    if len(data[1:][0]) == 1:
        tom_række = [["" for _ in range(len(data[0]))]]
        return pd.DataFrame(tom_række, columns=data[0])

    df = pd.DataFrame(data[1:], columns=data[0])
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

    return df

if __name__ == "__main__":
    base_sti = os.path.join("F:", "BP", "ALF", "ALF organisation", "Grupper", "Analysegruppen", "Kommaformatering", "Filer med dårligt format", "reports(2).tsv")

    with open(base_sti, 'r', encoding='utf-8') as file:
            lines = file.readlines()

    df = konverter_tsv_dr(lines)


    #print(lines)