import pandas as pd
import os
import numpy as np
import streamlit as st

def lav_overblik(df):
    """Laver et overblik over data med et søjlediagram over top 10 forlag."""

    kolonne = 'Reporting_Period_Total' if 'Reporting_Period_Total' in df.columns else 'Count' 
    if kolonne not in df.columns:
        return None
    
    df[kolonne] = df[kolonne].astype(int)
    forlag_brug = df.groupby('Publisher')[kolonne].sum()

    forlag_brug = forlag_brug.sort_values(ascending=False).head(10)

    forlag_brug = forlag_brug.to_dict()

    return forlag_brug