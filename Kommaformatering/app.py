import streamlit as st
import pandas as pd
import os
from Kommaformatering import main 

st.title("Filbehandling")

uploaded_file = st.file_uploader("Upload en fil", type=["csv", "xlsx", "txt"])

if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.getvalue()
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