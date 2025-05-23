from sentence_transformers import SentenceTransformer, util

# Load sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_keywords(keywords):
    return model.encode(keywords, convert_to_tensor=True)

def flag_transcript(transcript, keyword_embeddings, user_keywords, threshold=0.5):
    results = []
    for seg in transcript:
        seg_embedding = model.encode(seg['text'], convert_to_tensor=True)
        score = float(util.cos_sim(seg_embedding, keyword_embeddings).max())

        if score > threshold:
            flag = "critical" if score > 0.75 else "warning"
            print(f"[DEBUG] {seg['text'][:40]}... | score: {score:.2f} → flag: {flag}")
            results.append({
                "timestamp": f"{seg['start']:.2f}-{seg['end']:.2f}",
                "text": seg['text'],
                "score": score,
                "flag": flag
            })
        else:
            sim = util.cos_sim(seg_embedding, keyword_embeddings)
            max_score = float(sim.max())
            max_index = int(sim.argmax())
            print(f"[DEBUG] Segment: {seg['text']}")
            print(f"Matched Keyword: {user_keywords[max_index]} | Score: {max_score:.2f}")

    return results
