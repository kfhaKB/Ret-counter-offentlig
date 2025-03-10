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
    from tqdm import tqdm
    # Kører alle filerne igennem for at tjekke, at de kan konverteres.
    base_sti = os.path.join("F:", "BP", "ALF", "ALF organisation", "Grupper", "Analysegruppen", "Kommaformatering", "Filer med dårligt format")
    filer = os.listdir(base_sti)
    filer = [fil for fil in filer if "." in fil]
    tqdm_bar = tqdm(filer, desc="Konverterer filer")
    for fil in tqdm_bar:
        tqdm_bar.set_postfix_str("Konverterer fil", fil)
        sti = os.path.join(base_sti, fil)
        output_file, df_cleaned = find_konverter(sti)