from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.ollama_client import ask_ollama

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


class ChatRequest(BaseModel):
    message: str


@router.post("/")
def chat(request: ChatRequest):
    answer = ask_ollama(request.message)

    return {
        "user_message": request.message,
        "assistant_message": answer,
    }