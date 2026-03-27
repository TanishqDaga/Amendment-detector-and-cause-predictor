import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')


def load_dataset():
    with open("cause_dataset.json", "r") as f:
        return json.load(f)


def build_embeddings(dataset):
    texts = [d["old"] + " " + d["new"] for d in dataset]
    embeddings = model.encode(texts, convert_to_tensor=True)
    return embeddings


def save_embeddings(embeddings):
    import torch
    torch.save(embeddings, "cause_embeddings.pt")


if __name__ == "__main__":
    data = load_dataset()
    emb = build_embeddings(data)
    save_embeddings(emb)

    print("✅ Model embeddings ready")