import transformers
from torch.utils.data import DataLoader, TensorDataset
import torch
from torch.optim import AdamW
from sklearn.model_selection import train_test_split
import pandas as pd
from tqdm import tqdm
import datetime

# Chargement des données
dataglobal = pd.read_excel("DataPress.xlsx")
dataglobal["Titre Article"] = dataglobal["Titre Article"].fillna("")
dataglobal["Texte Article"] = dataglobal["Texte Article"].fillna("")
dataglobal["Isclimate"] = dataglobal["Isclimate"].apply(lambda x: False if x != True else x)
dataglobal["text"] = dataglobal["Titre Article"] + " " + dataglobal["Texte Article"]

# Préparation des données pour BERT
tokenizer = transformers.BertTokenizer.from_pretrained("bert-base-uncased")
max_len = 200 # Choisissez une valeur max_len qui convient à votre projet
batch_size = 8 # Adaptez la taille du lot en fonction de la mémoire disponible

# Encodage des données
input_ids = tokenizer(
    dataglobal["text"],
    padding=True,
    truncation=True,
    max_length=max_len,
    return_tensors="pt"
)
attention_masks = input_ids.attention_mask
labels = dataglobal["Isclimate"].to_numpy()

# Séparation des données en ensembles d'entraînement et de test
train_data, val_data = train_test_split(
    (input_ids, attention_masks, labels),
    test_size=0.1,
    random_state=42
)
train_dataloader = DataLoader(
    train_data,
    batch_size=batch_size,
    shuffle=True
)
val_dataloader = DataLoader(
    val_data,
    batch_size=batch_size,
    shuffle=False
)

# Initialisation du modèle BERT
model = transformers.BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
optimizer = AdamW(model.parameters(), lr=2e-5)

# Entraînement du modèle
num_epochs = 3 # Ajustez selon vos besoins

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    for batch in tqdm(train_dataloader):
        batch = tuple(t.to(device) for t in batch)
        
        model.zero_grad()
        outputs = model(**batch)
        
        loss = outputs.loss
        total_loss += loss.item()
        loss.backward()
        
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
    
    print(f"Epoch: {epoch+1}, Loss: {total_loss/len(train_dataloader)}")

# Sauvegarde du modèle
model.save_pretrained(".")

# Pour prédiction:
# Mettre le modèle en mode évaluation
model.eval()

# Définir la phrase à tester
text = "une nouvelle sécheresse en Israël"

# Encodage de la phrase
encoded_inputs = tokenizer(
    text,
    padding=True,
    truncation=True,
    max_length=max_len,
    return_tensors="pt"
)

# Prédiction avec le modèle
with torch.no_grad():
    outputs = model(**encoded_inputs)

# Récupération de la prédiction
logits = outputs.logits
predicted_class_idx = torch.argmax(logits, dim=1).item() # prendre l'index de la classe avec la plus grande logit

# Affichage de la prédiction
if predicted_class_idx == 0:
    print("La phrase n'est pas liée au changement climatique selon le modèle.")
else:
    print("La phrase est liée au changement climatique selon le modèle.")
