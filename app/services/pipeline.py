from app.services.nlp import get_embedding
from app.services.ranking import (
    compute_similarity,
    follower_score,
    engagement_rate,
    final_score
)
from app.services.filters import apply_filters
from app.repository.data_loader import load_data


def run_pipeline(req):

    df = load_data()

    # Combine product text
    product_text = req.description + " " + " ".join(req.keywords or [])
    product_vec = get_embedding(product_text)

    # Compute engagement
    df["engagement"] = df.apply(
        lambda x: engagement_rate(x["avg_likes"], x["avg_comments"], x["followers"]),
        axis=1
    )

    # Apply filters
    df = apply_filters(df, req)

    results = []

    for _, row in df.iterrows():

        influencer_text = row["bio"] + " " + row["captions"]
        inf_vec = get_embedding(influencer_text)

        sim = compute_similarity(product_vec, inf_vec)
        f_score = follower_score(row["followers"], req.target_followers)

        score = final_score(sim, f_score, row["engagement"], req.engagement_priority)

        results.append({
            "username": row["username"],
            "followers": int(row["followers"]),
            "engagement": round(row["engagement"], 4),
            "score": round(score, 4)
        })

    # Sort results
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:req.top_k]
