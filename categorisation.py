import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification, logging
from tqdm import tqdm

# Désactivation des logs non essentiels
logging.set_verbosity_error()

# Chargement des données
dataglobal = pd.read_excel("DataPress2.xlsx")
dataglobal["Titre Article"] = dataglobal["Titre Article"].fillna("")
dataglobal["Prédiction"] = False # Initialisation de la nouvelle colonne à False

# Chargement du modèle et du tokenizer pré-entraînés
model_path = "C://Users//henri//Downloads"
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)



# Mettre le modèle en mode évaluation
model.eval()

# Fonction pour prédire si une phrase est liée au changement climatique ou non
def predict(text, tokenizer, model):
    inputs = tokenizer(
        text,
        padding=True,
        truncation=True,
        max_length=200,
        return_tensors="pt"
    )
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_idx = torch.argmax(logits, dim=1).item()
    return predicted_class_idx

# Application de la prédiction à tous les titres d'articles et stockage des résultats dans "Prédiction"
for idx, row in tqdm(dataglobal.iterrows(), total=dataglobal.shape[0]):
    dataglobal.at[idx, "Prédiction"] = predict(row["Titre Article"], tokenizer, model) == 1

# Exportation des résultats dans un fichier Excel
dataglobal.to_excel("Results.xlsx", index=False)
