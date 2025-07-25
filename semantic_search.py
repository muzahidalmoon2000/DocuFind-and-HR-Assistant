
from sentence_transformers import SentenceTransformer, util

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def rank_files_by_similarity(query, files, top_k=None):
    if not files:
        return []

    file_names = [f['name'] for f in files]
    query_embedding = model.encode(query, convert_to_tensor=True)
    name_embeddings = model.encode(file_names, convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(query_embedding, name_embeddings)[0]
    ranked_indices = similarities.argsort(descending=True)

    if top_k is None:
        top_k = len(files)

    top_matches = []
    for idx in ranked_indices[:top_k]:
        file = files[int(idx)]
        file['similarity_score'] = float(similarities[idx])
        top_matches.append(file)

    return top_matches
