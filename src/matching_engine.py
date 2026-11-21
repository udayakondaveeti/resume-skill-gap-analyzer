from sentence_transformers import SentenceTransformer, util


def compute_semantic_similarity(
    resume_text: str,
    jd_text: str,
    model_name: str = "all-MiniLM-L6-v2",
) -> float:
    """Return cosine similarity percentage (0-100) between resume and JD."""
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    model = SentenceTransformer(model_name)
    embeddings = model.encode([resume_text, jd_text], convert_to_tensor=True)
    score = util.cos_sim(embeddings[0], embeddings[1]).item()
    return round(max(0.0, min(1.0, score)) * 100, 2)