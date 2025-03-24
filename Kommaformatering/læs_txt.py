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

def txt_header(data):
    rows = []
    read = True
    for row in data:
        row = row.strip()
        if len(''.join(char for char in row if char.isalnum())) < 2:
            continue

        if "Title" in row and "Publisher" in row and "Publisher_ID" in row:
            read = False

        if read:
            rows.append(row.split(','))

    data_dict = {item[0]: item[1] if len(item) > 1 else None for item in rows}
    df = pd.DataFrame([data_dict]).T
    df.columns = ["Værdier"]
    return df