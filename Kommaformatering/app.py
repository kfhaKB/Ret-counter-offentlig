import streamlit as st
import pandas as pd
import os
from Kommaformatering import main 
import matplotlib.pyplot as plt
import io
from analyse import lav_overblik

st.title("Filbehandling")

MAX_FILE_SIZE = 100 * 1024 * 1024 

uploaded_file = st.file_uploader("Upload en fil (max 100 MB), ellers kan hjemmesiden ikke håndtere det. Send i stedet filen direkte til analysegruppen.", type=["csv", "xlsx", "txt"])

if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.getvalue()

        if len(file_bytes) > MAX_FILE_SIZE:
            st.error(f"Filen er for stor. Maksimal filstørrelse er {MAX_FILE_SIZE / (1024 * 1024):.0f} MB.")
            st.stop() 

        file_name = uploaded_file.name

        with open(file_name, "wb") as f:
            f.write(file_bytes)

        st.info("Behandler filen...")
        output_file, df = main(file_name)
        st.success("Filen er blevet behandlet!")

        forlag_brug = lav_overblik(df)

        with open(output_file, "rb") as f:
            excel_bytes = f.read()

        st.download_button(
            label="Download Excel-fil",
            data=excel_bytes,
            file_name="rettet_fil.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        plt.figure(figsize=(10, 6))
        st.info("Behandler barplot...")
        plt.bar(forlag_brug.keys(), forlag_brug.values())
        st.info("Behandler lavet barplot...")
        plt.xlabel("Forlag")
        plt.ylabel("Brug")
        plt.title("Top 10 Forlag Brug")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        st.info("laver filen...")
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        img_bytes = img_buffer.getvalue()

        st.info("downloader billede filen...")

        st.download_button(
            label="Download Plot som PNG",
            data=img_bytes,
            file_name="plot.png",
            mime="image/png"
        )
        os.remove(file_name)
        os.remove(output_file)

    except Exception as e:
        st.error(f"Der opstod en fejl: {e}")