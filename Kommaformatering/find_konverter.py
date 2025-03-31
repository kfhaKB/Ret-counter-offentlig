import os
from counter_converter import main as counter_converter

def find_konverter(sti):
    converters = [
        ("counter converter", counter_converter) # Lavet så vi kan udvide med flere konverteringsfunktioner. Eks, hvis vi skal konvertere titellister eller andet.
    ]
    
    for _, converter in converters:
        output_file, df_cleaned = converter(sti)
        
    return output_file, df_cleaned


if __name__ == "__main__":
    from tqdm import tqdm
    from analyse import lav_overblik
    # Kører alle filerne igennem for at tjekke, at de kan konverteres. Anbefales at gøre før push.

    #MAX_FILE_SIZE = 40 * 1024 * 1024  # hvis du er doven og ikke vil vente længe...
    
    mappe = "TXT"

    base_sti = os.path.join("F:", "BP", "ALF", "ALF organisation", "Grupper", "Analysegruppen", "Kommaformatering", "Filer med dårligt format", mappe)
    filer = os.listdir(base_sti)
    filer = [fil for fil in filer if "." in fil]
    print("Konverterer filer fra mappen:", mappe)
    tqdm_bar = tqdm(filer, desc="Konverterer filer")
    for fil in tqdm_bar:
        sti = os.path.join(base_sti, fil)

        fil_sti = os.path.join(base_sti, fil)
        file_size = os.path.getsize(fil_sti)
        
        #if file_size > MAX_FILE_SIZE:
        #    print(f"Springer {fil} over - filen er for stor ({file_size / (1024*1024):.1f} MB)")
        #    continue

        tqdm_bar.set_postfix(fil=fil)

        output_file, df_cleaned = find_konverter(sti)
        forlag_brug = lav_overblik(df_cleaned)
