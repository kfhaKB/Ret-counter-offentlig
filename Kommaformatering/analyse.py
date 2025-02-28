import pandas as pd
import os
import numpy as np
import streamlit as st

def lav_overblik(df):
    """Laver et overblik over data med et søjlediagram over top 10 forlag."""

    forlag_brug = df.groupby('Publisher')['Reporting_Period_Total'].sum()

    return forlag_brug