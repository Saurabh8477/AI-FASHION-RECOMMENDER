
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

app = FastAPI()

DATA_PATH = os.path.join("..", "data", "products.json")

with open(DATA_PATH, "r") as f:
    PRODUCTS = json.load(f)

def build_text(p):
    tags = " ".join(p.get("tags", []))
    return f"{p.get('name','')} {p.get('category','')} {tags} {p.get('description','')}"

CORPUS = [build_text(p) for p in PRODUCTS]
VECT = TfidfVectorizer(stop_words="english")
X = VECT.fit_transform(CORPUS)

class RecommendRequest(BaseModel):
    query: str
    budget: int = 999999

@app.post("/recommend")
def recommend(req: RecommendRequest):
    q_vec = VECT.transform([req.query])
    sims = cosine_similarity(q_vec, X)[0]

    ranked = sorted(
        [(i, float(sims[i])) for i in range(len(PRODUCTS))],
        key=lambda x: x[1],
        reverse=True
    )

    results = []
    for idx, score in ranked:
        p = PRODUCTS[idx]
        if p["price"] > req.budget:
            continue
        results.append({**p, "score": score})

    return {"results": results}
