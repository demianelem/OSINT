#%%
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import make_pipeline
import joblib
import datetime
import pandas as pd
from sklearn.linear_model import SGDClassifier
import re
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

# Entraînez ce modèle avec vos données

starttrain = datetime.datetime.now()
print(starttrain)

print("PROGRAMME EN COURS NE PAS TOUCHER")
dataglobal = pd.read_excel("DataPress.xlsx")
dataglobal["Titre Article"] = dataglobal["Titre Article"].fillna("")
dataglobal["Texte Article"] = dataglobal["Texte Article"].fillna("")
# Filtrer les données pour garder uniquement celles qui sont liées au changement climatiqu
# e

dataglobal["Isclimate"] = dataglobal["Isclimate"].apply(lambda x: False if x != True else x)

# Combiner le titre et le texte de l'article pour obtenir un texte complet
dataglobal["text"] = dataglobal["Titre Article"] + " " + dataglobal["Texte Article"]
print(dataglobal["Isclimate"].shape)
    # process df
print(dataglobal)

# Premièrement, supposons que vous ayez un ensemble de données d'entraînement comme celui-ci:
dataglobal["Isclimate"] = dataglobal["Isclimate"].astype(bool)


def preprocess_text(text):
    # Supprimer la ponctuation et les caractères non désirés, convertir en minuscules
    text = re.sub(r'\W', ' ', str(text))
    text = text.lower()
    # Supprimer les stopwords
    stop_words = set(stopwords.words('english'))  # ou 'french' selon votre texte
    words = text.split()
    text = ' '.join([word for word in words if word not in stop_words])
    return text

dataglobal["text"] = dataglobal["Titre Article"] + " " + dataglobal["Texte Article"]
dataglobal["clean_text"] = dataglobal["text"].apply(lambda x: preprocess_text(x))

# Split data
X_train, X_test, y_train, y_test = train_test_split(dataglobal["clean_text"], dataglobal["Isclimate"], test_size=0.2, random_state=42)



#X_train = ['j\'achète des fruits','j\'achète des pèches', 'j\'achète des légumes', 'j\'achète des pomme de terre','j\'achète un vélo', 'j\'achète des chaussures de course','j\'achète une maison','j\'achète un appartement']

#%%
def train_model(X, y):
    vectorizer = TfidfVectorizer(max_features=5000)
    classifier = SGDClassifier(tol=0.1)
    model = make_pipeline(vectorizer, classifier)
    model.fit(X, y)
    joblib.dump(model, 'modelMinistere.pkl')


# Prédire les catégories d'un texte
def predict_categories(text):
    model = joblib.load('modelMinistere.pkl')

    # Le modèle prédit les catégories
    predictions = model.predict([text])

    return predictions[0]

# Entraînez le modèle avec ces données
train_model(X_train, y_train)
end = datetime.datetime.now()
print('Temps pour entrainement : '+str(end-starttrain))

end = datetime.datetime.now()
print('Temps pour entrainement : '+str(end-starttrain))
# Maintenant, supposons que vous ayez un nouvel énoncé et que vous vouliez prédire sa catégorie:
#%%
text = "Une nouvelle sécheresse pour israel"

# Utilisez la fonction de prédiction pour obtenir les catégories
categories = predict_categories(text)

print(f'Les catégories prédites pour "{text}" sont {categories}.')
print("Temps pour analyse : "+str(datetime.datetime.now()-end))