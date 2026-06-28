from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.mechanic_agent import ask_mechanic

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


class ChatRequest(BaseModel):
    message: str


@router.post("/")
def chat(request: ChatRequest):
    answer = ask_mechanic(request.message)

    return {
        "user_message": request.message,
        "assistant_message": answer,
    }