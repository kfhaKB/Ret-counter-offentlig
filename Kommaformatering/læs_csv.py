import pandas as pd

def process_row(row):
    """Renser og behandler en enkelt række fra DataFrame."""
    # TODO: Skal opdateres til at kunne læse filer uden citationstegn i titlerne.
    try:
        title_parts = row['Title'].split(',"')
        title_parts = [part.replace('"', '').replace("'", '').replace(";", '') for part in title_parts]

        first_value = title_parts[0]
        if first_value.endswith(','):
            first_value = [first_value[:len(first_value) - 1], '', '']
        else:
            first_value = [first_value]

        title_parts = [part.split(",") for part in title_parts[1:]]
        flattened_list = [value for sublist in title_parts for value in sublist]
        title_parts = first_value + flattened_list

        if len(title_parts) < 10:
            return None

        if len(title_parts) > 2 and 'Press' in title_parts[2]:
            title_parts[1] = title_parts[1] + title_parts[2]
            title_parts.pop(2)

        return title_parts

    except Exception as e:
        print(f"Fejl ved behandling af række: {e}")
        return None

def konverter_csv_tr(df):
    columns = df.columns
    processed_rows = [process_row(row) for _, row in df.iterrows()]
    processed_rows = [row for row in processed_rows if row]

    if not processed_rows:
        raise ValueError("Ingen gyldige rækker fundet efter behandling.")

    return pd.DataFrame(processed_rows, columns=columns)