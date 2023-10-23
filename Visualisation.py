import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import torch
from transformers import BertTokenizer

# Chargement des données
data = pd.read_excel("DataPress.xlsx")

# Encodage des mots
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
encoded_words = tokenizer(data["Titre Article"], return_tensors="pt")

# Conversion de la variable encoded_words en un objet torch.Tensor
encoded_words = torch.tensor(encoded_words)

# Réduction de la dimensionnalité
tsne_model = TSNE(n_components=2, perplexity=30, random_state=42)
reduced_word_embeddings = tsne_model.fit_transform(encoded_words.word_embeddings.numpy())

# Affichage des points
plt.scatter(reduced_word_embeddings[:, 0], reduced_word_embeddings[:, 1], c=data["Isclimate"])
plt.xlabel("Dimension 1")
plt.ylabel("Dimension 2")
plt.show()

# K-means
kmeans = KMeans(n_clusters=2)
labels = kmeans.fit_predict(reduced_word_embeddings)

# Affichage des clusters
plt.scatter(reduced_word_embeddings[:, 0], reduced_word_embeddings[:, 1], c=labels)
plt.xlabel("Dimension 1")
plt.ylabel("Dimension 2")
plt.show()
