from fastapi import APIRouter

router = APIRouter(
    tags=["System"],
    )


@router.get("/")
def root():
    return {"message": "Welcome to ServiceMind AI"}


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ServiceMind AI API",
    }
