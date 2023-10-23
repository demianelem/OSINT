import pandas as pd
import requests
import openpyxl
from bs4 import BeautifulSoup
import time
from google.cloud import bigquery
from io import BytesIO
from google.cloud import storage

def find_excel_file(source_blob_name, bucket_name="osint_bucket1"):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    # Download the contents of the blob as bytes and then load it into a pandas dataframe
    data = blob.download_as_bytes()
    data = BytesIO(data)
    df = pd.read_excel(data)

    return df

# Initialisation du client BigQuery
client = bigquery.Client()
storage_client = storage.Client()
# Récupérer les données depuis BigQuery au lieu du fichier Excel
# Essayer de récupérer les données depuis BigQuery
lienpress = find_excel_file("Flux_RSS.xlsx")
print(lienpress)
#lienpress = pd.read_excel("C://Users//henri//ESILV_A4//PI2//Flux_RSS.xlsx")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept-Language": "en-US, en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}
query_existing_data = "SELECT * FROM `kapkool-d6bba.test.DataPress2`"
try:
    existing_data = client.query(query_existing_data).to_dataframe()
    print(existing_data)
except:
    existing_data = pd.DataFrame(columns=["Titre Article","Source","Date","Pays","Journal","Texte Article","Domaine","Isclimate"])



output = pd.DataFrame(columns=["Titre Article","Source","Date","Pays","Journal","Texte Article","Domaine","Isclimate"])
output["Isclimate"] = False

climateurl = ["https://syndication.lesechos.fr/rss/rss_energie-environnement.xml",
"https://feeds.leparisien.fr/leparisien/rss/environnement",
"https://rss.nytimes.com/services/xml/rss/nyt/EnergyEnvironment.xml",
"https://rss.nytimes.com/services/xml/rss/nyt/Climate.xml",
"http://www.oecd.org/fr/environnement/index.xml"
]
for journal in lienpress.columns:
    if journal == "OuestFrance":
        for url in lienpress[journal]:
            if len(str(url))>10:
                time.sleep(0.3)
                try:
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'xml')
                    items = soup.find_all('item')
                    for item in items:
                        data_dict = {}
                        data_dict["Titre Article"] = item.find('title').get_text(strip=True)
                        data_dict["Source"] = item.find('link').get_text(strip=True)
                        data_dict["Date"] = item.find('pubDate').get_text(strip=True)
                        data_dict["Pays"] = "France"
                        data_dict["Journal"] = "Ouest France"
                        data_dict["Texte Article"] = item.find('description').get_text(strip=True)
                        categories = item.find_all('category')
                        categories_text = '; '.join([category.get_text(strip=True) for category in categories])
                        data_dict["Domaine"] = categories_text
                        if str(url) in climateurl:
                            data_dict["Isclimate"] = True
                        output = pd.concat([output, pd.DataFrame([data_dict])], ignore_index=True)

                    
                except requests.RequestException as e:
                    print("Problème avec le lien : ",url)
                    print(e)
                except Exception as e:
                    print("Autre problème : ", e)
    
    if journal == "LeDauphine.fr" or journal == "LeProgres.fr" or journal == "DNA.fr" or journal == "EstRepublicain.fr" or journal == "LePoint.fr" or journal == "LeMonde.fr" or journal == "LaProvence.com" or journal == "NYTimes" or journal =="OCDE" or journal =="CNN":
            for url in lienpress[journal]:
                if len(str(url))>10:
                    time.sleep(0.3)
                    try:
                        response = requests.get(url, headers=headers)
                        response.raise_for_status()
                        soup = BeautifulSoup(response.content, 'xml')
                        items = soup.find_all('item')
                        for item in items:
                            data_dict = {}
                            data_dict["Titre Article"] = item.find('title').get_text(strip=True)
                            data_dict["Source"] = item.find('link').get_text(strip=True)
                            data_dict["Date"] = item.find('pubDate').get_text(strip=True)
                            data_dict["Pays"] = "France"
                            data_dict["Journal"] = journal
                            data_dict["Texte Article"] = item.find('description').get_text(strip=True)
                            categories = item.find_all('category')
                            categories_text = '; '.join([category.get_text(strip=True) for category in categories])
                            data_dict["Domaine"] = categories_text
                            if journal == "OCDE":
                                data_dict["Domaine"] =  url.split("http://www.oecd.org/fr/")[1].split("/")[0]
                            if str(url) in climateurl:
                                data_dict["Isclimate"] = True
                            output = pd.concat([output, pd.DataFrame([data_dict])], ignore_index=True)

                        
                    except requests.RequestException as e:
                        print("Problème avec le lien : ",url)
                        print(e)
                    except Exception as e:
                        print("Autre problème : ", e)
    if journal == "Lexpress.fr":
        for url in lienpress[journal]:
            if len(str(url))>10:
                time.sleep(0.3)
                try:
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'xml')
                    items = soup.find_all('item')
                    for item in items:
                        data_dict = {}
                        data_dict["Titre Article"] = item.find('title').get_text(strip=True)
                        data_dict["Source"] = item.find('link').get_text(strip=True)
                        data_dict["Date"] = item.find('pubDate').get_text(strip=True)
                        data_dict["Pays"] = "France"
                        data_dict["Journal"] = "Lexpress.fr"
                        data_dict["Texte Article"] = item.find('description').get_text(strip=True)
                        categories = item.find_all('category')
                        categories_text = '; '.join([category.get_text(strip=True) for category in categories])
                        data_dict["Domaine"] = categories_text
                        if str(url) in climateurl:
                            data_dict["Isclimate"] = True
                        output = pd.concat([output, pd.DataFrame([data_dict])], ignore_index=True)

                    
                except requests.RequestException as e:
                    print("Problème avec le lien : ",url)
                    print(e)
                except Exception as e:
                    print("Autre problème : ", e)
    if journal == "Leparisien.fr":
        for url in lienpress[journal]:
            if len(str(url))>10:
                time.sleep(0.3)
                try:
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'xml')
                    items = soup.find_all('item')
                    for item in items:
                        data_dict = {}
                        data_dict["Titre Article"] = item.find('title').get_text(strip=True)
                        data_dict["Source"] = item.find('link').get_text(strip=True)
                        data_dict["Date"] = ""
                        data_dict["Pays"] = "France"
                        data_dict["Journal"] = "Leparisien.fr"
                        data_dict["Texte Article"] = ""
                        categories = item.find_all('category')
                        categories_text = '; '.join([category.get_text(strip=True) for category in categories])
                        data_dict["Domaine"] = categories_text
                        if str(url) in climateurl:
                            data_dict["Isclimate"] = True
                        output = pd.concat([output, pd.DataFrame([data_dict])], ignore_index=True)

                    
                except requests.RequestException as e:
                    print("Problème avec le lien : ",url)
                    print(e)
                except Exception as e:
                    print("Autre problème : ", e)
    if journal == "LeFigaro.fr":
        for url in lienpress[journal]:
            if len(str(url))>10:
                time.sleep(0.3)
                try:
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'xml')
                    items = soup.find_all('item')
                    for item in items:
                        data_dict = {}
                        data_dict["Titre Article"] = item.find('title').get_text(strip=True)
                        data_dict["Source"] = item.find('link').get_text(strip=True)
                        data_dict["Date"] = item.find('pubDate').get_text(strip=True)
                        data_dict["Pays"] = "France"
                        data_dict["Journal"] = "Le Figaro" 
                        data_dict["Texte Article"] = item.find('description').get_text(strip=True)
                        categories = item.find_all('category')
                        categories_text = '; '.join([category.get_text(strip=True) for category in categories])
                        data_dict["Domaine"] = categories_text
                        if str(url) in climateurl:
                            data_dict["Isclimate"] = True                        
                        output = pd.concat([output, pd.DataFrame([data_dict])], ignore_index=True)

                    
                except requests.RequestException as e:
                    print("Problème avec le lien : ",url)
                    print(e)
                except Exception as e:
                    print("Autre problème : ", e)

# Ajoutez output à existing_data en supprimant les doublons
all_data = existing_data.copy()
all_data.loc[all_data.shape[0]:] = output
#all_data = all_data.drop_duplicates(subset=["Titre Article", "Source"]).reset_index(drop=True)
print(all_data)
print(existing_data.columns)
print(output.columns)
# Création d'un tableau BigQuery depuis un datagramme
dataset_ref = client.dataset('test')
table_ref = dataset_ref.table('DataPress2')
job = client.load_table_from_dataframe(all_data, table_ref)
job.result()