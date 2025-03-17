import pandas as pd
import os
import numpy as np
import streamlit as st

def lav_overblik(df):
    """Laver et overblik over data med et søjlediagram over top 10 forlag."""
    kolonne = 'Reporting_Period_Total' if 'Reporting_Period_Total' in df.columns else 'Count' 

    if kolonne not in df.columns or len(df) == 1:
        return None
        
    df = df.dropna(subset=[kolonne])
    if 'Metric_Type' in df.columns and 'Unique_Item_Requests' in df['Metric_Type'].values:
        df = df[df['Metric_Type'] == 'Unique_Item_Requests']
    
    df[kolonne] = df[kolonne].astype(int)
    forlag_brug = df.groupby('Publisher')[kolonne].sum()

    forlag_brug = forlag_brug.sort_values(ascending=False).head(10)

    forlag_brug = forlag_brug.to_dict()

    return forlag_brug

if __name__ == "__main__":
    from læs_tsv import konverter_tsv_tr
    from læs_csv import konverter_csv_tr

    base_sti = os.path.join("F:", "BP", "ALF", "ALF organisation", "Grupper", "Analysegruppen", "Kommaformatering", "Filer med dårligt format", "TSV", "AU TR_J3_2020-01_2022-09.tsv")
    with open(base_sti, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    df = konverter_tsv_tr(lines)
    print(df)
    lav_overblik(df)  