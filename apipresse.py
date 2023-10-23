from gnewsclient import gnewsclient
import pandas as pd

# Créer un client de news
client = gnewsclient.NewsClient(
                                )

# Récupérer les articles
articles = client.get_news()

# Créer une liste pour stocker les données d'article
data = []
# Extraire les données et les ajouter à la liste
for article in articles:
    data.append([article['title'], article['link']])

# Créer un DataFrame avec les données
df = pd.DataFrame(data, columns=['Titre', 'Lien'])

# Exporter les données vers un fichier Excel
#df.to_excel("articles.xlsx", index=False, engine='openpyxl')

print(f"{len(data)} articles ont été enregistrés dans 'articles.xlsx'")
