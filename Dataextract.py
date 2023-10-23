import pandas as pd
import requests
import openpyxl
from bs4 import BeautifulSoup
import time

lienpress = pd.read_excel("C://Users//henri//ESILV_A4//PI2//Flux_RSS.xlsx")
print(lienpress)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept-Language": "en-US, en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}
try:
    existing_data = pd.read_excel("C://Users//henri//ESILV_A4//PI2//DataPress2.xlsx")
except FileNotFoundError:
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
                        
                        output = output.append(data_dict, ignore_index=True)
                    
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
                            output = output.append(data_dict, ignore_index=True)
                        
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
                        output = output.append(data_dict, ignore_index=True)
                    
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
                        output = output.append(data_dict, ignore_index=True)
                    
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

                        
                        output = output.append(data_dict, ignore_index=True)
                    
                except requests.RequestException as e:
                    print("Problème avec le lien : ",url)
                    print(e)
                except Exception as e:
                    print("Autre problème : ", e)
    
print(output)
print(output["Domaine"])
all_data = pd.concat([existing_data, output]).drop_duplicates(subset=["Titre Article", "Source"], keep='last')

# Exporter toutes les données dans le fichier Excel
all_data.to_excel("C://Users//henri//ESILV_A4//PI2//DataPress2.xlsx", index=False)


"""
lienpress[['Nom du journal', 'Type de titre']] = lienpress['titre'].str.split(' - ', 1, expand=True)

# Supprime la colonne "titre" originale si nécessaire
lienpress.drop(columns=['titre'], inplace=True)

# Affiche le DataFrame résultant
print(lienpress)

urls = lienpress["url"]
all_data = pd.DataFrame()

# Parcourir toutes les URLs
for url in urls:
    try:
        # Vérifier que l'URL pointe vers un fichier XML
        if not url.lower().endswith('.xml'):
            print(f"Skipped (not an XML): {url}")
            continue

        # Faire une requête HTTP pour obtenir le contenu XML
        response = requests.get(url)
        response.raise_for_status()  # Vérifier que la requête a réussi
        
        # Parser le contenu XML avec BeautifulSoup
        soup = BeautifulSoup(response.content, 'xml')
        
        # Créer un dictionnaire pour stocker les données de cet XML
        data_dict = {}
        
        # Parcourir tous les éléments du fichier XML et stocker les données dans data_dict
        for element in soup.find_all(True):
            # Créer une nouvelle colonne pour chaque type de balise
            column_name = element.name
            # Stocker le texte de l'élément dans le dictionnaire
            data_dict[column_name] = element.get_text(strip=True)
        
        # Ajouter les données de ce XML au DataFrame
        all_data = all_data.append(data_dict, ignore_index=True)
    
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {str(e)}")
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")

# Remplacer les NaN par des valeurs vides dans le DataFrame
all_data = all_data.fillna("")

# Exporter les données dans un nouveau fichier Excel
all_data.to_excel('data_extracted.xlsx', engine='openpyxl', index=False)
"""