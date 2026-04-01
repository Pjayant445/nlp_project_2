from fastapi import FastAPI
from app.routes.recommend import router

app = FastAPI(title="Influencer Recommendation API")

app.include_router(router)
