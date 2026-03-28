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


from intent_detector import detect_intent
from cause_knowledge import CAUSE_KB
import random


def predict_cause(old_rule, new_rule):
    intent = detect_intent(old_rule, new_rule)

    causes = CAUSE_KB.get(intent, ["to improve overall system efficiency"])

    # pick 2–3 causes (no repetition)
    selected = random.sample(causes, min(3, len(causes)))

    return " | ".join(selected)