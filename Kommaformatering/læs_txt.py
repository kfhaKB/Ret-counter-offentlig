import pandas as pd

def konverter_txt_tr(data):
    rows = []
    read = False
    for row in data:
            row = row.strip()
            if len(''.join(char for char in row if char.isalnum())) < 2:
                continue

            if "Title" in row and "Publisher" in row and "Publisher_ID" in row:
                read = True
                header = row.split(",")
                header = [field.replace('\t\t\n', '') for field in header]
                nr_commas = len(header) - 1
                rows.append(header)
                continue
            elif read:
                parts = row.rsplit(',', nr_commas)
                rows.append(parts)
    df = pd.DataFrame(rows[1:], columns=rows[0]) if rows else pd.DataFrame()
    return df