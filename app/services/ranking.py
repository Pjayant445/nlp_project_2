from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(vec1, vec2):
    return cosine_similarity([vec1], [vec2])[0][0]


def follower_score(actual, target):
    if target == 0:
        return 0
    return 1 - abs(actual - target) / target


def engagement_rate(likes, comments, followers):
    if followers == 0:
        return 0
    return (likes + comments) / followers


def final_score(sim, f_score, eng, eng_weight=0.3):
    return (
        0.5 * sim +
        0.2 * f_score +
        eng_weight * eng
    )
