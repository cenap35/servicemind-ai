from fastapi import FastAPI

from app.api.router import router

app = FastAPI(
    title="ServiceMind AI API",
    description="AI-powered automotive intelligence platform.",
    version="1.0.0",
)

app.include_router(router)