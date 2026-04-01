from sentence_transformers import SentenceTransformer
from app.config.settings import all-MiniLM-L6-v2

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    return model.encode(text)
