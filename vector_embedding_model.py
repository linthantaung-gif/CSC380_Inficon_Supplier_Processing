from encodings import normalize_encoding
from sentence_transformers import SentenceTransformer
from sklearn .metrics.pairwise import cosine_similarity
import numpy as np

model_name = "BAAI/bge-large-en-v1.5"

#loading the embedding model
def load_embedding_model():
    return SentenceTransformer(model_name)

#taking a list of strings and returns a normalized embedding
def embed_texts(model, texts):
    return model.encode(texts, normalize_embeddings=True)

#computes cosine similarity between form embedding and confluence embeddings
#outputs 1D array of scores
def compute_similarity(form_embeddings, confluence_embeddings):
    return cosine_similarity(
        [form_embeddings],
        confluence_embeddings
    )[0]

#find index and score of best match
def find_match(similarity_scores):
    best_index = int(np.argmax(similarity_scores))
    best_score = float(similarity_scores[best_index])
    return best_index, best_score
