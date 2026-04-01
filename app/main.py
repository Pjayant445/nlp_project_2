from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.recommend import router

app = FastAPI(title="Influencer Recommendation API")

# CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
