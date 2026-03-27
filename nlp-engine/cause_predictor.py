import os
import torch
import json
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dataset_path = os.path.join(BASE_DIR, "cause_dataset.json")
embedding_path = os.path.join(BASE_DIR, "cause_embeddings.pt")

with open(dataset_path, "r") as f:
    dataset = json.load(f)

embeddings = torch.load(embedding_path)


def predict_cause(old_rule, new_rule):
    query = old_rule + " " + new_rule
    query_emb = model.encode(query, convert_to_tensor=True)

    scores = util.cos_sim(query_emb, embeddings)[0]

    # 🔥 TOP 3 causes
    top_k = scores.topk(3)

    causes = []
    for idx in top_k.indices:
        causes.append(dataset[idx]["label"])

    return " | ".join(causes)