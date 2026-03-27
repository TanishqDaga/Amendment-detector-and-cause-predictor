from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')


def match_rules(old_rules, new_rules):
    old_embeddings = model.encode(old_rules, convert_to_tensor=True)
    new_embeddings = model.encode(new_rules, convert_to_tensor=True)

    sim_matrix = util.cos_sim(old_embeddings, new_embeddings)

    matches = []
    used_new = set()

    for i in range(len(old_rules)):
        best_j = sim_matrix[i].argmax().item()
        best_score = sim_matrix[i][best_j].item()

        matches.append((i, best_j, best_score))
        used_new.add(best_j)

    return matches, used_new