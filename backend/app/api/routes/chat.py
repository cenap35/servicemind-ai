from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


class ChatRequest(BaseModel):
    message: str


@router.post("/")
def chat(request: ChatRequest):
    return {
        "user_message": request.message,
        "assistant_message": "AI connection will be added soon.",
    }