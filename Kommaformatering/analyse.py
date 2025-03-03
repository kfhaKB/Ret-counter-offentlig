import pandas as pd
import os
import numpy as np
import streamlit as st

def lav_overblik(df):
    """Laver et overblik over data med et søjlediagram over top 10 forlag."""

    df['Reporting_Period_Total'] = df['Reporting_Period_Total'].astype(int)
    forlag_brug = df.groupby('Publisher')['Reporting_Period_Total'].sum()

    forlag_brug = forlag_brug.sort_values(ascending=False).head(10)

    forlag_brug = forlag_brug.to_dict()

    return forlag_brug