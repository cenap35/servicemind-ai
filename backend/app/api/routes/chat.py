from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.mechanic_agent import ask_mechanic

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    user_message: str
    assistant_message: str
    source_file: str


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer, source_file = ask_mechanic(request.message)

    return ChatResponse(
        user_message=request.message,
        assistant_message=answer,
        source_file=source_file,
    )