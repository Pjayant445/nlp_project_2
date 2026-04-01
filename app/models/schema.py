from pydantic import BaseModel
from typing import List, Optional

class RecommendationRequest(BaseModel):
    product_name: str
    description: str
    category: Optional[str]

    target_followers: int
    flexibility: float

    platform: Optional[str]
    engagement_priority: float

    location: Optional[str]
    language: Optional[str]

    keywords: Optional[List[str]]
    min_engagement: Optional[float] = 0.0

    top_k: int = 10
    sort_by: str = "best_match"
