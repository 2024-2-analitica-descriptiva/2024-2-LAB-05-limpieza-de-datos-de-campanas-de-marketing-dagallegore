"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

import os
import zipfile
import pandas as pd

def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    INPUT_FOLDER = "files/input/"
    OUTPUT_FOLDER = "files/output/"

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    zip_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".zip")]

    client_data = []
    campaign_data = []
    economics_data = []

    for zip_file in zip_files:
        with zipfile.ZipFile(os.path.join(INPUT_FOLDER, zip_file), 'r') as z:
            for filename in z.namelist():
                if filename.endswith(".csv"):
                    with z.open(filename) as f:
                        df = pd.read_csv(f)

                        client_df = df[[
                            'client_id', 'age', 'job', 'marital', 'education',
                            'credit_default', 'mortgage'
                        ]].copy()

                        client_df['job'] = client_df['job'].str.replace(".", "", regex=False)
                        client_df['job'] = client_df['job'].str.replace("-", "_", regex=False)
                        client_df['education'] = client_df['education'].str.replace(".", "_", regex=False)
                        client_df['education'] = client_df['education'].replace("unknown", pd.NA)
                        client_df['credit_default'] = client_df['credit_default'].apply(lambda x: 1 if x == "yes" else 0)
                        client_df['mortgage'] = client_df['mortgage'].apply(lambda x: 1 if x == "yes" else 0)
                        client_data.append(client_df)

                        campaign_df = df[[
                            'client_id', 'number_contacts', 'contact_duration',
                            'previous_campaign_contacts', 'previous_outcome', 'campaign_outcome',
                            'day', 'month'
                        ]].copy()

                        campaign_df['previous_outcome'] = campaign_df['previous_outcome'].apply(lambda x: 1 if x == "success" else 0)
                        campaign_df['campaign_outcome'] = campaign_df['campaign_outcome'].apply(lambda x: 1 if x == "yes" else 0)
                        campaign_df['last_contact_date'] = pd.to_datetime(
                            "2022-" + campaign_df['month'].astype(str) + "-" + campaign_df['day'].astype(str),
                            format="%Y-%b-%d",
                            errors="coerce"
                        ).dt.strftime("%Y-%m-%d")
                        campaign_df.drop(columns=['day', 'month'], inplace=True)
                        campaign_data.append(campaign_df)

                        economics_df = df[[
                            'client_id', 'cons_price_idx', 'euribor_three_months'
                        ]].copy()
                        economics_data.append(economics_df)

    pd.concat(client_data).to_csv(os.path.join(OUTPUT_FOLDER, "client.csv"), index=False)
    pd.concat(campaign_data).to_csv(os.path.join(OUTPUT_FOLDER, "campaign.csv"), index=False)
    pd.concat(economics_data).to_csv(os.path.join(OUTPUT_FOLDER, "economics.csv"), index=False)

if __name__ == "__main__":
    clean_campaign_data()