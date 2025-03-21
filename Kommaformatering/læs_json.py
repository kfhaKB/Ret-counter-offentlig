import os
import json
import pandas as pd

def json_header(data):
    excel_data = []
    
    report_name = data["Report_Header"]["Report_Name"]
    created = data["Report_Header"]["Created"]
    created_by = data["Report_Header"]["Created_By"]
    customer_ID = data["Report_Header"]["Customer_ID"]
    report_ID = data["Report_Header"]["Report_ID"]
    release = data["Report_Header"]["Release"]
    inst_name = data["Report_Header"]["Institution_Name"]
    for item in data['Report_Header']['Report_Filters']:
        access_type = item['Value']
    excel_data.append({
        "Report_Name": report_name,
        "Created": created,
        "Created_By": created_by,
        "Customer_ID": customer_ID, 
        "Report_ID": report_ID,
        "Release": release, 
        "Institution_Name": inst_name,
        "Access_Type": access_type
    })

    df = pd.DataFrame(excel_data)
    df = df.melt()
    df.columns = [col.title() for col in df.columns]
    return df


def konverter_json_dr_d2(data):
    excel_data = []

    for item in data:
        platform = item['Platform']
        database = item['Database']
        publisher = item['Publisher']
        for performance in item['Performance']:
            metric_type = performance['Instance'][0]['Metric_Type']
            count = int(performance['Instance'][0]['Count'])
            begin_date = performance['Period']['Begin_Date']
            end_date = performance['Period']['End_Date']
            excel_data.append({
                'Platform': platform,
                'Database': database,
                'Publisher': publisher,
                'Metric Type': metric_type,
                'Count': count,
                'Begin Date': begin_date,
                'End Date': end_date
            })

    df = pd.DataFrame(excel_data)
    return df

def konverter_json_tr_b3(data):
    excel_data = []

    for item in data:
        platform = item["Platform"]
        access_type = item["Access_Type"]
        title = item["Title"]
        publisher = item["Publisher"]
        yop = item["YOP"]
        doi = next((id_item["Value"] for id_item in item["Item_ID"] if id_item["Type"] == "DOI"), None)
        isbn = next((id_item["Value"] for id_item in item["Item_ID"] if id_item["Type"] == "ISBN"), None)
        print_issn = next((id_item["Value"] for id_item in item["Item_ID"] if id_item["Type"] == "Print_ISSN"), None)
        proprietary_id = next(
            (id_item["Value"] for id_item in item["Item_ID"] if id_item["Type"] == "Proprietary"), None
        )

        for performance in item["Performance"]:
            begin_date = performance["Period"]["Begin_Date"]
            end_date = performance["Period"]["End_Date"]

            for instance in performance["Instance"]:
                metric_type = instance["Metric_Type"]
                count = int(instance["Count"])

                excel_data.append(
                    {
                        "Platform": platform,
                        "Access Type": access_type,
                        "Title": title,
                        "Publisher": publisher,
                        "YOP": yop,
                        "DOI": doi,
                        "ISBN": isbn,
                        "Print ISSN": print_issn,
                        "Proprietary ID": proprietary_id,
                        "Begin Date": begin_date,
                        "End Date": end_date,
                        "Metric Type": metric_type,
                        "Count": count,
                    }
                )

    df = pd.DataFrame(excel_data)
    return df

def konverter_json_tr_master(data):
    excel_data = []

    for item in data:
        platform = item.get("Platform")
        title = item.get("Title")
        publisher = item.get("Publisher")
        item_ids = item.get("Item_ID", [])
        performances = item.get("Performance", [])

        proprietary_id = next((id_info["Value"] for id_info in item_ids if id_info["Type"] == "Proprietary"), None)
        doi = next((id_info["Value"] for id_info in item_ids if id_info["Type"] == "DOI"), None)
        isbn = next((id_info["Value"] for id_info in item_ids if id_info["Type"] == "ISBN"), None)

        for performance in performances:
            instances = performance.get("Instance", [])
            period = performance.get("Period", {})
            begin_date = period.get("Begin_Date")
            end_date = period.get("End_Date")

            for instance in instances:
                metric_type = instance.get("Metric_Type")
                count = instance.get("Count")

                excel_data.append({
                    "Platform": platform,
                    "Title": title,
                    "Publisher": publisher,
                    "Proprietary ID": proprietary_id,
                    "DOI": doi,
                    "ISBN": isbn,
                    "Begin Date": begin_date,
                    "End Date": end_date,
                    "Metric Type": metric_type,
                    "Count": count,
                })

    return pd.DataFrame(excel_data)

def konverter_json_tr_j1(data):

    excel_data = []
    for item in data:
        platform = item["Platform"]
        title = item["Title"]
        publisher = item["Publisher"]
        item_ids = item["Item_ID"]
        performances = item["Performance"]

        for performance in performances:
            period = performance["Period"]
            begin_date = period["Begin_Date"]
            end_date = period["End_Date"]

            for instance in performance["Instance"]:
                metric_type = instance["Metric_Type"]
                count = instance["Count"]

                flattened_item = {
                    "Platform": platform,
                    "Title": title,
                    "Publisher": publisher,
                    "Begin_Date": begin_date,
                    "End_Date": end_date,
                    "Metric_Type": metric_type,
                    "Count": count,
                }

                for item_id in item_ids:
                    flattened_item[item_id["Type"]] = item_id["Value"]

                excel_data.append(flattened_item)

    return pd.DataFrame(excel_data)


def konverter_json_tr_j3(data):

    excel_data = []
    for item in data:
        platform = item["Platform"]
        access_type = item['Access_Type']
        title = item["Title"]
        publisher = item["Publisher"]
        item_ids = item["Item_ID"]
        performances = item["Performance"]

        for performance in performances:
            period = performance["Period"]
            begin_date = period["Begin_Date"]
            end_date = period["End_Date"]

            for instance in performance["Instance"]:
                metric_type = instance["Metric_Type"]
                count = instance["Count"]

                flattened_item = {
                    "Platform": platform,
                    "Access_Type": access_type,
                    "Title": title,
                    "Publisher": publisher,
                    "Begin_Date": begin_date,
                    "End_Date": end_date,
                    "Metric_Type": metric_type,
                    "Count": count,
                }

                for item_id in item_ids:
                    flattened_item[item_id["Type"]] = item_id["Value"]

                excel_data.append(flattened_item)

    return  pd.DataFrame(excel_data)  

def konverter_json_tr_j4(data):
    excel_data = []

    for item in data:
        platform = item.get("Platform")
        title = item.get("Title")
        publisher = item.get("Publisher")
        yop = item.get("YOP")
        item_ids = item.get("Item_ID", [])
        performances = item.get("Performance", [])

        proprietary_id = next((id_info["Value"] for id_info in item_ids if id_info["Type"] == "Proprietary"), None)
        online_issn = next((id_info["Value"] for id_info in item_ids if id_info["Type"] == "Online_ISSN"), None)
        print_issn = next((id_info["Value"] for id_info in item_ids if id_info["Type"] == "Print_ISSN"), None)

        for performance in performances:
            instances = performance.get("Instance", [])
            period = performance.get("Period", {})
            begin_date = period.get("Begin_Date")
            end_date = period.get("End_Date")

            for instance in instances:
                metric_type = instance.get("Metric_Type")
                count = instance.get("Count")

                excel_data.append({
                    "Platform": platform,
                    "Title": title,
                    "Publisher": publisher,
                    "YOP": yop,
                    "Proprietary ID": proprietary_id,
                    "Online ISSN": online_issn,
                    "Print ISSN": print_issn,
                    "Begin Date": begin_date,
                    "End Date": end_date,
                    "Metric Type": metric_type,
                    "Count": count,
                })

    return pd.DataFrame(excel_data)


if __name__ == "__main__":
    base_sti = os.path.join("F:", "BP", "ALF", "ALF organisation", "Grupper", "Analysegruppen", "Kommaformatering", "Filer med dårligt format", "JSON", "SUSHI_Wiley Online Library_tr_j4_202312_102572782800005763_0_response.json")

    with open(base_sti, encoding="utf-8") as f:
        data = json.load(f)

    if data['Report_Header']['Report_ID'] == "DR_D2":
        df = konverter_json_dr_d2(data['Report_Items'])
    elif data['Report_Header']['Report_ID'] == "TR_B3":
        df = konverter_json_tr_b3(data['Report_Items'])
    elif data['Report_Header']['Report_ID'] == "TR_J1":
        df = konverter_json_tr_j1(data['Report_Items'])
    elif data['Report_Header']['Report_ID'] == "TR_J3":
        df = konverter_json_tr_j3(data['Report_Items'])
    elif data['Report_Header']['Report_ID'] == "TR_J4":
        df = konverter_json_tr_j4(data['Report_Items'])

    df.to_excel("output.xlsx", index=False)
