import os
from Uden_citationstegn import main as uden_citationstegn
from med_citationstegn import main as med_citationstegn

def find_konverter(sti):
    converters = [
        ("uden_citationstegn", uden_citationstegn),
        ("med_citationstegn", med_citationstegn)
    ]
    
    for name, converter in converters:
        try:
            output_file, df_cleaned = converter(sti)
            print(f"{name} virker")
            return output_file, df_cleaned
        except:
            continue 
    
    raise Exception("Alle konverteringsfunktioner fejlede")

if __name__ == "__main__":
    base_sti = os.path.join("F:", "BIBPART-K", "ALF", "ALF organisation", "Grupper", "Analysegruppen", "Kommaformatering", "Filer med dårligt format")
    sti = os.path.join(base_sti, "AU usage 2024.csv")
    output_file, df_cleaned = find_konverter(sti)