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

st.info('Hjemmesiden er i øjeblikket under opbygning, vær opmærksom på, at der kan være fejl i filerne.')

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

        if 'Reporting_Period_Total' in df.columns:
            metric_type_index = list(df.columns).index('Reporting_Period_Total')
            numeric_columns = df.columns[metric_type_index + 1:]
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype('int64')

            # Save with specified data types
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
                worksheet = writer.sheets['Sheet1']
                
                # Set number format for integer columns
                for idx, col in enumerate(df.columns):
                    if col in numeric_columns:
                        col_letter = chr(65 + idx)  # Convert column index to letter (A, B, C, etc.)
                        worksheet.column_dimensions[col_letter].number_format = '0'


        st.success("Filen er blevet behandlet!")

        with open(output_file, "rb") as f:
            excel_bytes = f.read()

        col1, col2 = st.columns(2)

        st.write(output_file)

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