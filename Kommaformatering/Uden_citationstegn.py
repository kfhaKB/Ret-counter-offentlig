import pandas as pd

def load_data(sti, skip_rækker, filtype):
    if filtype == "csv":
        df = pd.read_csv(sti, skiprows=skip_rækker, sep=',')
        df.columns = [col.replace(";", "") for col in df.columns]

    if filtype == "excel":
        df_org = pd.read_excel(sti, skiprows=skip_rækker)
        col = df_org.columns.values[0].split(",")
        col = [f.replace("'", "").replace('"', '') for f in col]
        df = pd.DataFrame(columns = col)

        data = df_org.iloc[:, 0]
        df['Title'] = data
             
    return df 

#Funktion som splitter på de sidste 23 hændelser af "," (da 24 kolonner)
def split_last_n_commas(s, n=23):
    #Position af sidset 23 kommaer
    comma_positions = [i for i, char in enumerate(reversed(s)) if char == ',']
    if len(comma_positions) < n:
        #Mindre end n kommaer, så split alle
        split_positions = [len(s) - i - 1 for i in comma_positions]
    else:
        #Ellers så split kun 23 sidste kommaer
        split_positions = [len(s) - i - 1 for i in comma_positions[:n]]

    #Splitter string (rækker) med brug af ovenstående position af kommaer
    parts = []
    prev_pos = 0
    for pos in sorted(split_positions):
        parts.append(s[prev_pos:pos])
        prev_pos = pos + 1
    parts.append(s[prev_pos:])  #Sidste del af string

    return parts

def main(sti, skip_rækker, filtype):
    df = load_data(sti, skip_rækker, filtype)
    split_columns = df['Title'].apply(split_last_n_commas).apply(pd.Series)
    col_names = df.columns.values
    split_columns.columns = col_names
    split_columns.to_excel(r"P:\Kommaseperation\Springer forsøg.xlsx", index=False)

if __name__ == "__main__":
    sti = r"P:\Kommaseperation\Springer txt.xlsx" #har været .txt men loadet i excel. Bemærk; ingen "", så "læs_rækker"-funktion virker ikke
    main(sti, 15, "excel")