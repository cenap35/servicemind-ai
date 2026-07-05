from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    tags=["System"],
)


class HealthResponse(BaseModel):
    status: str
    service: str


@router.get("/")
def root():
    return {"message": "Welcome to ServiceMind AI"}


@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="healthy",
        service="ServiceMind AI API",
    )