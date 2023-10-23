from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import make_pipeline
import joblib
import datetime
import pandas as pd
from sklearn.linear_model import SGDClassifier
# Entraînez ce modèle avec vos données

starttrain = datetime.datetime.now()
print(starttrain)

print("PROGRAMME EN COURS NE PAS TOUCHER")
dataglobal = pd.read_excel("DataPress.xlsx")
dataglobal["Titre Article"] = dataglobal["Titre Article"].fillna("")
dataglobal["Texte Article"] = dataglobal["Texte Article"].fillna("")
# Filtrer les données pour garder uniquement celles qui sont liées au changement climatiqu
# e

# Combiner le titre et le texte de l'article pour obtenir un texte complet
dataglobal["text"] = dataglobal["Titre Article"] + " " + dataglobal["Texte Article"]
print(dataglobal["Isclimate"].shape)
    # process df
print(dataglobal)
# Premièrement, supposons que vous ayez un ensemble de données d'entraînement comme celui-ci:


X_train = dataglobal["Titre Article"]

# Concaténation des colonnes dans le bon format pour MultiOutputClassifier
y_train = dataglobal["Isclimate"]

#X_train = ['j\'achète des fruits','j\'achète des pèches', 'j\'achète des légumes', 'j\'achète des pomme de terre','j\'achète un vélo', 'j\'achète des chaussures de course','j\'achète une maison','j\'achète un appartement']

#%%
def train_model(X, y):
    vectorizer = TfidfVectorizer(max_features=5000)
    classifier = MultiOutputClassifier(SGDClassifier(tol=0.1), n_jobs=-1)
    model = make_pipeline(vectorizer, classifier)
    model.fit(X, y)

    # Sauvegardez le modèle entraîné pour une utilisation future
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