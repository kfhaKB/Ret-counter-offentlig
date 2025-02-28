import streamlit as st
import pandas as pd
import os
from Kommaformatering import main 

st.title("Filbehandling")

MAX_FILE_SIZE = 100 * 1024 * 1024 

uploaded_file = st.file_uploader("Upload en fil (max 100 MB)", type=["csv", "xlsx", "txt"])

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
        output_file = main(file_name)
        st.success("Filen er blevet behandlet!")

        with open(output_file, "rb") as f:
            excel_bytes = f.read()

        st.download_button(
            label="Download Excel-fil",
            data=excel_bytes,
            file_name="rettet_fil.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        os.remove(file_name)
        os.remove(output_file)

    except Exception as e:
        st.error(f"Der opstod en fejl: {e}")