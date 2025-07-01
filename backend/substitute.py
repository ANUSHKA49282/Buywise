# backend/substitute.py
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load product catalog
df = pd.read_csv("data/product_catalog.csv")
product_names = df["ProductName"].tolist()
product_embeddings = model.encode(product_names, convert_to_tensor=True)

def get_substitute(product_query):
    try:
        # Encode user query
        query_embedding = model.encode(product_query, convert_to_tensor=True)

        # Compute cosine similarity
        scores = util.cos_sim(query_embedding, product_embeddings)[0]

        # Get top 3 indices
        top_indices = scores.argsort(descending=True)[:3]

        results = df.iloc[[int(i) for i in top_indices]].to_dict(orient="records")
        return {"substitutes": results}
    except Exception as e:
        return {"error": str(e)}
