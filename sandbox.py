import time
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import io

# Charger les données depuis Excel avec pandas
df = pd.read_excel('Results.xlsx', engine='openpyxl')

# Information pour l'authentification avec Google Cloud
credentials = service_account.Credentials.from_service_account_file(
    'C://Users//henri//ESILV_A4//PI2//kapkool-d6bba-87f258388ce7.json',
)

# Paramètres BigQuery
project_id = 'kapkool-d6bba'
dataset_id = 'test'
table_id = 'OSINT'  

# Initialiser un client BigQuery avec des credentials
client = bigquery.Client(credentials=credentials, project=project_id)

# Chemin complet de la table
table_ref = f"{project_id}.{dataset_id}.{table_id}"

# Charger les données dans BigQuery
job_config = bigquery.LoadJobConfig(
    write_disposition="WRITE_EMPTY",  
    autodetect=True,  
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON 
)

try:
    # Convertir le DataFrame en JSON pour le chargement
    json_rows = df.to_json(orient='records', lines=True)

    # Charger les données dans BigQuery
    job = client.load_table_from_file(
        io.StringIO(json_rows),
        table_ref,
        job_config=job_config,
    )

    # Attendre la fin du job
    job.result()
    print("Données chargées avec succès dans : {}".format(table_ref))

except Exception as e:
    print("Erreur lors de l'envoi des données à BigQuery :", str(e))
