def apply_filters(df, req):
    
    if req.min_engagement:
        df = df[df["engagement"] >= req.min_engagement]

    if req.location:
        df = df[df["location"] == req.location]

    if req.language:
        df = df[df["language"] == req.language]

    return df
