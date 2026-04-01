from fastapi import APIRouter
import pandas as pd

from app.models.schema import RecommendationRequest
from app.services.nlp import get_embedding
from app.services.ranking import compute_similarity, follower_score, engagement_rate, final_score
from app.services.filters import apply_filters

router = APIRouter()

# Load dataset
df = pd.read_csv("app/data/influencers.csv")


@router.post("/recommend")
def recommend(req: RecommendationRequest):

    product_text = req.description + " " + " ".join(req.keywords or [])
    product_vec = get_embedding(product_text)

    df_copy = df.copy()

    # Compute engagement
    df_copy["engagement"] = df_copy.apply(
        lambda x: engagement_rate(x["avg_likes"], x["avg_comments"], x["followers"]),
        axis=1
    )

    # Apply filters
    df_copy = apply_filters(df_copy, req)

    scores = []

    for _, row in df_copy.iterrows():
        influencer_text = row["bio"] + " " + row["captions"]
        inf_vec = get_embedding(influencer_text)

        sim = compute_similarity(product_vec, inf_vec)
        f_score = follower_score(row["followers"], req.target_followers)

        score = final_score(sim, f_score, row["engagement"], req.engagement_priority)

        scores.append({
            "username": row["username"],
            "followers": row["followers"],
            "engagement": round(row["engagement"], 3),
            "score": round(score, 3)
        })

    # Sort
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)

    return scores[:req.top_k]
