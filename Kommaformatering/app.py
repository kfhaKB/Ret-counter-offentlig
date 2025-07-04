import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import io
from analyse import lav_overblik
from find_konverter import find_konverter

st.title("Filbehandling")

MAX_FILE_SIZE = 100 * 1024 * 1024 

uploaded_file = st.file_uploader("Upload en fil (max 100 MB)", type=["csv", "xlsx", "txt", "json","tsv"])

#st.info('Hjemmesiden er i øjeblikket under opbygning, vær opmærksom på, at der kan være fejl i filerne.')

st.info("""
Streamlit behandler uploadede data udelukkende i **RAM** på den server, hvor applikationen kører. Data slettes fra hukommelsen, så snart behandlingen er afsluttet, og resultatet er downloadet.

Hjemmesiden hostes via **Streamlit Cloud** på Google Cloud Platform, som anvender sikre datacentre og lever op til industristandarder (ISO-27001, SOC 1, SOC 2). Al datatrafik er krypteret med 256-bit kryptering via **HTTPS** og sikres med **HTTP Secure Transport Security (HSTS)**.
""")

if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.getvalue()

        if len(file_bytes) > MAX_FILE_SIZE:
            st.error(f"Filen er for stor. Maksimal filstørrelse er {MAX_FILE_SIZE / (1024 * 1024):.0f} MB.")
            st.stop() 

        fil_navn = uploaded_file.name

        with open(fil_navn, "wb") as f:
            f.write(file_bytes)

        st.info("Behandler filen...")
        output_file, df = find_konverter(fil_navn)

        st.success("Filen er blevet behandlet!")

        with open(output_file, "rb") as f:
            excel_bytes = f.read()

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="Download Excel-fil",
                data=excel_bytes,
                file_name=os.path.join(os.path.basename(fil_navn).split('.')[0], ".xlsx"),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


        forlag_brug = lav_overblik(df)

        if forlag_brug is not None:
            plt.figure(figsize=(10, 6))
            plt.bar(forlag_brug.keys(), forlag_brug.values())
            plt.xlabel("Forlag")
            plt.ylabel("Brug")
            plt.title("Top 10 Forlag Brug")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png')
            img_buffer.seek(0)
            img_bytes = img_buffer.getvalue()

            with col2:
                st.download_button(
                    label="Download diagram som PNG",
                    data=img_bytes,
                    file_name="plot.png",
                    mime="image/png"
                )

            st.image(img_bytes)


    except Exception as e:
        st.error(f"Der opstod en fejl: {e}")