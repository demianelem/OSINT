import requests
import pandas as pd
import time

"""
# Insérez votre clé API CORE ici
api_key = 'u8Gytfa1MAwc2HCYXqseml9QTPjkUEBn'
# URL de l'endpoint API (Veuillez vérifier dans la documentation de CORE pour l'URL exacte)
api_url = 'https://core.ac.uk:443/api-v3/articles/search'

# Paramètres de requête (Adaptez-les selon vos besoins et la documentation de l'API)
params = {
    'apiKey': api_key,
    'page': 1,
    'pageSize': 100,
    'query': "global warming OR climate change"
}


# Faire une requête API
response = requests.get(api_url, params=params)
print(response.json())
# Vérifiez le statut de la réponse
if response.status_code == 200:
    # Chargez les données en JSON
    data = response.json()
    
    # Transformez les données en DataFrame (adaptez selon la structure des données réelles)
    df = pd.DataFrame(data['data'])
    
    # Exportez les données en fichier Excel
    df.to_excel('core_articles.xlsx', index=False)
else:
    print('Failed to retrieve data:', response.status_code)
"""


api_url = 'https://chroniclingamerica.loc.gov/search/pages/results/'
all_items = []

params = {
    'andtext': 'climate incident OR climate crisis OR extreme weather',
    'format': 'json',
    'rows': 50,  # Maximum autorisé par l'API
    'page': 1  # Page de résultats à récupérer
}

while True:  # Boucle pour continuer à récupérer des pages supplémentaires
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"An error occurred: {str(e)}")
        break
    else:
        data = response.json()
        if 'items' in data:
            all_items.extend(data['items'])
            params['page'] += 1  # Incrementer le numéro de page pour la prochaine requête
            print(f"Page {params['page']} retrieved. Total items: {len(all_items)}")
            if len(data['items']) < params['rows']:
                # Si nous avons récupéré moins d'items que le maximum, nous avons probablement atteint la dernière page
                break
        else:
            # Si 'items' n'est pas dans la réponse, nous avons probablement atteint la fin des résultats
            break
    
    time.sleep(1) 

df = pd.DataFrame(all_items)
df.to_excel('chronicling_america_climate_data.xlsx', index=False)

