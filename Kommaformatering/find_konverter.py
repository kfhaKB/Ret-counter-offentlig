import os
from counter_converter import main as counter_converter

def find_konverter(sti):
    converters = [
        ("counter converter", counter_converter) # Lavet så vi kan udvide med flere konverteringsfunktioner.
    ]
    
    for name, converter in converters:
        output_file, df_cleaned = converter(sti)
        
    return output_file, df_cleaned


if __name__ == "__main__":
    base_sti = os.path.join("F:", "BIBPART-K", "ALF", "ALF organisation", "Grupper", "Analysegruppen", "Kommaformatering", "Filer med dårligt format")
    sti = os.path.join(base_sti, "KU usage 2024.csv")
    output_file, df_cleaned = find_konverter(sti)