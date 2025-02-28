import pandas as pd
import os
import numpy as np
import streamlit as st

def lav_overblik(df):
    """Laver et overblik over data med et søjlediagram over top 10 forlag."""

    forlag_brug = df.groupby('Publisher')['Reporting_Period_Total'].sum()

    st.write(forlag_brug).head(10)

    forlag_brug = forlag_brug.sort_values(ascending=False).head(10)

    print(forlag_brug).head(10)

    # lav det til en dictionary
    forlag_brug = forlag_brug.to_dict()

    print(forlag_brug)

    return forlag_brug